# 专利附图 Prompt 模板

本文件包含 4 种 CNIPA 标准专利附图的 Gemini Image API prompt 模板。
使用时选择对应类型，将 `{占位符}` 替换为实际内容。

线宽、编号格式、布局等详细规范见 `patent-diagram-spec.md`。

---

## 方法流程图

```
Generate a black-and-white patent-style method flowchart for a Chinese patent application (CNIPA standard).

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
- Arrows connecting steps top to bottom
- Decision branches labeled "是" and "否"
- Line weights per CNIPA patent-diagram-spec (border 2pt, boxes 1.5pt, arrows 1pt)
- Professional patent illustration quality
```

**占位符说明**：
- `{N}` — 图号（如 1、2、3）
- `{X}` — 步骤编号前缀（如 1 表示 S101/S102，2 表示 S201/S202）
- `{步骤名称}` — 从 description.md 中提取的实际步骤名称

---

## 装置结构框图

```
Generate a black-and-white patent-style apparatus structure block diagram for a Chinese patent application (CNIPA standard).

Title at bottom center: "图{N}"

Apparatus: {装置名称} {总编号}
Modules inside dashed boundary:
- {模块1名称} {编号}
- {模块2名称} {编号}
...

Data flow:
- {模块1} -> {模块2}: {数据描述}
...

Requirements:
- Pure black and white, NO grayscale, NO colors, NO shadows
- Engineering drawing style with clean lines
- Dashed rectangle as apparatus boundary with title and number
- Solid rectangles for functional modules with name and number
- Arrows showing data/control flow direction, all labels in Chinese
- Line weights per CNIPA patent-diagram-spec (boundary 2pt dashed, modules 1.5pt solid, arrows 1pt)
- Professional patent illustration quality
```

**占位符说明**：
- `{总编号}` — 装置总编号（如 200）
- `{编号}` — 模块编号（如 201、202）
- `{数据描述}` — 模块间传递的数据内容

---

## 系统架构图

```
Generate a black-and-white patent-style system architecture diagram for a Chinese patent application (CNIPA standard).

Title at bottom center: "图{N}"

Layers (top to bottom):
- {层1名称}: {组件1} {编号}, {组件2} {编号}
- {层2名称}: {组件3} {编号}, {组件4} {编号}
...

Communication:
- {组件1} -> {组件3}: {协议/数据}
...

Requirements:
- Pure black and white, NO grayscale, NO colors, NO shadows
- Layered layout with dashed boxes grouping each layer
- Rectangles for components with Chinese labels and numbers
- Arrows with protocol/data annotations
- Line weights per CNIPA patent-diagram-spec (layer boundaries 2pt dashed, components 1.5pt solid, arrows 1pt)
- Professional patent illustration quality
```

**占位符说明**：
- `{层名称}` — 架构层名称（如客户端层、服务层、数据层）
- `{编号}` — 组件编号（如 301、302）

---

## 硬件截面图

```
Generate a black-and-white patent-style hardware cross-section diagram for a Chinese patent application (CNIPA standard).

Title at bottom center: "图{N}"

Structure: {硬件结构描述}

Components with reference numbers:
- {部件1}: {编号}
- {部件2}: {编号}
...

Requirements:
- Pure black and white, NO grayscale, NO colors, NO shadows
- Engineering drawing style with clean precise lines
- 45-degree cross-hatching for sectioned solid parts
- Leader lines with Arabic numeral reference numbers, no crossing
- Numbers increment top-to-bottom, left-to-right
- Line weights per CNIPA patent-diagram-spec (contour 2pt, structure 1.5pt, leader lines 1pt, hatching 0.5pt)
- Professional patent illustration quality
```

**占位符说明**：
- `{硬件结构描述}` — 硬件的物理结构描述
- `{编号}` — 部件引出线编号
