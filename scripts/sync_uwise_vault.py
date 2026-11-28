#!/usr/bin/env python3
"""Weekly sync of private Obsidian uWise entries into public MkDocs pages.

Source (private): zhubao315/obsidian-vault @ 02-BUILD/23-uWise
Output (public, committed): docs/vault-encyclopedia/<slug>/index.md
                            docs/generated/uwise-encyclopedia.md
                            docs/uwise-encyclopedia-index.json

Fetch needs GITHUB_TOKEN from env (Actions secret VAULT_SYNC_PAT, or local env).
Local analysis can use VAULT_DIR to point at an already-downloaded tree.
No scripts from the vault are executed; no fabricated content is added.
"""

import base64
import collections
import concurrent.futures
import hashlib
import json
import os
import re
import shutil
import time
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, cast

REPO = os.environ.get("VAULT_REPO", "zhubao315/obsidian-vault")
PREFIX = os.environ.get("VAULT_PATH", "02-BUILD/23-uWise")
BRANCH = os.environ.get("VAULT_BRANCH", "main")
SRC = Path(os.environ.get("VAULT_DIR", "/tmp/uwise-vault-sync"))
ROOT = Path(os.environ.get("UWISE_DIR", ".")).resolve()
OUT = ROOT / "docs/vault-encyclopedia"
PAGES_DIR = ROOT / "docs/generated"
INDEX_PATH = ROOT / "docs/uwise-encyclopedia-index.json"
SOURCE = f"{REPO}@{BRANCH}:{PREFIX}"


def api(url: str) -> dict[str, Any]:
    """Fetch JSON from the GitHub API with retry."""
    token = os.environ.get("GITHUB_TOKEN", "")
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "uwise-vault-sync/1.0"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    for i in range(5):
        try:
            r = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(r, timeout=120) as f:
                return cast(dict[str, Any], json.loads(f.read().decode()))
        except Exception:
            if i == 4:
                raise
            time.sleep(2**i)
    return {}


def fetch_vault() -> None:
    """Download all markdown entries from the private vault."""
    tree = api(f"https://api.github.com/repos/{REPO}/git/trees/{BRANCH}?recursive=1")
    items = [
        i
        for i in tree["tree"]
        if i["path"].startswith(PREFIX + "/") and i["type"] == "blob" and i["path"].endswith(".md")
    ]
    print(f"[sync] {len(items)} markdown entries", flush=True)

    def one(item: dict[str, Any]) -> None:
        """Download one markdown blob."""
        rel = item["path"][len(PREFIX) + 1 :]
        p = SRC / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if p.exists():
            return
        d = api(f"https://api.github.com/repos/{REPO}/git/blobs/{item['sha']}")
        p.write_bytes(base64.b64decode(d["content"].replace("\n", "")))

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(one, items))


def slugify(value: str, seed: str) -> str:
    """Build a stable ASCII slug with a hash suffix."""
    ascii_part = unicodedata.normalize("NFKC", str(value)).lower()
    ascii_part = re.sub(r"[^a-z0-9]+", "-", ascii_part).strip("-")[:42]
    h = hashlib.sha1(seed.encode("utf8")).hexdigest()[:8]
    return f"{ascii_part}-{h}" if ascii_part else f"entry-{h}"


