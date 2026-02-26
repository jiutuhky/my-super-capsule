---
name: patent-diagram-drawing
description: >
  触发词："生成专利附图PNG"、"画专利插图"、"generate patent diagram images"、
  "专利附图绘制"。使用 Gemini Image API 生成符合 CNIPA 标准的黑白专利附图。
version: 1.0.0
---

# 专利附图 PNG 生成技能

本技能使用内置脚本调用 Google Gemini 3 Pro Image API，生成符合中国国家知识产权局（CNIPA）标准的纯黑白工程制图风格专利附图（PNG 格式）。

---

## 前置条件

### 环境变量

| 变量名 | 必需 | 说明 |
|--------|------|------|
| `GEMINI_API_KEY` | 是（优先） | Gemini API 密钥 |
| `GOOGLE_API_KEY` | 备选 | 当 `GEMINI_API_KEY` 未设置时使用 |
| `GEMINI_BASE_URL` | 否（优先） | 自定义 API 端点 |
| `GOOGLE_API_BASE_URL` | 备选 | 当 `GEMINI_BASE_URL` 未设置时使用 |

### Python 依赖

```bash
pip install google-genai
```

---

## 绘制规范

在编写 Prompt 之前，**必须先阅读**附图绘制风格规范文档：

```
${CLAUDE_PLUGIN_ROOT}/skills/patent-diagram-drawing/references/patent-diagram-spec.md
```

该文档定义了线条粗细、编号格式、布局规则等所有细节要求。

---

## 生成命令模板

```bash
GEMINI_API_KEY="${GEMINI_API_KEY:-$GOOGLE_API_KEY}" \
GEMINI_BASE_URL="${GEMINI_BASE_URL:-$GOOGLE_API_BASE_URL}" \
python3 "${CLAUDE_PLUGIN_ROOT}/skills/patent-diagram-drawing/scripts/generate.py" \
  "<PROMPT>" --ratio 3:4 -o "<OUTPUT_PATH>" --size 2K -v
```

- `<PROMPT>`：根据下方模板构造的完整 prompt 文本
- `<OUTPUT_PATH>`：输出 PNG 文件的完整路径
- `--ratio 3:4`：专利附图推荐比例（A4 竖版）
- `--size 2K`：2K 分辨率，确保文字清晰
- `-v`：详细输出模式，便于调试

---

## 附图 Prompt 模板

### 5.1 方法流程图

```
Generate a black-and-white patent-style method flowchart diagram for a Chinese patent application (CNIPA standard).

Title at bottom center: "图{N}"

Steps (top to bottom flow):
- S{X}01: {步骤1名称}
- S{X}02: {步骤2名称}
- S{X}03: {步骤3名称}
...

Requirements:
- Pure black and white, NO grayscale, NO colors, NO shadows
- Engineering drawing style with clean lines
- Rounded rectangles for start/end, rectangles for process steps, diamonds for decisions
- Step labels in Chinese with step numbers (S{X}01, S{X}02...)
- Arrows connecting steps from top to bottom
- Decision branches labeled "是" (yes) and "否" (no)
- Line weights: outer border 2pt, step boxes 1.5pt, arrows 1pt
- Sufficient white space and margins
- Professional patent illustration quality
```

### 5.2 装置结构框图

```
Generate a black-and-white patent-style apparatus structure block diagram for a Chinese patent application (CNIPA standard).

Title at bottom center: "图{N}"

Apparatus: {装置名称} {总编号如200}
Modules inside dashed boundary box:
- {模块1名称} {编号如201}
- {模块2名称} {编号如202}
- {模块3名称} {编号如203}
...

Data flow connections:
- {模块1} -> {模块2}: {数据描述}
- {模块2} -> {模块3}: {数据描述}
...

Requirements:
- Pure black and white, NO grayscale, NO colors, NO shadows
- Engineering drawing style with clean lines
- Dashed rectangle as apparatus boundary with title and number (e.g., "{装置名称} 200")
- Solid rectangles for each functional module with name and number
- Arrows showing data/control flow direction
- All labels in Chinese
- Line weights: boundary 2pt dashed, modules 1.5pt solid, arrows 1pt
- Modules evenly distributed within boundary
- Professional patent illustration quality
```

### 5.3 系统架构图

```
Generate a black-and-white patent-style system architecture diagram for a Chinese patent application (CNIPA standard).

Title at bottom center: "图{N}"

Layers (top to bottom):
- Client layer: {组件1} {编号}, {组件2} {编号}
- Service layer: {组件3} {编号}, {组件4} {编号}
- Data layer: {组件5} {编号}, {组件6} {编号}

Communication:
- {组件1} -> {组件3}: {协议/数据}
- {组件3} -> {组件5}: {协议/数据}
...

Requirements:
- Pure black and white, NO grayscale, NO colors, NO shadows
- Engineering drawing style with clean lines
- Layered layout with dashed boxes grouping each layer
- Rectangles for system components with Chinese labels and numbers
- Arrows with protocol/data type annotations
- Line weights: layer boundaries 2pt dashed, components 1.5pt solid, arrows 1pt
- Horizontal arrangement within layers, vertical connections between layers
- Professional patent illustration quality
```

### 5.4 硬件截面图

```
Generate a black-and-white patent-style hardware cross-section diagram for a Chinese patent application (CNIPA standard).

Title at bottom center: "图{N}"

Structure (describe the hardware):
{硬件结构的详细描述}

Components with reference numbers:
- {部件1名称}: {编号}
- {部件2名称}: {编号}
...

Requirements:
- Pure black and white, NO grayscale, NO colors, NO shadows
- Engineering drawing style with clean precise lines
- 45-degree cross-hatching for sectioned solid parts
- Leader lines with Arabic numeral reference numbers
- Leader lines must not cross each other
- Numbers increment top-to-bottom, left-to-right
- Line weights: outer contour 2pt, internal structure 1.5pt, leader lines 1pt, hatching 0.5pt
- Dashed lines for hidden internal structures
- Professional patent illustration quality
```

---

## 输出文件命名规范

所有附图 PNG 文件保存在项目的 `05_diagrams/` 子目录下：

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

- 文件名使用 snake_case 英文命名
- 扩展名统一为 `.png`
- 按附图类型分子目录存放

---

## 质量检查清单

每张生成的附图必须通过以下检查：

- [ ] **黑白性**：图像为纯黑白，无灰度色块、无彩色元素
- [ ] **图号正确**：底部居中的"图N"编号与说明书附图说明一致
- [ ] **标记一致性**：步骤编号（S101等）或模块编号（201等）与说明书具体实施方式一致
- [ ] **文字清晰度**：所有中文标注清晰可读，无模糊或截断
- [ ] **布局合理**：元素间距均匀，无重叠、无拥挤
- [ ] **文件可读**：PNG 文件可正常打开且内容完整

---

## 故障排除

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| `GEMINI_API_KEY not set` | 环境变量未配置 | 设置 `GEMINI_API_KEY` 或 `GOOGLE_API_KEY` |
| `No image generated` | API 未返回图片 | 检查 prompt 是否过短或不合规，重试 |
| 中文显示为方块/乱码 | 模型渲染问题 | 在 prompt 中明确要求"Chinese text labels"，重试 |
| 图中出现彩色元素 | prompt 约束不够强 | 加强 prompt 中的黑白要求，重试（最多3次） |
| `Rate limit exceeded` | API 调用频率过高 | 等待 30-60 秒后重试 |
| `Content blocked` | 安全过滤器触发 | 调整 prompt 措辞，避免敏感词汇 |
