---
title: "项目总览"
description: "|------|-----|"
---

# 项目总览

## 项目信息

| 属性 | 值 |
|------|-----|
| **项目名称** | uWise 知识百科 |
| **创建时间** | 2026-05-08 |
| **项目状态** | ✅ 全部完成 |
| **词条总数** | 1,944 |
| **目标词条数** | 6,000+ |
| **知识来源** | 01-BRAIN 思维层（2,477 源文件） |

## 项目愿景

将个人 6,000+ 笔记结构化为 **Agent 可读的知识百科**，形成可检索、可关联、可推理的知识体系。

## 执行阶段

### Phase 0: 框架搭建 ✅
- 建立 9 大分类体系（MECE 原则）
- 制定词条标准化规范（YAML + Markdown 模板）
- 创建核心词条索引（200 个规划词条）
- 创建知识分类体系文档

### Phase 1: 骨架生成 ✅
- 扫描 01-BRAIN 全部源文件（2,477 条）
- 创建 `scripts/batch_generate.py` 批量生成
- 分类映射：维度标签 → uWise 分类代码
- 产出：2,494 篇词条骨架

### Phase 2: 质量精修 ✅
- 创建 `scripts/enrich_phase2.py` + `enrich_phase2_v2.py`
- 从 01-BRAIN 源文件提取关键要点（85% 已填充）
- 提取概念解释（80% 已填充）
- 去除重复 section（核心要素/实际应用冗余）
- 清理模板残留文本（18 篇）
- 补充交叉链接（72% 词条有 >1 链接）
- 移动 7 篇散落词条到 `词条/` 目录

### Phase 3: 产品化 ✅
- 知识图谱可视化（交互式 HTML + 静态 SVG）
- REST API 服务（8 个端点，零依赖）
- API 完整文档

## 质量指标

| 指标 | Phase 1 后 | Phase 2 后 | 最终 |
|------|-----------|-----------|------|
| 关键要点填充率 | 1% | 85% | 85% |
| 概念解释填充率 | 1% | 80% | 80% |
| 多链接率(>1) | 55% | 72% | 72% |
| 模板残留 | 18 | 0 | 0 |
| 体积合格(>800B) | 100% | 100% | 100% |

## 产出清单

### 文档
| 文件 | 说明 |
|------|------|
| `README.md` | 项目入口 |
| `项目总览.md` | 本文件 |
| `知识分类体系.md` | 9 大分类 + 标签映射 |
| `词条标准化规范.md` | 词条模板与字段规范 |
| `核心词条索引.md` | 词条统计与查找 |
| `API文档.md` | REST API 完整文档 |
| `Scaffolding/uWise-Scaffolding-Spec.md` | 脚手架规范 |

### 数据
| 文件 | 说明 |
|------|------|
| `词条/*.md` | 1,944 篇知识词条 |
| `scripts/knowledge_graph_data.json` | 图谱原始数据 |

### 工具
| 文件 | 说明 |
|------|------|
| `scripts/api_server.py` | REST API 服务（`python3 scripts/api_server.py`） |
| `scripts/knowledge_graph.html` | 交互式知识图谱（浏览器打开） |
| `scripts/knowledge_graph.svg` | 静态全景图 |

### 脚本
| 文件 | 阶段 | 说明 |
|------|------|------|
| `scripts/batch_generate.py` | Phase 1 | 从 01-BRAIN 批量生成词条骨架 |
| `scripts/enrich_entries.py` | Phase 2 | 初始精修 |
| `scripts/enrich_entries_v2.py` | Phase 2 | 增强精修 |
| `scripts/enrich_v3.py` | Phase 2 | 进一步精修 |
| `scripts/enrich_final.py` | Phase 2 | 最终精修 |
| `scripts/enrich_phase2.py` | Phase 2 | 去重+链接补充 |
| `scripts/enrich_phase2_v2.py` | Phase 2 | 全量待补充修复 |

## 与 01-BRAIN 的关系

```
01-BRAIN (思维层，2,477 源文件)
    ↓ batch_generate.py
uWise 词条骨架 (2,494)
    ↓ enrich_phase2_v2.py
精修后的知识百科 (2,501)
    ↓ scripts/api_server.py
REST API + 知识图谱
```

| 维度 | 01-BRAIN | uWise |
|------|----------|-------|
| 定位 | 个人思维资产 | 结构化知识百科 |
| 受众 | 自己 | 机器可读 + 他人可查 |
| 格式 | 灵活自由 | 严格模板 |
| 更新 | 随时 | 批量 + 定期精修 |

---

*最后更新：2026-06-17 · Phase 3 全部完成*

---
**相关笔记**：[化性起伪](../md-e4dab78b/) [金钱心理学](../md-7713aa4a/)

---

<details>
<summary>来源与口径</summary>

- 来源：个人知识库（每周同步，未逐条事实核验）
- 来源标识：`e-64adb8a1e30a`（稳定 ID，不暴露私库路径）
- 状态：unreviewed · 分类：uncategorized
- 未解析双链：0 条（已保留目标标记）
- 本页由每周同步自动生成；内容来自个人笔记，未经逐条事实核验。

</details>
