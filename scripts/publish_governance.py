#!/usr/bin/env python3
"""Shadow-mode publishing governance for the private uWise vault.

This module does NOT publish anything. It reads the private vault (already
downloaded or fetched via the existing sync helper), applies an explicit
publish gate, scans for sensitive data, and writes a report plus optional
shadow pages into a directory OUTSIDE docs/. It is safe to run in CI.

Publishing rule (all must hold):
    status == reviewed AND visibility == public AND publish is true
Anything else is blocked with explicit reasons. High-risk sensitive hits
also block publishing even when the metadata is otherwise valid.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

os.environ.setdefault("VAULT_DIR", "/tmp/uwise-vault-shadow")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import yaml  # noqa: E402
from scripts import sync_uwise_vault as sync  # noqa: E402

VAULT_DIR = Path(os.environ["VAULT_DIR"])
SHADOW_DIR = Path(os.environ.get("SHADOW_DIR", "/tmp/uwise-shadow-pages"))
REPORT_DIR = Path(os.environ.get("REPORT_DIR", "/tmp/uwise-governance-report"))

REQUIRED_FOR_PUBLISH = {"status": "reviewed", "visibility": "public", "publish": True}
SCHEMA_FIELDS = (
    "title",
    "aliases",
    "type",
    "domain",
    "identity",
    "project",
    "tags",
    "status",
    "visibility",
    "publish",
    "reviewed_at",
    "source_id",
    "updated_at",
    "related",
)

# (name, pattern, replacement). Add new rules here; every hit is reported.
REDACT_RULES: tuple[tuple[str, re.Pattern[str], str], ...] = (
    ("phone", re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)"), "[REDACTED_PHONE]"),
    ("email", re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b"), "[REDACTED_EMAIL]"),
    (
        "github_token",
        re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,}"),
        "[REDACTED_TOKEN]",
    ),
    (
        "api_key",
        re.compile(r'(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*["\']?[A-Za-z0-9_\-]{16,}'),
        "[REDACTED_SECRET]",
    ),
    (
        "private_path",
        re.compile(r'(?:/home/[^/\s]+|/root/|C:\\Users\\|/fs/|/opt/data/obsidian)[^\s`"\'）)]*'),
        "[REDACTED_PATH]",
    ),
    (
        "private_repo",
        re.compile(r"github\.com/zhubao315/obsidian-vault|obsidian_vault|obsidian-vault"),
        "[PRIVATE_SOURCE]",
    ),
)
HIGH_RISK = {"phone", "email", "github_token", "api_key", "private_path", "private_repo"}


@dataclass
class Decision:
    """Publishing decision for one vault entry."""

    source_id: str
    title: str
    rel_path: str
    publish: bool
    reasons: list[str] = field(default_factory=list)
    sensitive: list[str] = field(default_factory=list)
    schema_issues: list[str] = field(default_factory=list)
    stable_url: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialize for the JSON report."""
        return asdict(self)


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Parse YAML frontmatter with a real parser; raise on malformed YAML."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end < 0:
        raise ValueError("frontmatter not closed")
    data = yaml.safe_load(text[3:end]) or {}
    if not isinstance(data, dict):
        raise ValueError("frontmatter is not a mapping")
    return data, text[end + 4 :].lstrip("\n")


def stable_id(rel_path: str) -> str:
    """Stable ID derived from the source path, not from a mutable title."""
    return "e-" + hashlib.sha1(rel_path.encode("utf8")).hexdigest()[:12]


def scan_sensitive(text: str) -> tuple[str, list[str]]:
    """Apply all redaction rules and return cleaned text plus rule names."""
    cleaned = text
    hits: list[str] = []
    for name, pattern, replacement in REDACT_RULES:
        cleaned, count = pattern.subn(replacement, cleaned)
        if count:
            hits.append(name)
    return cleaned, hits


def check_schema(frontmatter: dict[str, Any]) -> list[str]:
    """Report missing or malformed governance fields."""
    issues: list[str] = []
    for key in SCHEMA_FIELDS:
        if key not in frontmatter:
            issues.append(f"missing:{key}")
    for key in ("title", "status", "visibility", "reviewed_at", "source_id"):
        if key in frontmatter and not isinstance(frontmatter[key], str):
            issues.append(f"type:{key}")
    if "publish" in frontmatter and not isinstance(frontmatter["publish"], bool):
        issues.append("type:publish")
    return issues


