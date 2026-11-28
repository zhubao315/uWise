---
title: "uWise 保真度审计指南"
description: "知识词条质量保障机制 | 目标：≥2000 词条 · 保真度 ≥70%"
---

# uWise 保真度审计指南

> 知识词条质量保障机制 | 目标：≥2000 词条 · 保真度 ≥70%
> 当前状态：未审计 · 总量 1,879 篇 · **2026-09-23 新增第4维：非镜像（O-105/O-107）**

---

## 1. 保真度定义

**保真度 = Schema 完整性 + 引用可溯源 + 跨链接 ≥2 + 非镜像智慧**

| 维度 | 权重 | 通过标准 | 检测方法 |
|------|------|----------|----------|
| **Schema 完整性** | 35% | 必填字段齐全（title, created, tags, category, status） | YAML frontmatter 解析 |
| **引用可溯源** | 25% | `source` 指向 07-SOURCES/01-BRAIN 真本 + 正文 ≥1 真本 wikilink | 正则匹配 source + wikilink |
| **跨链接 ≥2** | 20% | 正文包含 ≥2 个 `wikilink` | wikilink 计数 |
| **非镜像（智慧提炼）** | 20% | 非书名/概念名镜像；非 expand_placeholders 占位句；含 `## 调用示例` + `## 边界约束` | title 对比真本 · 占位句 grep · fill_audit section |

### 合格判定

- 单词条保真度 ≥70 分 → **合格**
- 四项均不为 0 → **底线保真度**（任一维度为 0 则直接不合格）
- **镜像/占位句命中 → 直接不合格**（走 O-107 清理：删镜像或重写为智慧词条）
- 保真度 ≥90 → **优秀**（推荐为标杆词条，范例：[可消亡部件·架构演进·分布式取舍——《凤凰架构》三条智慧](../md-5ead4006/)）

---

## 2. 采样方法论

### 分层随机抽样（Stratified Random Sample）

**总体**：1,879 篇词条（`[PRIVATE_VAULT_PATH]`）

**目标样本**：200 篇（覆盖率 10.6%）

### 分层维度

#### 按 category 分布

| 分类 | 总量 | 占比 | 样本数 |
|------|------|------|--------|
| 06-Cognitive-Psychology | ~1,386 | 73.8% | 148 |
| 03-AI-Architecture | ~122 | 6.5% | 13 |
| 05-Biology-Health | ~111 | 5.9% | 12 |
| 01-Finance-Investment | ~94 | 5.0% | 10 |
| 07-Philosophy-Ethics | ~41 | 2.2% | 4 |
| 08-History-Social | ~34 | 1.8% | 4 |
| 04-Business-Management | ~34 | 1.8% | 4 |
| 99-General | ~36 | 1.9% | 4 |
| 09-Art-Culture | ~19 | 1.0% | 2 |
| **合计** | **1,879** | **100%** | **200** |

#### 按 status 分布（辅助层）

| 状态 | 预期占比 | 说明 |
|------|----------|------|
| draft | ~85% | 主体 |
| published | ~10% | 已发布 |
| archived | ~5% | 归档 |

### 抽样流程

```bash
# 1. 按 category 分组
ls 词条/*.md | xargs grep -l "category:" > /tmp/uwise_by_cat.txt

# 2. 每层随机抽取（Python）
python3 -c "
import random, os
# 读取所有词条并按 category 分组
# 每层按比例抽取 200 个
# 输出抽样清单到 reports/uwise_sample_YYYY-MM-DD.csv
"

# 3. 保存抽样结果
# reports/uwise_sample_YYYY-MM-DD.csv
```

---

## 3. 评分标准（0-100 分）

### 维度 1：Schema 完整性（40 分）

| 字段 | 分值 | 说明 |
|------|------|------|
| `title` | 8 | 必填 |
| `created` | 8 | 必填，YYYY-MM-DD 格式 |
| `tags` | 8 | 必填，至少 2 个标签 |
| `category` | 8 | 必填，分类代码 |
| `status` | 8 | 必填，draft/published/archived |

