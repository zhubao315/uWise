#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""日志模块测试"""

import pytest
import logging
from pathlib import Path
from scripts.logger import setup_logger


def test_logger_creation(tmp_path):
    """测试日志记录器创建"""
    log_file = tmp_path / "test.log"
    logger = setup_logger("test", log_file=log_file)

    assert isinstance(logger, logging.Logger)
    assert logger.name == "test"


def test_logger_output(tmp_path, caplog):
    """测试日志输出"""
    log_file = tmp_path / "test.log"
    logger = setup_logger("test", log_file=log_file)

    with caplog.at_level(logging.INFO):
        logger.info("Test message")

    assert "Test message" in caplog.text


def test_logger_file_creation(tmp_path):
    """测试日志文件创建"""
    log_file = tmp_path / "test.log"
    logger = setup_logger("test", log_file=log_file)

    logger.info("Test message")

    assert log_file.exists()
    content = log_file.read_text(encoding="utf-8")
    assert "Test message" in content
