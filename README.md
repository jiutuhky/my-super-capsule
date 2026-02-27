# my-super-capsule

个人 Claude Code 插件收录

## 插件目录

| 插件 | 分类 | 说明 |
|------|------|------|
| [paper-banana](./paper-banana/) | 可视化 | 基于 Gemini 图像模型的学术论文插图生成器。通过 5 个子代理协作流水线，自动生成符合 NeurIPS/ICML 风格标准的科学示意图（架构图、流程图、方法图）和统计图表（柱状图、折线图、热力图等），支持多轮 Critic 迭代优化。 |
| [patent-writer](./patent-writer/) | 写作 | AI 驱动的中国专利申请文件自动撰写工具。从技术交底书（.docx）出发，经 8 个子代理按序协调，自动生成符合《专利法》和《专利审查指南》的完整申请文件（摘要、权利要求书、说明书、附图）。 |

## 安装

### 第一步：添加插件市场

在 Claude Code 会话中执行：

```
/plugin marketplace add jiutuhky/my-super-capsule
```

### 第二步：安装插件

```
# 学术插图生成插件
/plugin install paper-banana@jiutuhky-plugins

# 专利撰写插件
/plugin install patent-writer@jiutuhky-plugins
```

### 查看已安装的插件

```
/plugin
```

## 环境变量

安装插件后，需根据所用插件配置对应的环境变量：

| 变量 | 所需插件 | 必填 | 说明 |
|------|----------|------|------|
| `GOOGLE_API_KEY` | 两者均需 | 是 | Google Gemini API，用于图像生成 |
| `GOOGLE_API_BASE_URL` | 两者均需 | 否 | 自定义 Gemini API 端点 |
| `SERPAPI_API_KEY` | patent-writer | 是 | Google Patents 专利检索 |
| `EXA_API_KEY` | patent-writer | 是 | Exa 搜索引擎 |

## 依赖

### Python

```bash
pip install google-genai matplotlib Pillow markitdown
```

### Node.js

## 许可证

[MIT](./LICENSE)