def decide(frontmatter: dict[str, Any], body: str, rel_path: str) -> Decision:
    """Apply the publish gate and sensitivity scan to one entry."""
    sid = stable_id(rel_path)
    title = str(frontmatter.get("title") or Path(rel_path).stem)
    result = Decision(
        source_id=sid,
        title=title,
        rel_path=rel_path,
        publish=False,
        stable_url=f"/uWise/vault-encyclopedia/{sid}/",
    )
    schema = check_schema(frontmatter)
    result.schema_issues = schema
    _, hits = scan_sensitive(body)
    result.sensitive = sorted(set(hits))

    for key, expected in REQUIRED_FOR_PUBLISH.items():
        if frontmatter.get(key) != expected:
            result.reasons.append(f"{key}!={expected}")
    blocked = sorted(set(result.sensitive) & HIGH_RISK)
    if blocked:
        result.reasons.append("sensitive:" + ",".join(blocked))
    if "frontmatter_invalid" in schema:
        result.reasons.append("frontmatter_invalid")
    result.publish = not result.reasons
    return result


def ensure_vault() -> None:
    """Fetch the private vault once when no local copy exists."""
    if not VAULT_DIR.exists():
        sync.fetch_vault()


def build_report() -> dict[str, Any]:
    """Run the shadow gate over the whole vault and return the report."""
    ensure_vault()
    decisions: list[Decision] = []
    parse_errors: list[dict[str, str]] = []
    for path in sorted(VAULT_DIR.rglob("*.md")):
        rel = path.relative_to(VAULT_DIR).as_posix()
        text = path.read_text(encoding="utf8", errors="replace")
        try:
            fm, body = parse_frontmatter(text)
        except Exception as exc:  # noqa: BLE001
            parse_errors.append({"path": rel, "error": str(exc)[:200]})
            decisions.append(
                Decision(
                    source_id=stable_id(rel),
                    title=Path(rel).stem,
                    rel_path=rel,
                    publish=False,
                    reasons=["frontmatter_invalid"],
                    stable_url=f"/uWise/vault-encyclopedia/{stable_id(rel)}/",
                )
            )
            continue
        decisions.append(decide(fm, text, rel))

    SHADOW_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    for d in decisions:
        if not d.publish:
            continue
        target = SHADOW_DIR / d.source_id
        target.mkdir(parents=True, exist_ok=True)
        (target / "index.md").write_text(
            f"---\ntitle: {json.dumps(d.title, ensure_ascii=False)}\n---\n\n# {d.title}\n",
            encoding="utf8",
        )

    reason_counts: dict[str, int] = {}
    sensitive_counts: dict[str, int] = {}
    for d in decisions:
        for reason in d.reasons:
            reason_counts[reason] = reason_counts.get(reason, 0) + 1
        for item in d.sensitive:
            sensitive_counts[item] = sensitive_counts.get(item, 0) + 1

    report = {
        "mode": "shadow (no public pages changed)",
        "source": sync.SOURCE,
        "total": len(decisions),
        "publishable": sum(1 for d in decisions if d.publish),
        "blocked": sum(1 for d in decisions if not d.publish),
        "parse_errors": len(parse_errors),
        "reason_counts": dict(sorted(reason_counts.items(), key=lambda kv: -kv[1])),
        "sensitive_counts": dict(sorted(sensitive_counts.items(), key=lambda kv: -kv[1])),
        "decisions": [d.to_dict() for d in decisions],
        "parse_error_samples": parse_errors[:20],
    }
    (REPORT_DIR / "governance-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf8"
    )
    md = [
        "# uWise 公开发布治理 · 影子报告",
        "",
        f"- 模式：{report['mode']}",
        f"- 来源：{report['source']}",
        f"- 词条总数：{report['total']}",
        f"- 可发布：{report['publishable']} · 阻断：{report['blocked']} "
        f"· YAML 解析失败：{report['parse_errors']}",
        "",
        "## 阻断原因分布",
        "",
        "| 原因 | 数量 |",
        "|---|---:|",
    ]
    reasons: dict[str, int] = report["reason_counts"]  # type: ignore[assignment]
    md += [f"| `{k}` | {v} |" for k, v in reasons.items()]
    md += ["", "## 敏感规则命中", "", "| 规则 | 数量 |", "|---|---:|"]
    sensitive: dict[str, int] = report["sensitive_counts"]  # type: ignore[assignment]
    md += [f"| `{k}` | {v} |" for k, v in sensitive.items()]
    md += ["", "## 待人工审核（前 30 条）", "", "| 词条 | 阻断原因 | 稳定 ID |", "|---|---|---|"]
    for d in [x for x in decisions if not x.publish][:30]:
        md.append(f'| {d.title} | {", ".join(d.reasons[:3])} | `{d.source_id}` |')
    md += ["", "> 本报告不修改任何已发布页面；白名单生效前必须人工审核存量条目。", ""]
    (REPORT_DIR / "governance-report.md").write_text("\n".join(md), encoding="utf8")
    return report


if __name__ == "__main__":
    result = build_report()
    print(
        f"[governance] total={result['total']} publishable={result['publishable']} "
        f"blocked={result['blocked']} parse_errors={result['parse_errors']}"
    )
    print(f"[governance] report: {REPORT_DIR / 'governance-report.md'}")
