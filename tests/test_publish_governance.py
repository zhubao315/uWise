#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for the shadow publishing gate."""

from scripts.publish_governance import decide, parse_frontmatter, scan_sensitive, stable_id


def test_parse_frontmatter_valid():
    """标准 YAML frontmatter 应正确解析."""
    fm, body = parse_frontmatter('---\ntitle: "测试"\nstatus: reviewed\n---\n正文')
    assert fm["title"] == "测试"
    assert body.strip() == "正文"


def test_parse_frontmatter_invalid():
    """非法 YAML 应抛出异常而不是静默通过."""
    try:
        parse_frontmatter("---\ntitle: [unclosed\n---\n正文")
    except Exception:
        return
    raise AssertionError("invalid YAML was accepted")


def test_only_reviewed_public_publishable():
    """只有 reviewed + public + publish 才允许发布."""
    fm = {"title": "A", "status": "reviewed", "visibility": "public", "publish": True}
    d = decide(fm, "正文", "词条/A.md")
    assert d.publish is True
    for bad in [{"status": "draft"}, {"visibility": "private"}, {"publish": False}]:
        mixed = dict(fm, **bad)
        assert decide(mixed, "正文", "词条/A.md").publish is False


def test_missing_fields_blocked():
    """缺少发布许可字段时默认阻断."""
    d = decide({"title": "A"}, "正文", "词条/A.md")
    assert d.publish is False
    assert "status!=reviewed" in d.reasons
    assert d.schema_issues  # missing fields are reported separately


def test_sensitive_content_blocks_even_when_approved():
    """敏感信息即使元数据合规也必须阻断."""
    fm = {"title": "A", "status": "reviewed", "visibility": "public", "publish": True}
    d = decide(fm, "联系 16300465413", "词条/A.md")
    assert d.publish is False
    assert "sensitive:phone" in d.reasons


def test_redaction_rules_are_extensible():
    """脱敏规则应覆盖多种敏感类型."""
    text = "mail a@b.com key: abcdefghijklmnopqrst /home/zhubao315/x obsidian-vault"
    cleaned, hits = scan_sensitive(text)
    assert "[REDACTED_EMAIL]" in cleaned
    assert "email" in hits
    assert "private_repo" in hits


def test_stable_id_survives_title_change():
    """稳定 ID 只依赖源文件路径，标题变化不应改变 URL."""
    assert stable_id("词条/同一篇.md") == stable_id("词条/同一篇.md")
    assert stable_id("词条/同一篇.md") != stable_id("词条/另一篇.md")
