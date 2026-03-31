#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""uWise 百科知识更新主程序"""

import asyncio
from datetime import datetime
from typing import Dict, List
from .config import settings
from .logger import logger
from .search import batch_search
from .summary import generate_summary
from .updater import updater
from .cache import cache


class KnowledgeUpdater:
    """知识更新器主类"""

    def __init__(self):
        """初始化知识更新器"""
        self.settings = settings
        self.updater = updater
        self.cache = cache

    async def update_domain(
        self, domain: str, keywords: List[str], keywords_per_update: int = 2
    ) -> None:
        """
        更新指定领域的知识

        Args:
            domain: 领域名称
            keywords: 关键词列表
            keywords_per_update: 每次更新的关键词数量
        """
        logger.info(f"📚 开始更新 {domain} 领域知识...")

        # 选择要更新的关键词
        selected_keywords = keywords[:keywords_per_update]

        # 构建搜索查询
        queries = [f"{keyword} 最新发展 2026" for keyword in selected_keywords]

        # 执行批量搜索
        search_results = await batch_search(
            queries=queries,
            api_key=self.settings.tavily_api_key or "",
            search_depth=self.settings.search_depth,
            max_results=self.settings.max_results,
            timeout=self.settings.search_timeout,
        )

        # 处理搜索结果
        for keyword, results in search_results.items():
            logger.info(f"  🔍 {keyword}: 找到 {len(results)} 条结果")

            # 生成摘要
            if results and self.settings.openai_api_key:
                combined_content = "\n\n".join([result.get("content", "") for result in results])
                summary = generate_summary(
                    combined_content, self.settings.openai_api_key, max_length=200
                )
            else:
                summary = None

            # 记录更新
            self.updater.add_update_entry(
                domain=domain, keyword=keyword, results=results, summary=summary
            )

        logger.info(f"✅ {domain} 领域更新完成")

    def get_today_domain(self) -> str:
        """
        获取今日需要更新的领域

        Returns:
            领域名称
        """
        domain_list = list(self.settings.domains.keys())
        today_index = datetime.now().weekday()
        return domain_list[today_index % len(domain_list)]

    async def run(self) -> None:
        """执行知识更新"""
        logger.info("=" * 50)
        logger.info("🦞 uWise 百科知识更新开始")
        logger.info(f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 50)

        # 检查API密钥
        if not self.settings.tavily_api_key and not self.settings.openai_api_key:
            logger.warning("⚠️  未配置API密钥，跳过自动更新")
            logger.info("💡 请在GitHub Secrets中配置 OPENAI_API_KEY 和 TAVILY_API_KEY")
            return

        # 清理过期缓存
        if self.settings.cache_enabled:
            self.cache.clear_expired()

        # 获取今日需要更新的领域
        today_domain = self.get_today_domain()
        logger.info(f"🎯 今日重点更新: {today_domain}")

        # 执行更新
        await self.update_domain(
            domain=today_domain, keywords=self.settings.domains[today_domain], keywords_per_update=2
        )

        logger.info("=" * 50)
        logger.info("✅ 知识更新完成!")
        logger.info("=" * 50)


async def main():
    """主函数"""
    updater = KnowledgeUpdater()
    await updater.run()


if __name__ == "__main__":
    asyncio.run(main())
