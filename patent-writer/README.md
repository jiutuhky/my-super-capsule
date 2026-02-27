# patent-writer

AI 驱动的中国专利申请文件自动撰写插件，基于 Claude Code 多智能体协调架构。

## 功能

从技术交底书（.docx）自动生成符合中国《专利法》和《专利审查指南》的完整专利申请文件：

- **说明书摘要** — <300 字，标准格式
- **权利要求书** — 方法、装置、设备、存储介质多方面保护
- **说明书** — 技术领域、背景技术、发明内容、附图说明、具体实施方式（>10000 字）
- **专利附图** — AI 生成 PNG 格式（方法流程图、装置结构图、系统架构图、硬件截面图）

## 安装

通过 [my-super-capsule](https://github.com/jiutuhky/my-super-capsule) 插件市场安装：

```
# 1. 添加插件市场（如已添加可跳过）
/plugin marketplace add jiutuhky/my-super-capsule

# 2. 安装插件
/plugin install patent-writer@jiutuhky-plugins
```

## 环境变量

```bash
# Google Patents 检索（通过 SerpAPI，必填）
export SERPAPI_API_KEY="your-serpapi-key"

# Exa 搜索引擎（必填）
export EXA_API_KEY="your-exa-key"

# Gemini Image API（必填，用于生成专利附图）
export GOOGLE_API_KEY="your-google-api-key"

# 可选：自定义 API 端点
export GOOGLE_API_BASE_URL="your-custom-endpoint"
```

## 依赖

- [markitdown](https://github.com/microsoft/markitdown) — 将 .docx 转换为 Markdown
- [google-genai](https://pypi.org/project/google-genai/) — Gemini Image API，生成专利附图
- Node.js (`npx`) — 运行 MCP 服务器

```bash
pip install markitdown google-genai
```

## 使用

在 Claude Code 中执行：

```
/patent-writer:write-patent data/技术交底书.docx
```

### 流水线

该命令自动协调 8 个子代理按序执行：

| 步骤 | 代理 | 职责 |
|------|------|------|
| 1 | **input-parser** | 解析技术交底书，提取结构化信息 |
| 2 | **patent-searcher** | 搜索相似专利，分析现有技术，学习写作风格 |
| 3 | **outline-generator** | 生成专利文件大纲与字数规划 |
| 4 | **abstract-writer** | 撰写说明书摘要（<300 字） |
| 5 | **claims-writer** | 撰写权利要求书（独立+从属权利要求） |
| 6 | **description-writer** | 撰写说明书（具体实施方式 >10000 字） |
| 7 | **diagram-generator** | 生成符合 CNIPA 标准的 PNG 专利附图 |
| 8 | **markdown-merger** | 合并所有章节，生成完整专利文件 |

### 输出目录

```
output/temp_[uuid]/
├── 01_input/        # 原始文档、解析结果
├── 02_research/     # 相似专利、现有技术分析
├── 03_outline/      # 专利大纲、结构映射
├── 04_content/      # 摘要、权利要求书、说明书
├── 05_diagrams/     # 专利附图
├── 06_final/        # complete_patent.md（最终输出）
└── metadata/        # 项目信息、代理日志、质量检查
```

## 插件结构

```
patent-writer/
├── .claude-plugin/
│   └── plugin.json                # 插件清单
├── commands/
│   └── write-patent.md            # 主命令
├── agents/                        # 8 个子代理
│   ├── input-parser.md
│   ├── patent-searcher.md
│   ├── outline-generator.md
│   ├── abstract-writer.md
│   ├── claims-writer.md
│   ├── description-writer.md
│   ├── diagram-generator.md
│   └── markdown-merger.md
├── skills/
│   ├── writing-patent/            # 专利写作协调流程
│   │   ├── SKILL.md
│   │   └── references/
│   │       └── patent-writing-guide.md
│   └── patent-diagram-drawing/    # 专利附图生成
│       ├── SKILL.md
│       ├── scripts/
│       │   └── generate.py
│       └── references/
│           ├── patent-diagram-spec.md
│           └── prompt-templates.md
├── .mcp.json                      # MCP 服务器配置
└── README.md
```

## 许可证

MIT
