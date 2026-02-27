---
description: "从技术交底书自动生成完整的中国专利申请文件：协调 6 个子代理生成专利文本，调用附图绘制技能生成 PNG 专利附图，最终合并为 Word 专利申请文件"
disable-model-invocation: true
---

## Step 1: 生成专利文本

Invoke the patent-writer:writing-patent skill and follow it exactly as presented to you.

Wait for Step 1 to fully complete (04_content/description.md 已生成) before proceeding.

## Step 2: 生成专利附图 PNG

Invoke the patent-writer:patent-diagram-drawing skill and follow it exactly as presented to you.

The skill will guide you to read description.md and structure_mapping.json from the same project working directory, then generate PNG diagrams into 05_diagrams/.

Wait for Step 2 to fully complete (05_diagrams/ 已生成附图) before proceeding.

## Step 3: 合并生成 Word 专利文件

Use the patent-writer:docx-merger agent to merge all content and diagrams into the final Word patent application file.

The agent will read abstract.md, claims.md, description.md and diagrams from 05_diagrams/, then generate 06_final/patent_application.docx.
