# paper-banana

基于 Google Gemini 图像模型的学术论文插图生成插件，通过多代理流水线自动生成符合顶会（NeurIPS/ICML）风格标准的出版级插图。

## 功能

- **科学示意图** — 方法架构图、流程图、框架图等，调用 Gemini Image API 直接生成
- **统计图表** — 柱状图、折线图、散点图、热力图、雷达图等，自动生成 matplotlib 代码并执行
- **顶会视觉标准** — 自动应用 NeurIPS 2025 风格指南（配色、字体、线型、布局）
- **多轮迭代优化** — Critic 代理自动审核生成结果，最多 3 轮迭代，满意即提前终止
- **Few-Shot 学习** — 可选从 PaperBananaBench 数据集检索相似参考样例
- **灵活输入** — 支持文本描述、`.tex` 文件、`.md` 文件
- **多种画幅比** — 16:9、1:1、3:2、21:9

## 安装

通过 [my-super-capsule](https://github.com/jiutuhky/my-super-capsule) 插件市场安装：

```
# 1. 添加插件市场（如已添加可跳过）
/plugin marketplace add jiutuhky/my-super-capsule

# 2. 安装插件
/plugin install paper-banana@jiutuhky-plugins
```

## 环境变量

```bash
# Google Gemini API（必填，用于图像生成）
export GOOGLE_API_KEY="your-google-api-key"

# 可选：自定义 API 端点
export GOOGLE_API_BASE_URL="your-custom-endpoint"
```

## Python 依赖

```bash
pip install google-genai matplotlib Pillow
```

## 使用

在 Claude Code 中执行：

```
/paper-banana <描述或文件路径> [--type diagram|plot] [--ratio 16:9|1:1|3:2|21:9]
```

### 示例

```bash
# 从文字描述生成示意图
/paper-banana "A transformer architecture with multi-head attention, feed-forward layers, and residual connections" --type diagram

# 从数据生成统计图
/paper-banana "Bar chart comparing BLEU scores: Model A=35.2, Model B=38.7, Model C=41.3" --type plot

# 从 LaTeX 文件生成
/paper-banana ./paper/method.tex --type diagram --ratio 16:9
```

## 流水线架构

插件协调 5 个子代理按序执行：

```
Retriever → Planner → Stylist → Visualizer → [Critic → Visualizer] ×N
```

| 代理 | 职责 |
|------|------|
| **Retriever** | 从 PaperBananaBench 数据集检索相似参考样例，用于 Few-Shot 学习 |
| **Planner** | 根据方法论或数据生成图的详细文字描述 |
| **Stylist** | 在不改变语义的前提下，为描述添加 NeurIPS 2025 风格细节 |
| **Visualizer** | 将描述转为图像：示意图走 Gemini API，统计图走 matplotlib 代码生成 |
| **Critic** | 对比生成图与源内容，输出修改建议；最多迭代 3 轮，无需修改则提前终止 |

### 输出目录

```
paper_banana_output_YYYYMMDD_HHMMSS/
├── pipeline_state.json     # 流水线状态与文件引用
├── descriptions/           # 各阶段文字描述
├── images/                 # 生成的 JPEG 图像
└── code/                   # matplotlib 代码（仅统计图）
```

## 插件结构

```
paper-banana/
├── .claude-plugin/
│   └── plugin.json                # 插件清单
├── commands/
│   └── paper-banana.md            # 主命令
├── agents/                        # 5 个子代理
│   ├── retriever.md
│   ├── planner.md
│   ├── stylist.md
│   ├── visualizer.md
│   └── critic.md
├── skills/
│   └── paper-banana-orchestration/
│       ├── SKILL.md               # 流水线编排逻辑
│       └── references/
│           ├── planner_guidance.md
│           ├── diagram_style_guide.md
│           ├── plot_style_guide.md
│           ├── critic_guidance.md
│           ├── retriever_guidance.md
│           ├── stylist_guidance.md
│           └── evaluation_prompts.md
├── scripts/
│   ├── generate_diagram.py        # Gemini 图像生成封装
│   └── execute_plot.py            # matplotlib 代码执行器
└── README.md
```

## 许可证

MIT
