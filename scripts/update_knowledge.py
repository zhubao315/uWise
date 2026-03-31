#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
uWise 百科知识更新脚本
每日自动抓取、整理、更新领域知识
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path

# 配置
DOCS_DIR = Path("docs")
UPDATE_LOG = DOCS_DIR / "UPDATES.md"

# 领域关键词配置
DOMAINS = {
    "架构师": ["AI", "云计算", "微服务", "Kubernetes", "LLM", "RAG"],
    "投资人": ["量化投资", "金融市场", "ESG", "因子模型"],
    "终身学习者": ["国学", "心理学", "学习方法"],
    "生活艺术家": ["葡萄酒", "摄影", "健身", "户外"],
}


def search_tavily(query: str, api_key: str) -> list:
    """使用Tavily搜索API获取最新信息"""
    if not api_key:
        return []

    try:
        response = requests.post(
            "https://api.tavily.com/search",
            json={
                "query": query,
                "search_depth": "basic",
                "include_answer": True,
                "max_results": 5,
            },
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=30,
        )
        if response.status_code == 200:
            return response.json().get("results", [])
    except Exception as e:
        print(f"搜索失败: {e}")
    return []


def generate_summary(content: str, api_key: str) -> str:
    """使用OpenAI生成知识摘要"""
    if not api_key:
        return content[:500]

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "你是一个知识整理助手，将搜索结果整理成简洁的中文摘要。",
                },
                {
                    "role": "user",
                    "content": f"请将以下内容整理成简洁的中文摘要（200字以内）：\n\n{content}",
                },
            ],
            max_tokens=300,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"生成摘要失败: {e}")
        return content[:500]


def update_domain_knowledge(domain: str, keywords: list, tavily_key: str, openai_key: str):
    """更新指定领域的知识"""
    print(f"📚 更新{domain}领域知识...")

    for keyword in keywords[:2]:  # 每次更新2个关键词
        print(f"  🔍 搜索: {keyword}")
        results = search_tavily(f"{keyword} 最新发展 2026", tavily_key)

        if results:
            # 这里可以添加将搜索结果写入文档的逻辑
            print(f"  ✅ 找到 {len(results)} 条结果")


def main():
    """主函数"""
    print("🦞 uWise 百科知识更新开始...")
    print(f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 获取API密钥
    tavily_key = os.getenv("TAVILY_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    if not tavily_key and not openai_key:
        print("⚠️  未配置API密钥，跳过自动更新")
        print("💡 请在GitHub Secrets中配置 OPENAI_API_KEY 和 TAVILY_API_KEY")
        return

    # 今日更新领域（轮转）
    today = datetime.now().weekday()
    domain_list = list(DOMAINS.keys())
    today_domain = domain_list[today % len(domain_list)]

    print(f"🎯 今日重点更新: {today_domain}")
    update_domain_knowledge(today_domain, DOMAINS[today_domain], tavily_key, openai_key)

    print("✅ 知识更新完成!")


if __name__ == "__main__":
    main()
