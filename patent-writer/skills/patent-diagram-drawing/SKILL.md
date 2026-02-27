---
name: patent-diagram-drawing
description: >
  This skill should be used when the user asks to "生成专利附图PNG", "画专利插图",
  "generate patent diagram images", "专利附图绘制", "draw patent figures",
  "patent illustration", "专利示意图", "附图生成",
  or when the /patent-writer:write-patent command reaches its diagram generation step.
  Generates CNIPA-compliant black-and-white engineering-style patent diagrams (PNG),
  including method flowcharts, apparatus block diagrams, system architecture diagrams,
  and hardware cross-section diagrams.
version: 1.0.0
---

# 专利附图 PNG 生成

通过 Google Gemini Image API 生成符合中国国家知识产权局（CNIPA）标准的纯黑白工程制图风格专利附图。

## 前置条件

### 环境变量

| 变量名 | 必需 | 说明 |
|--------|------|------|
| `GEMINI_API_KEY` | 是（优先） | Gemini API 密钥 |
| `GOOGLE_API_KEY` | 备选 | 当 `GEMINI_API_KEY` 未设置时使用 |
| `GEMINI_BASE_URL` | 否（优先） | 自定义 API 端点 |
| `GOOGLE_API_BASE_URL` | 备选 | 当 `GEMINI_BASE_URL` 未设置时使用 |

Python 依赖：`pip install google-genai`

## Workflow

### Step 1: 读取风格规范

Read `${CLAUDE_PLUGIN_ROOT}/skills/patent-diagram-drawing/references/patent-diagram-spec.md` to load CNIPA diagram standards (line weights, numbering formats, layout rules). Strictly follow all rules defined there.

### Step 2: 读取项目输入

Locate the project working directory (`output/temp_[uuid]/`). If invoked as /write-patent Step 2, reuse the directory from Step 1. Read:

- `04_content/description.md` — 具体实施方式全文
- `03_outline/structure_mapping.json` — 结构映射（图号、模块编号对应关系）

### Step 3: 确定附图列表

Based on description content and structure mapping, identify all diagrams to generate:

| 类型 | 触发条件 | 编号 |
|------|---------|------|
| 方法流程图 | 每个方法权利要求对应一张 | S101, S102... |
| 装置结构框图 | 每个装置权利要求对应一张 | 201, 202... |
| 系统架构图 | 涉及多组件交互时 | 301, 302... |
| 硬件截面图 | 涉及物理结构时 | 引出线编号 |

### Step 4: 逐一生成附图

Read `${CLAUDE_PLUGIN_ROOT}/skills/patent-diagram-drawing/references/prompt-templates.md` to get prompt templates. Select the template matching the diagram type (flowchart, apparatus, system, cross-section) and fill in placeholders from description.md and structure_mapping.json.

Create output directories, then execute for each diagram:

```bash
mkdir -p {PROJECT_DIR}/05_diagrams/{flowcharts,structural_diagrams,cross_sections}

GEMINI_API_KEY="${GEMINI_API_KEY:-$GOOGLE_API_KEY}" \
GEMINI_BASE_URL="${GEMINI_BASE_URL:-$GOOGLE_API_BASE_URL}" \
python3 "${CLAUDE_PLUGIN_ROOT}/skills/patent-diagram-drawing/scripts/generate.py" \
  "<PROMPT>" --ratio 3:4 -o "<OUTPUT_PATH>" --size 2K -v
```

- `<PROMPT>`: Full English prompt constructed from template with placeholders filled
- `<OUTPUT_PATH>`: Absolute path to output PNG (e.g., `05_diagrams/flowcharts/method_flow.png`)

If generation fails or quality check does not pass, retry up to 3 times with strengthened prompt constraints.

### Step 5: 质量验证

Verify each generated PNG against the checklist:

- [ ] **黑白性**：纯黑白，无灰度色块、无彩色元素
- [ ] **无图号**：图片中不包含底部"图N"编号
- [ ] **无外边框**：图片四周无黑色边框线
- [ ] **标记一致性**：步骤/模块编号与说明书具体实施方式一致
- [ ] **文字清晰度**：所有中文标注清晰可读
- [ ] **布局合理**：元素间距均匀，无重叠
- [ ] **文件可读**：PNG 文件完整且可打开

## Output Structure

```
05_diagrams/
├── flowcharts/           # 方法流程图
├── structural_diagrams/  # 装置结构框图
└── cross_sections/       # 硬件截面图
```

File naming: snake_case English, `.png` extension.

## Additional Resources

- **`references/patent-diagram-spec.md`** — CNIPA 附图绘制风格规范（线宽、编号、布局、文字等详细要求）
- **`references/prompt-templates.md`** — 4 种附图类型的 Gemini API prompt 模板及占位符说明

## Troubleshooting

| 问题 | 解决方案 |
|------|----------|
| `GEMINI_API_KEY not set` | 设置 `GEMINI_API_KEY` 或 `GOOGLE_API_KEY` |
| `No image generated` | 检查 prompt 长度和内容，重试 |
| 中文显示乱码 | 在 prompt 中要求 "Chinese text labels"，重试 |
| 出现彩色元素 | 加强黑白要求，重试（最多3次） |
| `Rate limit exceeded` | 等待 30-60 秒后重试 |
| `Content blocked` | 调整 prompt 措辞，避免敏感词 |
