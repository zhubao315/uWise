---
title: "Serverless"
description: "Serverless（无服务器架构）是一种云计算执行模型，开发者无需管理服务器，只需编写函数代码，由云平台自动管理扩缩容和资源分配。"
---

# Serverless

Serverless（无服务器架构）是一种云计算执行模型，开发者无需管理服务器，只需编写函数代码，由云平台自动管理扩缩容和资源分配。

## 核心特征

| 特征 | 说明 |
|:---|:---|
| **按需执行** | 函数只在被触发时运行，空闲时不计费 |
| **自动扩缩** | 平台根据请求量自动伸缩实例 |
| **无状态** | 每次调用独立，状态存外部存储 |
| **事件驱动** | 通过 HTTP/消息队列/定时器触发 |

## 主流产品

- AWS Lambda / Azure Functions / Google Cloud Functions
- Cloudflare Workers（边缘计算）
- Vercel Serverless Functions / Netlify Functions

## 适用边界

**适合**：API 端点、定时任务、事件处理、Webhook
**不适合**：长连接、有状态服务、冷启动敏感场景

## 相关笔记

- [Netlify](../netlify-md-5422b89a/)
- Vercel
- CloudFlare

## 关联
- Serverless计算

---

## 调用示例

场景 1：判断「Serverless」是否适用时，先复述其核心——「Serverless」的定义见上文——再对照当前事实逐项核对。
场景 2：遇到与「Serverless」相似的模糊情形，以要点「围绕「Serverless」建立判断框架」为检查清单，避免只凭印象下结论。

## 边界约束

- 适用范围：本词条属 未分类 类 词条，用于理解与复盘「Serverless」相关判断。
- 不适用：不替代该领域的专业判断；原始来源标注为「01-BRAIN」。
- 前置条件：需先确认上文核心定义与关键要点，且信息来自可核实的一手材料。
- 风险提示：状态为「未标注」；记忆转述可能偏差，关键决策请回查一手来源。

---

<details>
<summary>来源与口径</summary>

- 来源：`zhubao315/obsidian-vault@main:02-BUILD/23-uWise`
- 私库路径：`词条/Serverless.md`
- 原始状态：未标注 · 分类：01-BRAIN
- 断链别名（无目标，保留为文本）：2 条
- 本页由每周同步自动生成；内容来自个人笔记，未经逐条核验。

</details>
