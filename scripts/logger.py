#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""日志管理模块"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional
from .config import settings


def setup_logger(
    name: str,
    log_file: Optional[Path] = None,
    level: Optional[int] = None,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    设置日志记录器
    
    Args:
        name: 日志记录器名称
        log_file: 日志文件路径（可选）
        level: 日志级别
        format_string: 日志格式字符串
    
    Returns:
        配置好的日志记录器
    """
    logger = logging.getLogger(name)
    
    # 避免重复添加handler
    if logger.handlers:
        return logger
    
    # 设置日志级别
    log_level = level or getattr(logging, settings.log_level.upper())
    logger.setLevel(log_level)
    
    # 日志格式
    if format_string is None:
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        date_format = '%Y-%m-%d %H:%M:%S'
    else:
        date_format = None
    
    formatter = logging.Formatter(format_string, datefmt=date_format)
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 文件处理器
    if log_file or settings.log_file:
        file_path = log_file or settings.log_file
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(file_path, encoding='utf-8')
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


# 创建默认日志记录器
logger = setup_logger("uWise")
