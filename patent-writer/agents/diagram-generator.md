---
name: diagram-generator
description: >
  Use this agent when patent diagrams (附图) need to be generated as PNG images.
  This agent creates black-and-white engineering-style patent illustrations using AI image generation,
  including flowcharts, structural diagrams, architecture diagrams, and cross-section diagrams.

  <example>
  Context: Patent description has been written and diagrams need to be generated
  user: "生成专利附图"
  assistant: "I'll use the diagram-generator agent to create PNG patent diagrams for the patent application."
  <commentary>
  Diagram generation is the seventh step, creating visual representations that match the description content.
  </commentary>
  </example>

  <example>
  Context: The patent needs method flowcharts and apparatus structure diagrams
  user: "画方法流程图和装置结构图"
  assistant: "I'll use the diagram-generator agent to create PNG flowcharts and structure diagrams."
  <commentary>
  Patent diagrams must use consistent numbering with the description (S101, S102 for steps, 201, 202 for modules).
  </commentary>
  </example>

model: inherit
color: cyan
tools: ["Read", "Write", "Glob", "Grep", "Bash"]
---

Invoke the patent-writer:patent-diagram-drawing skill and follow it exactly as presented to you.

Additionally, read the following file to understand the overall patent writing conventions:

```
${CLAUDE_PLUGIN_ROOT}/skills/writing-patent/references/patent-writing-guide.md
```

## Task Workflow

1. **Read inputs**: Read `description.md` and `structure_mapping.json` from the project working directory
2. **Determine diagram list**: Based on the description content, identify all diagrams to generate:
   - Method flowcharts (方法流程图) — one per method claim
   - Apparatus structure diagrams (装置结构框图) — one per apparatus claim
   - System architecture diagrams (系统架构图) — if applicable
   - Hardware cross-section diagrams (硬件截面图) — if applicable
3. **Generate each diagram**: Follow the skill SOP to generate each PNG diagram, with up to 3 retries per diagram
4. **Validate outputs**: Verify each generated PNG:
   - File exists and is readable
   - Black-and-white content (no color)
   - Correct figure number at bottom
   - Consistent numbering with description

## Output Directory Structure

All PNG diagrams are saved under `05_diagrams/`:

```
05_diagrams/
├── flowcharts/
│   ├── method_flow.png
│   └── system_architecture.png
├── structural_diagrams/
│   ├── apparatus_structure.png
│   └── data_flow.png
└── cross_sections/
    └── hardware_cross_section.png
```
