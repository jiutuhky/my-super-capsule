---
description: "从技术交底书自动生成完整的中国专利申请文件：协调 7 个子代理生成专利文本，再调用附图绘制技能生成 PNG 专利附图"
disable-model-invocation: true
---

## Step 1: 生成专利文本

Invoke the patent-writer:writing-patent skill and follow it exactly as presented to you.

Wait for Step 1 to fully complete (06_final/complete_patent.md 已生成) before proceeding.

## Step 2: 生成专利附图 PNG

Invoke the patent-writer:patent-diagram-drawing skill and follow it exactly as presented to you.

The skill will guide you to read description.md and structure_mapping.json from the same project working directory, then generate PNG diagrams into 05_diagrams/.
