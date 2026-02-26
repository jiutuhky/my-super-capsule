# patent-writer

AI 驱动的中国专利申请文件自动撰写插件，基于 Claude Code 多智能体协调架构。

## 功能

从技术交底书（.docx）自动生成符合中国《专利法》和《专利审查指南》的完整专利申请文件，包括：

- 说明书摘要（<300 字）
- 权利要求书（方法、装置、设备、存储介质多方面保护）
- 说明书（技术领域、背景技术、发明内容、附图说明、具体实施方式 >10000 字）
- AI 生成 PNG 专利附图（方法流程图、装置结构图、系统架构图、硬件截面图）

## 安装

```bash
# 方式一：本地目录安装
claude plugins add /path/to/patent-writer

# 方式二：测试运行
claude --plugin-dir /path/to/patent-writer
```

## 配置 API Keys

本插件使用 MCP 服务器进行专利检索，需要配置以下环境变量：

```bash
# Google Patents 检索（通过 SerpAPI）
export SERPAPI_API_KEY="your-serpapi-key"

# Exa 搜索引擎
export EXA_API_KEY="your-exa-key"
```

## 使用

```bash
# 在 Claude Code 中使用 slash command
/patent-writer:write-patent data/技术交底书.docx
```

该命令会自动协调 8 个子代理按顺序执行：

1. **input-parser** - 解析技术交底书，提取结构化信息
2. **patent-searcher** - 搜索相似专利，学习写作风格
3. **outline-generator** - 生成专利大纲
4. **abstract-writer** - 撰写说明书摘要
5. **claims-writer** - 撰写权利要求书
6. **description-writer** - 撰写说明书（具体实施方式 >10000 字）
7. **diagram-generator** - 生成 PNG 专利附图（AI 绘制）
8. **markdown-merger** - 合并为完整专利文件

输出文件保存在 `output/temp_[uuid]/06_final/complete_patent.md`。

## 插件结构

```
patent-writer/
├── .claude-plugin/
│   └── plugin.json              # 插件清单
├── commands/
│   └── write-patent.md          # 主命令
├── agents/                      # 8 个子代理
│   ├── input-parser.md
│   ├── patent-searcher.md
│   ├── outline-generator.md
│   ├── abstract-writer.md
│   ├── claims-writer.md
│   ├── description-writer.md
│   ├── diagram-generator.md
│   └── markdown-merger.md
├── skills/
│   ├── writing-patent/          # 专利写作协调流程技能
│   │   ├── SKILL.md
│   │   └── references/
│   │       └── patent-writing-guide.md
│   ├── patent-diagram-drawing/  # 专利附图生成技能
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   │   └── generate.py
│   │   └── references/
│   │       └── patent-diagram-spec.md
│   └── patent-writing/          # 专利写作知识技能
│       ├── SKILL.md
│       └── references/
│           └── example-patent.md
├── .mcp.json                    # MCP 服务器配置
└── README.md
```

## 依赖

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI
- [markitdown](https://github.com/microsoft/markitdown) - 用于将 .docx 转换为 Markdown
- [google-genai](https://pypi.org/project/google-genai/) - 用于调用 Gemini Image API 生成专利附图
- Node.js (npx) - 用于运行 MCP 服务器

### 环境变量

| 变量 | 说明 |
|------|------|
| `SERPAPI_API_KEY` | Google Patents 检索 |
| `EXA_API_KEY` | Exa 搜索引擎 |
| `GEMINI_API_KEY` 或 `GOOGLE_API_KEY` | Gemini Image API（专利附图生成） |
| `GEMINI_BASE_URL` 或 `GOOGLE_API_BASE_URL` | 可选，自定义 API 端点 |

## 许可证

MIT
