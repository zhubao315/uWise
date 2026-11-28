---
title: "CAP定理"
description: "分布式系统的根本约束——一致性(Consistency)、可用性(Availability)、分区容错性(Partition tolerance)三者最多只能同时满足两个。"
---

# CAP定理

## 📌 核心定义

> 分布式系统的根本约束——一致性(Consistency)、可用性(Availability)、分区容错性(Partition tolerance)三者最多只能同时满足两个。

## 🎯 关键要点

- 一致性（C）：所有节点在同一时间看到相同的数据。读操作总是返回最近写入的值。
- 可用性（A）：每个请求都能收到一个非错误的响应，但不保证返回的是最新写入的值。
- 分区容错性（P）：系统在网络分区（节点之间通信中断）发生时仍能继续运行。
- CP系统：保证强一致性，但在网络分区时可能拒绝服务。典型如 ZooKeeper、etcd、HBase。
- AP系统：保证高可用性，但在网络分区时可能返回陈旧数据。典型如 Cassandra、DynamoDB、CouchDB。

## 📖 详细说明

### 概念解释
分布式系统的根本约束——一致性(Consistency)、可用性(Availability)、分区容错性(Partition tolerance)三者最多只能同时满足两个。
- **一致性（C）**：所有节点在同一时间看到相同的数据。读操作总是返回最近写入的值。
- **可用性（A）**：每个请求都能收到一个非错误的响应，但不保证返回的是最新写入的值。
- **分区容错性（P）**：系统在网络分区（节点之间通信中断）发生时仍能继续运行。


### 实际应用

- **CP系统**：保证强一致性，但在网络分区时可能拒绝服务。典型如 ZooKeeper、etcd、HBase。
- **AP系统**：保证高可用性，但在网络分区时可能返回陈旧数据。典型如 Cassandra、DynamoDB、CouchDB。

## 🔗 关联知识

- <span class="uw-unresolved" data-target="事件溯源" title="未解析的双链目标：事件溯源">事件溯源</span>
- [数据分区](../md-2e7f582f/)
- <span class="uw-unresolved" data-target="《设计数据密集型应用》-马丁·克莱普曼" title="未解析的双链目标：《设计数据密集型应用》-马丁·克莱普曼">《设计数据密集型应用》-马丁·克莱普曼</span>
- <span class="uw-unresolved" data-target="书单-2026年度" title="未解析的双链目标：书单-2026年度">书单-2026年度</span>

## 📊 元数据

| 属性 | 值 |
|------|-----|
| 分类代码 | 02-AI-Architecture |
| 知识类型 | concept |
| 精修时间 | 2026-06-17 11:53 |

---

## 调用示例

场景 1：判断「CAP定理」是否适用时，先复述其核心——分布式系统的根本约束——一致性(Consistency)、可用性(Availability)、分区容错性(Partition tolerance)三者最多只能同时满足两个。——再对照当前事实逐项核对。
场景 2：遇到与「CAP定理」相似的模糊情形，以要点「- 一致性（C）：所有节点在同一时间看到相同的数据。」为检查清单，避免只凭印象下结论。

## 边界约束

- 适用范围：本词条属 02-AI-Architecture 类 concept，用于理解与复盘「CAP定理」相关判断。
- 不适用：不替代该领域的专业判断；原始来源标注为「07-SOURCES/71-书籍/B5-科技科普/《设计数据密集型应用》-马丁·克莱普曼.md」。
- 前置条件：需先确认上文核心定义与关键要点，且信息来自可核实的一手材料。
- 风险提示：状态为「已确立」；记忆转述可能偏差，关键决策请回查一手来源。

---

<details>
<summary>来源与口径</summary>

- 来源：zhubao315/obsidian-vault@main:02-BUILD/23-uWise
- 来源标识：`e-7d17f0e032e3`（稳定 ID，不暴露私库路径）
- 状态：active · 分类：02-AI-Architecture
- 未解析双链：3 条（已保留目标标记）
- 本页由每周同步自动生成；内容来自个人笔记，未经逐条事实核验。

</details>
