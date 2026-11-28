---
title: "语音AI集成"
description: "将语音识别（ASR）、语音合成（TTS）、语音理解集成到应用中的技术方案。"
---

# 语音AI集成

> 将语音识别（ASR）、语音合成（TTS）、语音理解集成到应用中的技术方案。

## 技术栈

| 技术 | 代表 |
|------|------|
| **ASR（语音识别）** | Whisper, Paraformer, Azure Speech |
| **TTS（语音合成）** | VITS, Bark, ElevenLabs |
| **NLU（语义理解）** | LLM + Prompt |
| **对话管理** | 有限状态机 / LLM 驱动 |

## 集成流程

```
音频输入 → ASR 转文本 → LLM 理解 → 生成回复 → TTS 输出音频
```

## 应用场景

- **智能客服**：语音交互式客服
- **语音助手**：日程/查询/控制
- **内容创作**：播客/有声书制作
- **辅助功能**：无障碍交互

## 相关

- <span class="uw-unresolved" data-target="LLM应用开发" title="未解析的双链目标：LLM应用开发">LLM应用开发</span>
- <span class="uw-unresolved" data-target="语音识别" title="未解析的双链目标：语音识别">语音识别</span>
- <span class="uw-unresolved" data-target="《自然语言处理综论》-Daniel Jurafsky" title="未解析的双链目标：《自然语言处理综论》-Daniel Jurafsky">《自然语言处理综论》-Daniel Jurafsky</span>

---

## 调用示例

场景 1：判断「语音AI集成」是否适用时，先复述其核心——「语音AI集成」的定义见上文——再对照当前事实逐项核对。
场景 2：遇到与「语音AI集成」相似的模糊情形，以要点「围绕「语音AI集成」建立判断框架」为检查清单，避免只凭印象下结论。

## 边界约束

- 适用范围：本词条属 未分类 类 词条，用于理解与复盘「语音AI集成」相关判断。
- 不适用：不替代该领域的专业判断；原始来源标注为「还原自 01-BRAIN（2026-09-17 归档迁移）」。
- 前置条件：需先确认上文核心定义与关键要点，且信息来自可核实的一手材料。
- 风险提示：状态为「未标注」；记忆转述可能偏差，关键决策请回查一手来源。

---

<details>
<summary>来源与口径</summary>

- 来源：zhubao315/obsidian-vault@main:02-BUILD/23-uWise
- 来源标识：`e-534b7c217f03`（稳定 ID，不暴露私库路径）
- 状态：unreviewed · 分类：concepts
- 未解析双链：3 条（已保留目标标记）
- 本页由每周同步自动生成；内容来自个人笔记，未经逐条事实核验。

</details>
