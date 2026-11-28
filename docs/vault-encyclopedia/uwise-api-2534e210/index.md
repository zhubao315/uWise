---
title: "uWise 知识百科 API 文档"
description: "updated: 2026-09-30"
---

# uWise 知识百科 API 文档

updated: 2026-09-30
---
# uWise 知识百科 API 文档

> REST API for the uWise Knowledge Encyclopedia
> Base URL: `http://localhost:8900`

## 快速开始

```bash
# 启动服务
python3 api_server.py --port 8900

# 健康检查
curl http://localhost:8900/api/health

# 搜索
curl "http://localhost:8900/api/search?q=投资"

# 获取词条
curl "http://localhost:8900/api/entries/安全边际"
```

## 端点一览

| Method | Path | 说明 |
|--------|------|------|
| GET | `/api/health` | 健康检查 |
| GET | `/api/stats` | 知识库统计 |
| GET | `/api/categories` | 分类列表 |
| GET | `/api/entries` | 词条列表（分页+筛选） |
| GET | `/api/entries/<id>` | 词条详情 |
| GET | `/api/entries/<id>/neighbors` | 关联词条 |
| GET | `/api/search` | 全文搜索 |
| GET | `/api/graph` | 图谱数据 |

---

## 端点详情

### GET /api/health

健康检查。

**Response:**
```json
{
  "status": "ok",
  "entries": 2494
}
```

---

### GET /api/stats

知识库统计信息。

```json
{
  "total_entries": 2494,
  "total_edges": 3750,
  "connected_nodes": 2330,
  "categories": {
    "06-Cognitive-Psychology": 1839,
    "02-AI-Architecture": 163,
    "01-Finance-Investment": 125
  },
  "source_types": {
    "concept": 1420,
    "insight": 365,
    "model": 351,
    "framework": 175,
    "principle": 166
  },
  "avg_links": 2.6
}
```

---

### GET /api/categories

列出所有分类及词条数。

```json
{
  "categories": [
    {
      "code": "06-Cognitive-Psychology",
      "name": "认知心理",
      "count": 1839,
      "sample_entries": ["元认知", "心流", "第一性原理"]
    }
  ],
  "total": 9
}
```

---

### GET /api/entries

分页列出词条，支持分类筛选和排序。

**Query Parameters:**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `page` | int | 1 | 页码 |
| `page_size` | int | 20 | 每页数量（最大100） |
| `category` | string | - | 分类代码筛选 |
| `source_type` | string | - | 来源类型筛选 |
| `sort` | string | id | 排序：`id`/`links`/`size` |

```json
{
  "total": 125,
  "page": 1,
  "page_size": 20,
  "total_pages": 7,
  "entries": [
    {
      "id": "安全边际",
      "title": "安全边际",
      "category": "01-Finance-Investment",
      "category_name": "金融投研",
      "source_type": "concept",
      "core_definition": "安全边际是价值投资的核心概念...",
      "link_count": 35,
      "status": "draft"
    }
  ]
}
```

**示例：**
```
GET /api/entries?category=01-Finance-Investment&sort=links&page_size=10
GET /api/entries?source_type=model&page=2
```

---

### GET /api/entries/<id>

获取单个词条的完整信息。

**Path Parameters:**

| 参数 | 类型 | 说明 |
|------|------|------|
| `id` | string | 词条ID（文件名，不含.md） |

```json
{
  "source": "01-BRAIN/11-概念/安全边际.md",
  "tags": ["维度/投资", "类型/概念"],
  "created": "2026-06-05",
  "core_definition": "...",
  "key_points": ["要点1", "要点2"],
  "links": ["价值投资", "护城河", "风险管理"],
  "neighbors": [
    {"id": "价值投资", "title": "价值投资", "category": "01-Finance-Investment"}
  ]
}
```

---

### GET /api/entries/<id>/neighbors

获取词条的关联网络。


| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `depth` | int | 1 | 搜索深度（1=直接邻居，2=二度关联） |
| `limit` | int | 50 | 返回数量上限 |

```json
{
  "center": "安全边际",
  "depth": 1,
  "total": 35,
    {"id": "价值投资", "title": "价值投资", "category": "01-Finance-Investment", "depth": 1},
    {"id": "护城河", "title": "护城河", "category": "01-Finance-Investment", "depth": 1}
  ]
}
```

---

### GET /api/search

全文搜索词条。


| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `q` | string | (必填) | 搜索关键词 |
| `limit` | int | 20 | 返回数量上限 |

**搜索策略（多层加权）：**
1. 标题精确匹配 → 权重 10
2. 核心定义匹配 → 权重 5
3. 关键要点匹配 → 权重 3
4. 分词匹配 → 权重 1
5. 模糊字符包含 → 权重 2

```json
{
  "query": "投资",
  "total": 184,
  "results": [
    {
      "id": "产业投资视角",
      "title": "产业投资视角",
      "link_count": 3,
      "score": 20.0
    }
  ]
}
```

---

### GET /api/graph

获取知识图谱数据（用于可视化）。


| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `category` | string | - | 按分类筛选 |
| `limit` | int | 500 | 节点数上限 |

```json
{
  "nodes": [
    {"id": "安全边际", "label": "安全边际", "category": "01-Finance-Investment", "color": "#f59e0b", "size": 3200}
  ],
  "edges": [
    {"from": "安全边际", "to": "价值投资", "weight": 3}
  ],
  "total_nodes": 500,
  "total_edges": 890
}
```

---

## 分类代码

| 代码 | 中文名 |
|------|--------|
| `01-Finance-Investment` | 金融投研 |
| `02-AI-Architecture` | AI架构 |
| `03-History-Society` | 历史社科 |
| `04-Business-Management` | 商业管理 |
| `05-Philosophy-Ethics` | 哲学伦理 |
| `06-Cognitive-Psychology` | 认知心理 |
| `07-Biology-Health` | 生物健康 |
| `08-Arts-Culture` | 艺术文化 |
| `00-General` | 通用 |

## 来源类型

| 类型 | 说明 |
|------|------|
| `concept` | 概念定义 |
| `model` | 运作模型 |
| `framework` | 分析框架 |
| `principle` | 行动原则 |
| `insight` | 个人洞察 |

---

*API v1.0 · 2026-06-17*

---
**相关笔记**：[挺经](../md-c8b53168/) [极度透明](../md-8072377c/)

---

<details>
<summary>来源与口径</summary>

- 来源：个人知识库（每周同步，未逐条事实核验）
- 来源标识：`e-2534e21087cb`（稳定 ID，不暴露私库路径）
- 状态：unreviewed · 分类：uncategorized
- 未解析双链：0 条（已保留目标标记）
- 本页由每周同步自动生成；内容来自个人笔记，未经逐条事实核验。

</details>
