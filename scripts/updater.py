#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""文档更新模块"""

from pathlib import Path
from datetime import datetime
from typing import List, Dict
from .logger import logger
from .config import settings


class DocumentUpdater:
    """文档更新器"""

    def __init__(self, docs_dir: Path = None):
        """
        初始化文档更新器

        Args:
            docs_dir: 文档目录路径
        """
        self.docs_dir = docs_dir or settings.docs_dir
        self.update_log = settings.update_log

    def add_update_entry(
        self, domain: str, keyword: str, results: List[Dict], summary: str = None
    ) -> None:
        """
        添加更新记录到更新日志

        Args:
            domain: 领域名称
            keyword: 关键词
            results: 搜索结果
            summary: 摘要内容
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        entry = f"""
## {timestamp} - {domain}

### 关键词: {keyword}

### 搜索结果: {len(results)} 条

"""

        if summary:
            entry += f"### 摘要\n\n{summary}\n\n"

        entry += "---\n\n"

        # 写入更新日志
        self.update_log.parent.mkdir(parents=True, exist_ok=True)

        if self.update_log.exists():
            content = self.update_log.read_text(encoding="utf-8")
            content = entry + content
        else:
            content = f"# 知识更新日志\n\n{entry}"

        self.update_log.write_text(content, encoding="utf-8")
        logger.info(f"更新日志已保存: {domain} - {keyword}")

    def update_domain_document(self, domain: str, keyword: str, new_content: str) -> None:
        """
        更新领域文档

        Args:
            domain: 领域名称
            keyword: 关键词
            new_content: 新内容
        """
        # 查找对应的文档文件
        # 这里可以添加更复杂的逻辑来定位和更新文档
        logger.info(f"文档更新: {domain} - {keyword}")

    def get_domain_file_path(self, domain: str) -> Path:
        """
        获取领域文档文件路径

        Args:
            domain: 领域名称

        Returns:
            文档文件路径
        """
        # 将领域名称映射到文件路径
        domain_files = {
            "架构师": "core-identity/architect.md",
            "投资人": "core-identity/investor.md",
            "终身学习者": "core-identity/lifelong-learner.md",
            "生活艺术家": "core-identity/life-artist.md",
        }

        file_path = domain_files.get(domain)
        if file_path:
            return self.docs_dir / file_path

        # 如果没有找到，返回None
        return None


# 全局文档更新器实例
updater = DocumentUpdater()
