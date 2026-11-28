---
title: "反向传播"
description: "反向传播（Backpropagation）是训练深度神经网络的核心算法，由鲁梅尔哈特（Rumelhart）、辛顿（Hinton）和威廉姆斯（Williams）在1986年推广，被认为是深度学习革命的基石。"
---

# 反向传播

## 📌 核心定义

> 反向传播（Backpropagation）是训练深度神经网络的核心算法，由鲁梅尔哈特（Rumelhart）、辛顿（Hinton）和威廉姆斯（Williams）在1986年推广，被认为是深度学习革命的基石。

## 🎯 关键要点

- ReLU激活函数：缓解梯度消失问题。
- 残差连接（Residual Connection）：ResNet的核心创新，让梯度可以"跳跃"传播。
- 梯度裁剪：限制梯度的最大值，防止爆炸。
- 批归一化（Batch Normalization）：稳定每层的输入分布。

## 📖 详细说明

### 概念解释
反向传播（Backpropagation）是训练深度神经网络的核心算法，由鲁梅尔哈特（Rumelhart）、辛顿（Hinton）和威廉姆斯（Williams）在1986年推广，被认为是深度学习革命的基石。
反向传播的本质是**链式法则的系统应用**——通过计算损失函数对网络中每个参数的梯度，来确定每个参数应该如何调整以减少预测误差。

整个过程分两步：

### 1. 前向传播（Forward Pass）
输入数据从第一层流向最后一层，逐层计算，最终产生预测结果。同时，每一层的中间结果被保存下来。

### 2. 反向传播（Backward Pass）
从输出层开始，利用链式法则逐层计算损失函数对每个参数的偏导数（梯度）。误差信号像波浪一样从后向前传播。

$$\frac{\partial L}{\partial w_{ij}} = \frac{\partial L}{\partial a_j} \cdot \frac{\partial a_j}{\partial z_j} \cdot \frac{\partial z_j}{\partial w_{ij}}$$

其中 $L$ 是损失函数，$a_j$ 是激活值，$z_j$ 是加权和，$w_{ij}$ 是权重参数。

### 1. 前向传播（Forward Pass）

### 2. 反向传播（Backward Pass）


## 🔗 关联知识

- <span class="uw-unresolved" data-target="表征学习" title="未解析的双链目标：表征学习">表征学习</span>
- [生成对抗网络](../md-7c896d1d/)
- <span class="uw-unresolved" data-target="《深度学习》-伊恩·古德费洛" title="未解析的双链目标：《深度学习》-伊恩·古德费洛">《深度学习》-伊恩·古德费洛</span>
- <span class="uw-unresolved" data-target="书单-2026年度" title="未解析的双链目标：书单-2026年度">书单-2026年度</span>

## 💡 个人理解

反向传播的本质是**链式法则的系统应用**——通过计算损失函数对网络中每个参数的梯度，来确定每个参数应该如何调整以减少预测误差。

## 📊 元数据

| 属性 | 值 |
|------|-----|
| 分类代码 | 06-Cognitive-Psychology |
| 知识类型 | concept |
| 精修时间 | 2026-06-17 11:53 |

---

## 调用示例

场景 1：判断「反向传播」是否适用时，先复述其核心——反向传播（Backpropagation）是训练深度神经网络的核心算法，由鲁梅尔哈特（Rumelhart）、辛顿（Hinton）和威廉姆斯（Williams）在1986年推广，被认为是深度学习革命的基石。——再对照当前事实逐项核对。
场景 2：遇到与「反向传播」相似的模糊情形，以要点「- ReLU激活函数：缓解梯度消失问题。」为检查清单，避免只凭印象下结论。

## 边界约束

- 适用范围：本词条属 06-Cognitive-Psychology 类 concept，用于理解与复盘「反向传播」相关判断。
- 不适用：不替代该领域的专业判断；原始来源标注为「07-SOURCES/71-书籍/B5-科技科普/《深度学习》-伊恩·古德费洛.md」。
- 前置条件：需先确认上文核心定义与关键要点，且信息来自可核实的一手材料。
- 风险提示：状态为「已确立」；记忆转述可能偏差，关键决策请回查一手来源。

---

<details>
<summary>来源与口径</summary>

- 来源：个人知识库（每周同步，未逐条事实核验）
- 来源标识：`e-79ccdb39061b`（稳定 ID，不暴露私库路径）
- 状态：active · 分类：06-Cognitive-Psychology
- 未解析双链：3 条（已保留目标标记）
- 本页由每周同步自动生成；内容来自个人笔记，未经逐条事实核验。

</details>
