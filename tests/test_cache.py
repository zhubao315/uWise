#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""缓存模块测试"""

import pytest
from pathlib import Path
from scripts.cache import CacheManager


@pytest.fixture
def cache_manager(tmp_path):
    """创建临时缓存管理器"""
    return CacheManager(cache_dir=tmp_path, ttl_hours=1)


def test_cache_set_and_get(cache_manager):
    """测试缓存设置和获取"""
    key = "test_key"
    value = {"data": "test_value"}

    cache_manager.set(key, value)
    retrieved = cache_manager.get(key)

    assert retrieved == value


def test_cache_nonexistent_key(cache_manager):
    """测试获取不存在的缓存键"""
    result = cache_manager.get("nonexistent_key")
    assert result is None


def test_cache_clear(cache_manager):
    """测试清空缓存"""
    cache_manager.set("key1", "value1")
    cache_manager.set("key2", "value2")

    cache_manager.clear()

    assert cache_manager.get("key1") is None
    assert cache_manager.get("key2") is None


def test_cache_manager_initialization(tmp_path):
    """测试缓存管理器初始化"""
    manager = CacheManager(cache_dir=tmp_path, ttl_hours=2)
    assert manager.cache_dir == tmp_path
    assert manager.ttl.total_seconds() == 2 * 3600
