#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""配置管理模块"""

import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class Settings:
    """应用配置类"""
    
    # API配置
    openai_api_key: Optional[str] = field(default_factory=lambda: os.getenv("OPENAI_API_KEY"))
    tavily_api_key: Optional[str] = field(default_factory=lambda: os.getenv("TAVILY_API_KEY"))
    
    # 路径配置
    project_root: Path = field(default_factory=lambda: Path(__file__).parent.parent)
    docs_dir: Path = field(default=lambda: Path("docs"))
    update_log: Path = field(default=lambda: Path("docs/UPDATES.md"))
    cache_dir: Path = field(default=lambda: Path(".cache"))
    
    # 缓存配置
    cache_enabled: bool = True
    cache_ttl_hours: int = 24
    
    # 重试配置
    max_retries: int = 3
    retry_delay: float = 1.0
    
    # 日志配置
    log_level: str = "INFO"
    log_file: Path = field(default=lambda: Path("logs/uwise.log"))
    
    # 搜索配置
    search_depth: str = "basic"
    max_results: int = 5
    search_timeout: int = 30
    
    # 领域配置
    domains: dict = field(default_factory=lambda: {
        "架构师": ["AI", "云计算", "微服务", "Kubernetes", "LLM", "RAG"],
        "投资人": ["量化投资", "金融市场", "ESG", "因子模型"],
        "终身学习者": ["国学", "心理学", "学习方法"],
        "生活艺术家": ["葡萄酒", "摄影", "健身", "户外"]
    })


# 全局配置实例
settings = Settings()