**加分项**（+5 分，上限 45 分）：
- `updated` 存在且 ≥ created：+2
- `aliases` 存在：+1
- `difficulty` 存在：+1
- `source` 存在：+1

### 维度 2：引用可溯源（30 分）

| 等级 | 分值 | 标准 |
|------|------|------|
| 完整引用 | 30 | source 字段存在 + 📚 参考资料 section ≥1 条 |
| 部分引用 | 20 | 仅 source 字段或仅参考资料 section |
| 弱引用 | 10 | 正文提及来源但无结构化引用 |
| 无引用 | 0 | 完全无来源信息 |

### 维度 3：跨链接 ≥2（30 分）

| wikilink 数 | 分值 |
|-------------|------|
| ≥5 | 30 |
| 3-4 | 25 |
| 2 | 20 |
| 1 | 10 |
| 0 | 0 |

**质量加分**（+5 分，上限 35 分）：
- 链接到不同 category 的词条：+3
- 包含 `<span class="uw-unresolved" data-target="` + `" title="未解析的双链目标：` + `">` + `</span>` 配对完整：+2

---

## 4. 评分汇总

| 等级 | 分数范围 | 标记 | 行动 |
|------|----------|------|------|
| **优秀** | 90-100 | 🟢 | 标杆词条，可作为模板 |
| **合格** | 70-89 | 🟡 | 无需立即行动 |
| **待改进** | 50-69 | 🟠 | 列入改进清单 |
| **不合格** | 0-49 | 🔴 | 优先修复 |

**KPI 目标**：
- 总词条 ≥2,000（当前 1,879，差 121 篇）
- 保真度 ≥70%（当前未知）

---

## 5. 修复工作流

### 低保真词条修复流程

```
识别 → 分类 → 优先级 → 执行 → 验证 → 闭环
```

### 步骤 1：识别

```bash
# 运行审计脚本
python3 09-REFERENCE/93-脚本/uWise_fidelity_audit.py

# 输出：reports/uwise_fidelity_report_YYYY-MM-DD.md
# 输出：reports/uwise_fidelity_report_YYYY-MM-DD.csv
```

### 步骤 2：分类修复

| 问题类型 | 修复方法 | 预估耗时/篇 |
|----------|----------|-------------|
| 缺失 frontmatter 字段 | 补全 YAML | 2 min |
| 缺失来源 | 添加 source 或参考资料 | 5 min |
| wikilink <2 | 添加关联词条 | 3 min |
| 内容为空骨架 | 删除或补充 | 15 min |

### 步骤 3：优先级排序

1. **P0**：frontmatter 完全缺失（Schema 0 分）
2. **P1**：保真度 <50 分
3. **P2**：保真度 50-69 分
4. **P3**：仅 wikilink 不足

### 步骤 4：执行修复

```bash
# 批量修复 frontmatter（安全）
python3 09-REFERENCE/93-脚本/uWise_fidelity_fix.py --fix schema

# 批量添加来源标记（需人工确认）
python3 09-REFERENCE/93-脚本/uWise_fidelity_fix.py --fix source --dry-run

# 批量添加跨链接（自动，需人工审核）
python3 09-REFERENCE/93-脚本/uWise_fidelity_fix.py --fix links
```

### 步骤 5：验证

```bash
# 重新运行审计
python3 09-REFERENCE/93-脚本/uWise_fidelity_audit.py --sample 200

# 确认保真度 ≥70%
```

---

## 6. 与现有脚本集成

### 已有脚本

| 脚本 | 功能 | 路径 |
|------|------|------|
| `uWise_fill_audit.py` | 补全完整性（调用示例 + 边界约束） | `09-REFERENCE/93-脚本/` |

### 新增脚本（本指南配套）

