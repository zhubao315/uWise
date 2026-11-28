---
title: "🧠 uWise 知识百科"
description: "结构化知识词条系统 | 从 01-BRAIN 思维层提炼的机器可读知识库"
---

# 🧠 uWise 知识百科

> 结构化知识词条系统 | 从 01-BRAIN 思维层提炼的机器可读知识库
> **最后更新**: 2026-09-18 | **总量**: 2,166 篇 | **状态**: Phase 4 内容质量修复中

> 🧹 **2026-09-18 结构修复**：`uwise_split_concat.py` 拆分 60 个多词条拼接文件，恢复 145 个被埋没词条；并清理 4 个 YAML/空 tags 异常。剩余待办：1,266 篇含通用废话模板需逐篇重写，2,120 篇缺「调用示例/边界约束」。

## 项目状态

| Phase | 状态 | 产出 |
|-------|------|------|
| Phase 0: 框架搭建 | ✅ | 分类体系、规范、索引 |
| Phase 1: 骨架生成 | ✅ | 2,494 篇词条（从 01-BRAIN 提取） |
| Phase 2: 质量精修 | ✅ | 85% 要点填充、80% 概念填充 |
| Phase 3: 产品化 | ✅ | 知识图谱 + REST API |

## 目录结构

```
23-uWise/
├── README.md                    ← 本文件
├── 项目总览.md                  ← 项目概述与进度
├── 知识分类体系.md              ← 9 大分类 + 标签映射
├── 词条标准化规范.md            ← 词条模板与字段规范
├── 核心词条索引.md              ← 词条统计与查找方法
├── API文档.md                   ← REST API 完整文档
│
├── Scaffolding/
│   └── uWise-Scaffolding-Spec.md  ← 脚手架规范
│
├── 词条/                        ← 1,944 篇知识词条
│
├── scripts/                     ← 构建与精修脚本
│   ├── batch_generate.py        ← Phase 1: 批量生成
│   ├── enrich_phase2.py         ← Phase 2: 去重+链接
│   ├── enrich_phase2_v2.py      ← Phase 2: 全量修复
│   └── ...
│
├── api_server.py                ← REST API 服务
├── knowledge_graph.html         ← 交互式知识图谱
├── knowledge_graph.svg          ← 静态全景图
└── knowledge_graph_data.json    ← 图谱原始数据
```

## 分类分布

| 分类 | 词条数 | 占比 |
|------|--------|------|
| 认知心理 | 1,846 | 73.8% |
| AI架构 | 163 | 6.5% |
| 生物健康 | 148 | 5.9% |
| 金融投研 | 125 | 5.0% |
| 哲学伦理 | 56 | 2.2% |
| 历史社科 | 46 | 1.8% |
| 商业管理 | 45 | 1.8% |
| 通用 | 47 | 1.9% |
| 艺术文化 | 25 | 1.0% |

## 快速使用

### 搜索
```bash
curl "http://localhost:8900/api/search?q=投资"
```

### 获取词条
```bash
curl "http://localhost:8900/api/entries/安全边际"
```

### 查看关联
```bash
curl "http://localhost:8900/api/entries/安全边际/neighbors?depth=2"
```

### 启动服务
```bash
python3 api_server.py --host 0.0.0.0 --port 8900
```

### 打开知识图谱
```
浏览器打开 knowledge_graph.html
```

---
**相关笔记**：[饮要少但要好](../md-f9764ab9/) [垄断与竞争](../md-d6b23ad8/)

---

<details>
<summary>来源与口径</summary>

- 来源：`zhubao315/obsidian-vault@main:02-BUILD/23-uWise`
- 私库路径：`README.md`
- 原始状态：未标注 · 分类：未标注
- 断链别名（无目标，保留为文本）：0 条
- 本页由每周同步自动生成；内容来自个人笔记，未经逐条核验。

</details>
