# paper-banana

Generate publication-quality academic illustrations (diagrams and statistical plots) for research papers using a multi-agent pipeline powered by Google Gemini models.

## Features

- **Scientific Diagrams** - Method illustrations, architecture diagrams, pipeline diagrams, framework overviews via Gemini image generation API
- **Statistical Plots** - Bar charts, line charts, scatter plots, heatmaps, radar charts, etc. via matplotlib code generation
- **NeurIPS/ICML Aesthetic Standards** - Automatically applies conference-grade visual styling
- **Iterative Refinement** - Multi-round critic loop with automatic quality checking and early stopping
- **Few-Shot Learning** - Optional reference retrieval from PaperBananaBench dataset
- **Flexible Input** - Accepts text descriptions, `.tex` files, or `.md` files
- **Multiple Aspect Ratios** - Supports 16:9, 1:1, 3:2, 21:9

## Installation

```bash
# Option 1: Install as plugin
claude plugins add /path/to/paper-banana

# Option 2: Test run
claude --plugin-dir /path/to/paper-banana
```

## Configuration

Set the following environment variable:

```bash
# Google Gemini API (required for diagram generation)
export GOOGLE_API_KEY="your-google-api-key"

# Optional: custom API endpoint
export GOOGLE_API_BASE_URL="your-custom-endpoint"
```

### Python Dependencies

```bash
pip install google-genai matplotlib Pillow
```

## Usage

```bash
# In Claude Code, use the slash command
/paper-banana <description-or-file-path> [--type diagram|plot] [--ratio 16:9|1:1|3:2|21:9]
```

### Examples

```bash
# Generate a diagram from a description
/paper-banana "A transformer architecture with multi-head attention, feed-forward layers, and residual connections" --type diagram

# Generate a plot from data
/paper-banana "Bar chart comparing BLEU scores: Model A=35.2, Model B=38.7, Model C=41.3" --type plot

# Generate from a LaTeX file
/paper-banana ./paper/method.tex --type diagram --ratio 16:9
```

## Pipeline Architecture

The plugin orchestrates 5 specialized sub-agents in sequence:

```
Retriever → Planner → Stylist → Visualizer → [Critic → Visualizer] ×N
```

1. **Retriever** - Retrieves relevant reference examples for few-shot learning (optional)
2. **Planner** - Generates detailed textual descriptions from methodology or data
3. **Stylist** - Refines descriptions with NeurIPS 2025 aesthetic details
4. **Visualizer** - Converts descriptions into images (Gemini API for diagrams, matplotlib for plots)
5. **Critic** - Iterative quality refinement (up to 3 rounds, early stop when satisfied)

Output is saved to `./paper_banana_output_YYYYMMDD_HHMMSS/` with subdirectories:

```
paper_banana_output_*/
├── pipeline_state.json    # Pipeline metadata and file references
├── descriptions/          # Text descriptions from each stage
├── images/                # Generated JPEG images
└── code/                  # Matplotlib code (plots only)
```

## Plugin Structure

```
paper-banana/
├── .claude-plugin/
│   └── plugin.json           # Plugin manifest
├── commands/
│   └── paper-banana.md       # Main slash command
├── agents/
│   ├── retriever.md          # Reference example retrieval
│   ├── planner.md            # Description generation
│   ├── stylist.md            # Aesthetic refinement
│   ├── visualizer.md         # Image generation
│   └── critic.md             # Quality critique & iteration
├── skills/
│   └── paper-banana-orchestration/
│       ├── SKILL.md          # Pipeline orchestration logic
│       └── references/
│           ├── planner_guidance.md
│           ├── diagram_style_guide.md
│           ├── plot_style_guide.md
│           ├── critic_guidance.md
│           ├── retriever_guidance.md
│           ├── stylist_guidance.md
│           └── evaluation_prompts.md
├── scripts/
│   ├── generate_diagram.py   # Gemini image generation wrapper
│   └── execute_plot.py       # Matplotlib code executor
└── README.md
```

## Dependencies

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI
- [google-genai](https://pypi.org/project/google-genai/) - Gemini image generation API
- [matplotlib](https://matplotlib.org/) - Statistical plot generation
- [Pillow](https://pillow.readthedocs.io/) - Image processing (PNG to JPEG conversion)

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_API_KEY` | Yes | Google Gemini API key for diagram generation |
| `GOOGLE_API_BASE_URL` | No | Custom API endpoint |

## License

MIT
