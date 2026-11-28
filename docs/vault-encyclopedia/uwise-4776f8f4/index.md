---
title: "🏗️ uWise 脚手架规范"
description: "uWise 是从 01-BRAIN 思维层提炼的结构化知识百科，面向机器+他人消费。"
---

# 🏗️ uWise 脚手架规范

## 1. 项目定位

uWise 是从 01-BRAIN 思维层提炼的**结构化知识百科**，面向机器+他人消费。

### 1.1 与 01-BRAIN 的关系

| 维度 | 01-BRAIN (思维层) | uWise (产出层) |
|------|-------------------|----------------|
| **定位** | 个人思维资产 | 结构化知识百科 |
| **受众** | 自己 | 机器可读 + 他人可查 |
| **格式** | 灵活自由 | 严格模板 |
| **标签** | `类型/洞察` 等 | + `项目/uWise` |
| **链接** | 自由关联 | 结构化关联 |
| **更新频率** | 随时 | 批量 + 定期精修 |

### 1.2 知识流转

```
01-BRAIN 洞察/概念/模型
    ↓ (提炼 + 结构化)
uWise 词条
    ↓ (产品化)
外部输出 (API/文档/文章)
```

## 2. 数据来源

| 来源层 | 目录 | 条目数 | 用途 |
|--------|------|--------|------|
| 思维层 | `01-BRAIN/11-概念` | ~1,420 | 基础概念定义 |
| | `01-BRAIN/12-模型` | ~351 | 运作机制模型 |
| | `01-BRAIN/13-框架` | ~175 | 分析行动框架 |
| | `01-BRAIN/14-原则` | ~166 | 行动准则 |
| | `01-BRAIN/15-洞察` | ~365 | 个人悟道 |
| **合计** | | **~2,477** | |

## 3. 词条分类体系

| 分类代码 | 中文名 | 英文名 | 当前条数 |
|----------|--------|--------|----------|
| 01-Finance-Investment | 金融投研 | Finance & Investment | 125 |
| 02-AI-Architecture | AI架构 | AI Architecture | 163 |
| 03-History-Society | 历史社科 | History & Society | 46 |
| 04-Business-Management | 商业管理 | Business & Management | 45 |
| 05-Philosophy-Ethics | 哲学伦理 | Philosophy & Ethics | 51 |
| 06-Cognitive-Psychology | 认知心理 | Cognitive & Psychology | 1,839 |
| 07-Biology-Health | 生物健康 | Biology & Health | 148 |
| 08-Arts-Culture | 艺术文化 | Arts & Culture | 25 |
| 00-General | 通用 | General | 35 |
| **合计** | | | **2,494** |

### 标签映射规则

| 01-BRAIN 标签 | uWise 分类代码 |
|---------------|---------------|
| `维度/架构 | 02-AI-Architecture |
| `维度/投资 | 01-Finance-Investment |
| `维度/学习 | 06-Cognitive-Psychology |
| `维度/生活 | 07-Biology-Health |
| `维度/管理 | 04-Business-Management |
| `维度/哲学 | 05-Philosophy-Ethics |
| `维度/心理 | 06-Cognitive-Psychology |
| `维度/健康 | 07-Biology-Health |
| `维度/科技 | 02-AI-Architecture |
| `维度/文学 | 08-Arts-Culture |
| `维度/历史 | 03-History-Society |
| `维度/技能 | 00-General |
| `维度/人物 | 03-History-Society |
| `维度/成长 | 06-Cognitive-Psychology |
| `维度/艺术 | 08-Arts-Culture |

## 4. 词条模板

```yaml
---
title: "词条名称"
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - "维度/学习"
  - "类型/概念"
  - "项目/uWise"
source: "01-BRAIN/xxx/xxx.md"
source_type: "concept|model|framework|principle|insight"
category: "分类代码"
status: "draft|published"
---
```

### 内容结构

```markdown
# 词条名称

## 📌 核心定义
> 1-2 句话定义

## 🎯 关键要点
- 要点1
- 要点2

## 📖 详细说明
### 概念解释
### 实际应用

## 🔗 关联知识
- <span class="uw-unresolved" data-target="相关词条" title="未解析的双链目标：相关词条">相关词条</span>

## 📚 参考资料
- 来源：`01-BRAIN/xxx/xxx.md`

## 💡 个人理解

## 📊 元数据
```

## 5. 批量生成流程

### Phase 1: 骨架生成 ✅
```
01-BRAIN 源条目 (2,477)
    ↓ (batch_generate.py)
uWise 词条骨架
    ↓ (自动分类 + 标签映射)
2,494 篇词条
```

### Phase 2: 质量精修 ✅
```
词条骨架 (2,494)
    ↓ (enrich_phase2_v2.py)
├── 填充关键要点 (85%)
├── 填充概念解释 (80%)
├── 去除重复 section
├── 清理模板残留
├── 补充交叉链接 (72%)
└── 体积验证 (100% >800B)
```

### Phase 3: 产品化 ✅
- [x] REST API 服务（8 个端点，零依赖）→ `api_server.py`
- [x] 知识图谱可视化 → `knowledge_graph.html` + `.svg`
- [x] API 文档 → `API文档.md`

## 6. 质量指标

| 指标 | Phase 1 后 | Phase 2 后 | 目标 |
|------|-----------|-----------|------|
| 关键要点填充率 | 1% | 85% | 95% |
| 概念解释填充率 | 1% | 80% | 90% |
| 多链接率(>1) | 55% | 72% | 85% |
| 模板残留 | 18 | 0 | 0 |
| 体积合格(>800B) | 100% | 100% | 100% |

---

*最后更新：2026-06-17 · Phase 3 全部完成*

---

<details>
<summary>来源与口径</summary>

- 来源：个人知识库（每周同步，未逐条事实核验）
- 来源标识：`e-4776f8f4494a`（稳定 ID，不暴露私库路径）
- 状态：active · 分类：uncategorized
- 未解析双链：1 条（已保留目标标记）
- 本页由每周同步自动生成；内容来自个人笔记，未经逐条事实核验。

</details>
