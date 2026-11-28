---
title: uWise 审核结论（机器可核验项）
description: 对私库同步词条的确定性检查结论 · 不代表事实核验
---

# 审核结论（机器可核验项）

> 本次审核由脚本执行，只覆盖**可确定性验证的项目**。它没有逐篇核对事实、出处或原典，也没有做真实浏览器/Lighthouse 测试。

## 可核验结果

| 项目 | 结果 |
|---|---:|
| 词条总数 | 1891 |
| 状态分布 | [('active', 1485), ('unreviewed', 226), ('draft', 172), ('published', 8)] |
| 分类分布（前 6） | [('06-Cognitive-Psychology', 1112), ('concepts', 207), ('01-Finance-Investment', 145), ('07-Biology-Health', 122), ('02-AI-Architecture', 94), ('03-History-Society', 43)] |
| 未解析双链引用 | 3715 个（已在词条页保留标记） |
| 影子门禁可发布数 | 0 |
| 影子门禁阻断数 | 1891 |
| 敏感规则命中 | {'private_path': 1} |

## 已直接修复

- 公开页面与索引中的**私库路径已移除**，改为稳定来源 ID。
- 未解析双链不再退化为纯文本，改为带目标标记的 `<span class="uw-unresolved">`。
- 状态与分类已归一化；索引字段统一为 `entries`。
- Service Worker 合并为单一处理器并限定 `/uWise/` 路径；manifest 不再声明不存在的图标。
- CI 部署前增加 black / flake8 / mypy / pytest / `mkdocs build --strict` 硬门禁。

## 未声称完成

- **事实核验**：词条内容是否正确、引用是否可靠，仍未逐篇核对。
- **人工发布准入**：`visibility/publish/reviewed` 白名单尚未在私库源文件中设置，因此影子报告显示 0 篇可发布。
- **前端浏览器回归**：Instant Navigation 下的 JS 生命周期尚未做真实浏览器验证。

> 结论：可确定性验证的隐私、结构与工程门禁问题已修复；内容可信度仍需人工抽检，白名单生效前不应宣称「已审核」。