def parse_fm(text: str) -> tuple[dict[str, Any], str]:
    """Parse simple Obsidian YAML frontmatter."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end < 0:
        return {}, text
    fm_text, body = text[3:end], text[end + 4 :].lstrip("\n")
    fm = {}
    cur = None
    for line in fm_text.splitlines():
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            cur = m.group(1)
            v = m.group(2).strip()
            if len(v) >= 2 and v[0] == v[-1] and v[0] in ('"', "'"):
                v = v[1:-1]
            fm[cur] = v
        elif cur and re.match(r"^\s+-\s+", line):
            values = fm.get(cur)
            if not isinstance(values, list):
                values = []
                fm[cur] = values
            values.append(re.sub(r'^[\s-]+|["\']$', "", line.strip()))
    return fm, body


REDACT_RULES: tuple[tuple[str, re.Pattern[str], str], ...] = (
    ("phone", re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)"), "[REDACTED_PHONE]"),
    ("email", re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b"), "[REDACTED_EMAIL]"),
    (
        "token",
        re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,}"),
        "[REDACTED_TOKEN]",
    ),
    (
        "secret",
        re.compile(r"(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*[\"\']?[A-Za-z0-9_\-]{16,}"),
        "[REDACTED_SECRET]",
    ),
    (
        "path",
        re.compile(r"(?:/home/[^/\s]+|/root/|C:\\Users\\|/fs/|/opt/data/obsidian)[^\s`\"\'）)]*"),
        "[REDACTED_PATH]",
    ),
    (
        "repo",
        re.compile(r"github\.com/zhubao315/obsidian-vault|obsidian_vault|obsidian-vault"),
        "[PRIVATE_SOURCE]",
    ),
)


def normalize_status(value: object) -> str:
    """Map inconsistent source statuses to a small controlled vocabulary."""
    v = str(value or "").strip().strip('"')
    low = v.lower()
    if not v or low in ("未标注", "none", "null"):
        return "unreviewed"
    if low in ("draft", "草稿"):
        return "draft"
    if low in ("published", "已发布"):
        return "published"
    if low in ("active", "已确立", "成熟"):
        return "active"
    return v


def normalize_category(fm: dict[str, Any], rel: str) -> str:
    """Derive a public category without exposing the private source path."""
    value = str(fm.get("category") or "").strip().strip('"')
    if value:
        return value
    source = str(fm.get("source") or "").strip().strip('"')
    if "B6-" in source or "investment" in source.lower():
        return "finance-investment"
    if "01-BRAIN" in source:
        return "concepts"
    if "reading" in str(fm.get("source_type") or "").lower():
        return "reading"
    return "uncategorized"


def redact(text: str) -> str:
    """Remove private identifiers before publishing."""
    cleaned = text
    for _name, pattern, replacement in REDACT_RULES:
        cleaned = pattern.sub(replacement, cleaned)
    return cleaned


def main() -> None:  # noqa: C901
    """Convert the downloaded vault into publishable MkDocs pages."""
    if not SRC.exists():
        fetch_vault()
    files = sorted(SRC.rglob("*.md"))
    print(f"[sync] converting {len(files)} entries", flush=True)

    entries: list[dict[str, Any]] = []
    for p in files:
        rel = p.relative_to(SRC).as_posix()
        text = p.read_text(encoding="utf8", errors="replace")
        fm, body = parse_fm(text)
        if body.startswith("# "):
            body = body.split("\n", 1)[1].lstrip("\n")
        title = str(fm.get("title") or p.stem)
        entries.append(
            {
                "slug": slugify(title if title != p.stem else rel, rel),
                "title": title,
                "rel": rel,
                "source_id": "e-" + hashlib.sha1(rel.encode("utf8")).hexdigest()[:12],
                "fm": fm,
                "body": body,
                "aliases": fm.get("aliases") if isinstance(fm.get("aliases"), list) else [],
            }
        )

    seen = set()
    for e in entries:
        if e["slug"] in seen:
            e["slug"] = slugify(e["title"], e["rel"] + "#dup")
        seen.add(e["slug"])

    targets: dict[str, str] = {}
    for e in entries:
        for name in [e["title"], *e["aliases"], Path(e["rel"]).stem]:
            targets.setdefault(str(name).strip(), e["slug"])

    wl = re.compile(r"\[\[([^\]|]+?)(?:\|([^\]]+))?\]\]")

    def convert(body: str) -> tuple[str, list[str]]:
        """Rewrite Obsidian wikilinks into relative MkDocs links."""
        broken = []

        def repl(m: re.Match) -> str:
            """Replace one wikilink."""
            target = str(m.group(1)).strip()
            label = str(m.group(2) or target)
            slug = targets.get(target)
            if slug is None:
                broken.append(target)
                escaped = (
                    target.replace("&", "&amp;")
                    .replace('"', "&quot;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                )
                return (
                    f'<span class="uw-unresolved" data-target="{escaped}" '
                    f'title="未解析的双链目标：{escaped}">{label}</span>'
                )
            return f"[{label}](../{slug}/)"

        return wl.sub(repl, body), broken

    shutil.rmtree(OUT, ignore_errors=True)
    OUT.mkdir(parents=True, exist_ok=True)
    PAGES_DIR.mkdir(parents=True, exist_ok=True)

    catalog = []
    for e in entries:
        body, broken = convert(e["body"])
        safe = redact(body)
        summary = ""
        for line in safe.splitlines():
            s = line.strip().lstrip(">").strip()
            if s and not s.startswith("#") and len(s) > 12:
                summary = re.sub(r"[*_`\[\]]", "", s)[:180]
                break
        status = normalize_status(e["fm"].get("status"))
        category = normalize_category(e["fm"], e["rel"])
        quality = (
            "stub"
            if len(safe.strip()) < 300
            else ("draft" if "draft" in status.lower() else "synced")
        )
        desc = summary or ("个人知识百科词条：" + str(e["title"]))
        page = (
            "---\n"
            f'title: {json.dumps(e["title"], ensure_ascii=False)}\n'
            f"description: {json.dumps(desc, ensure_ascii=False)}\n"
            "---\n\n"
            f'# {e["title"]}\n\n{safe.strip()}\n\n'
            "---\n\n<details>\n<summary>来源与口径</summary>\n\n"
            f"- 来源：{SOURCE}\n"
            f"- 来源标识：`{e['source_id']}`（稳定 ID，不暴露私库路径）\n"
            f"- 状态：{status} · 分类：{category}\n"
            f"- 未解析双链：{len(broken)} 条（已保留目标标记）\n"
            "- 本页由每周同步自动生成；内容来自个人笔记，未经逐条事实核验。\n\n</details>\n"
        )
        d = OUT / e["slug"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.md").write_text(page, encoding="utf8")
        catalog.append(
            {
                "slug": e["slug"],
                "title": e["title"],
                "status": status,
                "category": category,
                "quality": quality,
                "broken_links": len(broken),
                "source_id": e["source_id"],
            }
        )

    def esc(value: object) -> str:
        """Escape HTML-sensitive characters in generated tables."""
        return (
            str(value)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )

    broken_counter: dict[str, int] = {}
    # targets are collected during conversion; recompute from the rendered pages
    for page_path in OUT.glob("*/index.md"):
        content = page_path.read_text(encoding="utf8")
        for m in re.finditer(r'class="uw-unresolved" data-target="([^"]+)"', content):
            target = m.group(1)
            broken_counter[target] = broken_counter.get(target, 0) + 1
    top_broken = sorted(broken_counter.items(), key=lambda kv: -kv[1])[:100]
    broken_md = (
        "---\ntitle: uWise 未解析双链报告\n"
        "description: 按引用频次排序的未解析双链目标 · 自动生成\n---\n\n"
        "# 未解析双链报告\n\n"
        f"> 共 {sum(broken_counter.values())} 个未解析引用，{len(broken_counter)} 个不同目标。"
        "这些引用已在词条页保留为可识别标记，但尚未连接到正式词条。\n\n"
        "| 目标 | 引用次数 |\n|---|---:|\n"
        + "\n".join(f"| {esc(t)} | {n} |" for t, n in top_broken)
        + "\n"
    )
    (PAGES_DIR / "uwise-broken-links.md").write_text(broken_md, encoding="utf8")

    INDEX_PATH.write_text(
        json.dumps(
            {
                "source": SOURCE,
                "count": len(catalog),
                "entries": catalog,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf8",
    )

    by_status = collections.Counter(c["status"] for c in catalog)
    rows = "\n".join(
        f'| [{esc(c["title"])}](/uWise/vault-encyclopedia/{c["slug"]}/) | {esc(c["status"])} | '
        f'{esc(c["category"])[:40]} | {c["quality"]} |'
        for c in sorted(catalog, key=lambda x: x["title"])
    )
    md = f"""---
