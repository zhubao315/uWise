# 📈 量化投资

> **数据驱动的投资决策** - 用算法和数学模型优化投资

## 领域概述

量化投资是将数学模型、统计分析和计算机算法应用于投资决策的方法，是技术背景投资人的核心优势领域。

## 核心技术

### 因子模型
- **价值因子**：PE、PB、EV/EBITDA
- **动量因子**：价格动量、收益动量
- **质量因子**：ROE、资产负债率
- **规模因子**：市值规模

### 算法交易
- 趋势跟踪
- 均值回归
- 统计套利
- 高频交易

### 风险模型
- VaR (Value at Risk)
- CVaR (Conditional VaR)
- 最大回撤控制
- 相关性分析

## 开发框架

### 回测系统
```python
# 伪代码示例
for date in trading_dates:
    signals = generate_signals(data)
    positions = optimize_portfolio(signals)
    execute_trades(positions)
    record_performance()
```

### 技术栈
- **数据源**：Tushare、Wind、Yahoo Finance
- **分析工具**：Pandas、NumPy、SciPy
- **机器学习**：Scikit-learn、TensorFlow
- **回测框架**：Backtrader、Zipline

## 来自个人技能库的真实技能

> 从 570 个已公开同步的个人技能中，按「分类 + 标题关键词」筛选，共 12 条（去重后最多展示 12 条）。这些技能是 Draft 资产并标记 `untrusted`；脚本不会自动执行。

| 技能 | 分类 | 入口 |
|---|---|---|
| [investment bond allocation strategy](https://zhubao315.github.io/uSkill/skills-from-vault/s6/uskill-investment-bond-allocation-strategy/SKILL/) | `s6` | [原文](https://zhubao315.github.io/uSkill/skills-from-vault/s6/uskill-investment-bond-allocation-strategy/references/source/) |
| [定投策略优化](https://zhubao315.github.io/uSkill/skills-from-vault/s6/uskill-investment-dca-strategy-opt/SKILL/) | `s6` | [原文](https://zhubao315.github.io/uSkill/skills-from-vault/s6/uskill-investment-dca-strategy-opt/references/source/) |
| [investment dca strategy optimization](https://zhubao315.github.io/uSkill/skills-from-vault/s6/uskill-investment-dca-strategy-optimization/SKILL/) | `s6` | [原文](https://zhubao315.github.io/uSkill/skills-from-vault/s6/uskill-investment-dca-strategy-optimization/references/source/) |
| [股债配置策略](https://zhubao315.github.io/uSkill/skills-from-vault/s6/uskill-investment-equity-bond-allocation/SKILL/) | `s6` | [原文](https://zhubao315.github.io/uSkill/skills-from-vault/s6/uskill-investment-equity-bond-allocation/references/source/) |
| [财报解读](https://zhubao315.github.io/uSkill/skills-from-vault/s6/uskill-investment-financial-analysis/SKILL/) | `s6` | [原文](https://zhubao315.github.io/uSkill/skills-from-vault/s6/uskill-investment-financial-analysis/references/source/) |
| [investment graham safety margin](https://zhubao315.github.io/uSkill/skills-from-vault/s6/uskill-investment-graham-safety-margin/SKILL/) | `s6` | [原文](https://zhubao315.github.io/uSkill/skills-from-vault/s6/uskill-investment-graham-safety-margin/references/source/) |
| [investment im report writing](https://zhubao315.github.io/uSkill/skills-from-vault/s6/uskill-investment-im-report-writing/SKILL/) | `s6` | [原文](https://zhubao315.github.io/uSkill/skills-from-vault/s6/uskill-investment-im-report-writing/references/source/) |
| [行业分析](https://zhubao315.github.io/uSkill/skills-from-vault/s6/uskill-investment-industry-analysis/SKILL/) | `s6` | [原文](https://zhubao315.github.io/uSkill/skills-from-vault/s6/uskill-investment-industry-analysis/references/source/) |
| [investment industry rotation analysis](https://zhubao315.github.io/uSkill/skills-from-vault/s6/uskill-investment-industry-rotation-analysis/SKILL/) | `s6` | [原文](https://zhubao315.github.io/uSkill/skills-from-vault/s6/uskill-investment-industry-rotation-analysis/references/source/) |
| [盘中行情监控](https://zhubao315.github.io/uSkill/skills-from-vault/s6/uskill-investment-intraday-market-monitor/SKILL/) | `s6` | [原文](https://zhubao315.github.io/uSkill/skills-from-vault/s6/uskill-investment-intraday-market-monitor/references/source/) |
| [IP管理与知识资产运营](https://zhubao315.github.io/uSkill/skills-from-vault/s6/uskill-investment-ip-162473/SKILL/) | `s6` | [原文](https://zhubao315.github.io/uSkill/skills-from-vault/s6/uskill-investment-ip-162473/references/source/) |
| [investment options basic strategies](https://zhubao315.github.io/uSkill/skills-from-vault/s6/uskill-investment-options-basic-strategies/SKILL/) | `s6` | [原文](https://zhubao315.github.io/uSkill/skills-from-vault/s6/uskill-investment-options-basic-strategies/references/source/) |

## 相关书稿与笔记

- [《投资的纪律》](https://zhubao315.github.io/books/investment-discipline/) · [公开笔记](https://zhubao315.github.io/uRead/read/book-investment-discipline/)

## 来自私库词条库的相关词条

> 私库词条库每周同步，条目未经逐条核验；只列出名称匹配的词条。

- [定投策略优化](../vault-encyclopedia/md-39519407/)
- [股债配置策略](../vault-encyclopedia/md-0bf127fb/)
- [肌肉内分泌学：抗阻力训练对神经营养因子BDNF的激活效应](../vault-encyclopedia/bdnf-md-d57cff4c/)

## 边界与口径

- 技能来自私有 Obsidian 仓库 `02-BUILD/22-uSkill` 的公开同步，每周自动更新；原文逐字保留。
- 本页只做索引，不对技能质量做评级；未匹配到技能时如实留空，不补写内容。
- 书稿与笔记链接指向各站点实时页面；引用前请核对原文与核验日期。
