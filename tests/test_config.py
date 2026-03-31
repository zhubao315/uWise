#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""配置模块测试"""

import pytest
from pathlib import Path
from scripts.config import Settings


def test_settings_initialization():
    """测试配置初始化"""
    settings = Settings()
    assert settings.cache_enabled is True
    assert settings.cache_ttl_hours == 24
    assert settings.max_retries == 3


def test_settings_paths():
    """测试路径配置"""
    settings = Settings()
    assert isinstance(settings.project_root, Path)
    assert isinstance(settings.docs_dir, Path)
    assert isinstance(settings.log_file, Path)


def test_settings_domains():
    """测试领域配置"""
    settings = Settings()
    assert isinstance(settings.domains, dict)
    assert "架构师" in settings.domains
    assert "投资人" in settings.domains
    assert len(settings.domains["架构师"]) > 0
