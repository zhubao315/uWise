#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""搜索模块"""

import asyncio
from typing import List, Dict, Optional
import aiohttp
from .logger import logger
from .config import settings


async def search_tavily_async(
    query: str, api_key: str, search_depth: str = "basic", max_results: int = 5, timeout: int = 30
) -> List[Dict]:
    """
    异步使用Tavily搜索API获取最新信息

    Args:
        query: 搜索查询字符串
        api_key: Tavily API密钥
        search_depth: 搜索深度（basic/advanced）
        max_results: 最大结果数
        timeout: 超时时间（秒）

    Returns:
        搜索结果列表
    """
    if not api_key:
        logger.warning("未配置Tavily API密钥")
        return []

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.tavily.com/search",
                json={
                    "query": query,
                    "search_depth": search_depth,
                    "include_answer": True,
                    "max_results": max_results,
                },
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=aiohttp.ClientTimeout(total=timeout),
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    results = data.get("results", [])
                    logger.info(f"搜索成功: {query}, 找到 {len(results)} 条结果")
                    return results
                else:
                    error_text = await response.text()
                    logger.error(
                        f"搜索失败: {query}, 状态码: {response.status}, 错误: {error_text}"
                    )
                    return []
    except asyncio.TimeoutError:
        logger.error(f"搜索超时: {query}")
        return []
    except Exception as e:
        logger.error(f"搜索异常: {query}, 错误: {e}")
        return []


def search_tavily(query: str, api_key: str) -> List[Dict]:
    """
    同步搜索接口（向后兼容）

    Args:
        query: 搜索查询字符串
        api_key: Tavily API密钥

    Returns:
        搜索结果列表
    """
    return asyncio.run(
        search_tavily_async(
            query=query,
            api_key=api_key,
            search_depth=settings.search_depth,
            max_results=settings.max_results,
            timeout=settings.search_timeout,
        )
    )


async def batch_search(
    queries: List[str],
    api_key: str,
    search_depth: str = "basic",
    max_results: int = 5,
    timeout: int = 30,
) -> Dict[str, List[Dict]]:
    """
    批量异步搜索

    Args:
        queries: 搜索查询列表
        api_key: Tavily API密钥
        search_depth: 搜索深度
        max_results: 最大结果数
        timeout: 超时时间

    Returns:
        查询到结果的映射字典
    """
    if not queries:
        return {}

    logger.info(f"开始批量搜索: {len(queries)} 个查询")

    tasks = [
        search_tavily_async(query, api_key, search_depth, max_results, timeout) for query in queries
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    # 过滤异常结果
    search_results = {}
    for query, result in zip(queries, results):
        if isinstance(result, Exception):
            logger.error(f"搜索失败: {query}, 错误: {result}")
        elif result:
            search_results[query] = result

    logger.info(f"批量搜索完成: {len(search_results)}/{len(queries)} 成功")
    return search_results
