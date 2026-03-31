#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""缓存管理模块"""

import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Any
from .logger import logger
from .config import settings


class CacheManager:
    """缓存管理器"""
    
    def __init__(
        self,
        cache_dir: Optional[Path] = None,
        ttl_hours: int = 24
    ):
        """
        初始化缓存管理器
        
        Args:
            cache_dir: 缓存目录路径
            ttl_hours: 缓存有效期（小时）
        """
        self.cache_dir = cache_dir or settings.cache_dir
        self.ttl = timedelta(hours=ttl_hours)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"缓存管理器初始化完成: {self.cache_dir}")
    
    def _get_cache_key(self, key: str) -> str:
        """生成缓存键的MD5哈希"""
        return hashlib.md5(key.encode('utf-8')).hexdigest()
    
    def _get_cache_file(self, key: str) -> Path:
        """获取缓存文件路径"""
        return self.cache_dir / f"{self._get_cache_key(key)}.json"
    
    def get(self, key: str) -> Optional[Any]:
        """
        获取缓存数据
        
        Args:
            key: 缓存键
        
        Returns:
            缓存数据，如果不存在或过期则返回None
        """
        cache_file = self._get_cache_file(key)
        
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            cached_time = datetime.fromisoformat(data['timestamp'])
            
            # 检查是否过期
            if datetime.now() - cached_time > self.ttl:
                cache_file.unlink()
                logger.debug(f"缓存已过期: {key}")
                return None
            
            logger.debug(f"缓存命中: {key}")
            return data['content']
            
        except Exception as e:
            logger.error(f"读取缓存失败: {key}, 错误: {e}")
            return None
    
    def set(self, key: str, value: Any) -> None:
        """
        设置缓存数据
        
        Args:
            key: 缓存键
            value: 缓存值
        """
        cache_file = self._get_cache_file(key)
        
        try:
            data = {
                'timestamp': datetime.now().isoformat(),
                'content': value
            }
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.debug(f"缓存已保存: {key}")
            
        except Exception as e:
            logger.error(f"保存缓存失败: {key}, 错误: {e}")
    
    def clear(self) -> None:
        """清空所有缓存"""
        try:
            for cache_file in self.cache_dir.glob("*.json"):
                cache_file.unlink()
            logger.info("所有缓存已清空")
        except Exception as e:
            logger.error(f"清空缓存失败: {e}")
    
    def clear_expired(self) -> None:
        """清空过期的缓存"""
        try:
            now = datetime.now()
            expired_count = 0
            
            for cache_file in self.cache_dir.glob("*.json"):
                try:
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    cached_time = datetime.fromisoformat(data['timestamp'])
                    if now - cached_time > self.ttl:
                        cache_file.unlink()
                        expired_count += 1
                        
                except Exception:
                    # 如果文件损坏，直接删除
                    cache_file.unlink()
                    expired_count += 1
            
            logger.info(f"清空了 {expired_count} 个过期缓存")
            
        except Exception as e:
            logger.error(f"清空过期缓存失败: {e}")


# 全局缓存管理器实例
cache = CacheManager(
    cache_dir=settings.cache_dir,
    ttl_hours=settings.cache_ttl_hours
)
