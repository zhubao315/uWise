#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AI摘要生成模块"""

from typing import Optional
from .logger import logger
from .config import settings


def generate_summary(
    content: str, api_key: Optional[str] = None, max_length: int = 200, model: str = "gpt-3.5-turbo"
) -> str:
    """
    使用OpenAI生成知识摘要

    Args:
        content: 原始内容
        api_key: OpenAI API密钥
        max_length: 摘要最大长度
        model: 使用的模型

    Returns:
        生成的摘要文本
    """
    if not api_key:
        logger.warning("未配置OpenAI API密钥，使用原始内容")
        return content[:max_length]

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "你是一个知识整理助手，将搜索结果整理成简洁、准确的中文摘要。",
                },
                {
                    "role": "user",
                    "content": f"请将以下内容整理成简洁的中文摘要（{max_length}字以内）：\n\n{content}",
                },
            ],
            max_tokens=max_length * 2,
            temperature=0.7,
        )

        summary = response.choices[0].message.content
        logger.info("摘要生成成功")
        return summary

    except ImportError:
        logger.error("未安装openai库，请运行: pip install openai")
        return content[:max_length]
    except Exception as e:
        logger.error(f"生成摘要失败: {e}")
        return content[:max_length]


def generate_multi_summary(
    contents: list, api_key: Optional[str] = None, max_length: int = 300
) -> str:
    """
    生成多个内容的综合摘要

    Args:
        contents: 内容列表
        api_key: OpenAI API密钥
        max_length: 摘要最大长度

    Returns:
        综合摘要文本
    """
    if not contents:
        return ""

    combined_content = "\n\n".join(contents)
    return generate_summary(combined_content, api_key, max_length)