| 脚本 | 功能 | 状态 |
|------|------|------|
| `uWise_fidelity_audit.py` | 保真度三维评分 | 待创建 |
| `uWise_fidelity_fix.py` | 批量修复 | 待创建 |
| `uWise_fidelity_report.py` | 生成报告 | 待创建 |

### 集成方式

```bash
# P0 审计流水线（已有）
quality_gate.sh
├── uSkill_upgrade_audit.py
├── uWise_fill_audit.py      ← 补全完整性
├── tag_audit.py
└── uWise_fidelity_audit.py  ← 新增：保真度审计（建议加入）
```

---

## 7. 月度节奏

### 每月执行

| 时间 | 动作 | 产出 |
|------|------|------|
| 每月 1 日 | 运行全量审计 | `reports/uwise_fidelity_report_MM.md` |
| 每月 1-3 日 | 分析报告，生成修复清单 | `reports/uwise_fix_queue_MM.csv` |
| 每月 3-10 日 | 执行 P0/P1 修复 | 修复 commit |
| 每月 15 日 | 抽样验证 | 修复确认 |
| 每月 25 日 | 更新统计，更新本文件 | KPI 更新 |

### 月度报告模板

```markdown
# uWise 保真度月报 — YYYY-MM

| 指标 | 本月 | 上月 | 变化 |
|------|------|------|------|
| 总词条数 | | | |
| 保真度 ≥70% | | | |
| Schema 完整率 | | | |
| 引用覆盖率 | | | |
| 平均跨链接数 | | | |

## 修复统计
- P0 修复：X 篇
- P1 修复：X 篇
- P2 修复：X 篇

## 下月重点
- 
```

---

## 8. 关联文档

- <span class="uw-unresolved" data-target="2026年度目标 AI Co-Evolution-自主进化的人生操作系统" title="未解析的双链目标：2026年度目标 AI Co-Evolution-自主进化的人生操作系统">2026年度目标 AI Co-Evolution-自主进化的人生操作系统</span> — 年度目标，uWise 是三大项目之一
- <span class="uw-unresolved" data-target="2026-07~09 Q3 OKR" title="未解析的双链目标：2026-07~09 Q3 OKR">2026-07~09 Q3 OKR</span> — Q3 目标，保真度审计是关键 KR
- <span class="uw-unresolved" data-target="2026-风险登记簿" title="未解析的双链目标：2026-风险登记簿">2026-风险登记簿</span> — 风险登记簿，uWise 质量风险
- `uwise_fill_audit` — 补全完整性审计（已有脚本）
- [词条标准化规范](../02-fc20d065/) — 词条模板与字段规范
- <span class="uw-unresolved" data-target="诊断分析报告" title="未解析的双链目标：诊断分析报告">诊断分析报告</span> — 全库健康度

---

## 9. 附录：审计脚本接口规范

### 输入

```
输入目录：[PRIVATE_VAULT_PATH]
抽样数量：--sample N（默认 200）
修复模式：--fix schema|source|links|all
试运行：  --dry-run（仅输出，不修改）
```

### 输出

```
reports/uwise_fidelity_report_YYYY-MM-DD.md   ← 人类可读报告
reports/uwise_fidelity_report_YYYY-MM-DD.csv  ← 机器可读数据
reports/uwise_fidelity_sample_YYYY-MM-DD.csv  ← 抽样清单
```

### 退出码

| 码 | 含义 |
|----|------|
| 0 | 保真度 ≥70% |
| 1 | 保真度 <70%（需修复） |
| 2 | 脚本错误 |

---

*本指南由 MiMoCode 生成 | 2026-07-24 | 维护者：宝哥*

---

<details>
<summary>来源与口径</summary>

- 来源：个人知识库（每周同步，未逐条事实核验）
- 来源标识：`e-d3f00d53d2fb`（稳定 ID，不暴露私库路径）
- 状态：unreviewed · 分类：uncategorized
- 未解析双链：5 条（已保留目标标记）
- 本页由每周同步自动生成；内容来自个人笔记，未经逐条事实核验。

</details>