title: uWise 私库词条总览
description: 从私有 Obsidian 仓库同步的 {len(catalog)} 篇知识词条 · 自动生成
---

# uWise 私库词条总览 · {len(catalog)} 篇

> 来源：`{SOURCE}`。本页由 `scripts/sync_uwise_vault.py` 自动生成。
> 所有词条标记为**未逐条核验**；原始状态分布：{esc(str(by_status.most_common(4)))}。

<div class="vault-filter">
  <input id="uwise-search" type="search" placeholder="搜索词条名称…" />
  <span id="uwise-count">{len(catalog)} 篇</span>
</div>

| 词条 | 原始状态 | 分类 | 质量标记 |
|---|---|---|---|
{rows}

<script>
(function () {{
  const input = document.getElementById('uwise-search');
  const rows = Array.from(document.querySelectorAll('table tbody tr'));
  const count = document.getElementById('uwise-count');
  input && input.addEventListener('input', () => {{
    const q = input.value.trim().toLowerCase();
    let shown = 0;
    rows.forEach((r) => {{
      const hit = r.textContent.toLowerCase().includes(q);
      r.hidden = !!q && !hit; if (hit) shown++;
    }});
    if (count) count.textContent = (q ? shown : rows.length) + ' 篇';
  }});
}})();
</script>
"""
    (PAGES_DIR / "uwise-encyclopedia.md").write_text(md, encoding="utf8")
    print(f"[sync] wrote {len(catalog)} pages + catalog", flush=True)


if __name__ == "__main__":
    main()
