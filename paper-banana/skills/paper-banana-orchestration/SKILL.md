---
name: paper-banana-orchestration
description: >
  Generate publication-quality academic illustrations (diagrams and statistical plots) for
  research papers using the PaperBanana multi-agent pipeline. Supports: (1) Diagrams -
  scientific method/architecture illustrations via Gemini image API, (2) Plots - statistical
  visualizations via matplotlib code generation. Use when user wants to create academic figures,
  conference paper illustrations, method diagrams, architecture diagrams, pipeline diagrams,
  statistical plots, bar charts, line charts, heatmaps, or NeurIPS/ICML-style academic visualizations.
  Also supports polishing existing figures and reading .tex/.md files to auto-generate paper illustrations.
---

# PaperBanana Orchestration Skill

You are the orchestrator for the PaperBanana multi-agent pipeline. Your job is to coordinate 5 sub-agents to generate publication-quality academic illustrations.

## Pipeline Overview

```
Retriever → Planner → Stylist → Visualizer → [Critic → Visualizer] ×N
```

## File-Based Storage Convention

Long text content (descriptions, critic suggestions) is stored as **separate files** in subdirectories, NOT inline in `pipeline_state.json`. This keeps the state file lightweight and prevents issues with large JSON values.

Directory layout inside the output directory:
```
{output_dir}/
├── pipeline_state.json       # lightweight metadata + file path references
├── descriptions/             # all text descriptions and critic suggestions (.txt)
├── images/                   # all generated images (.jpg)
└── code/                     # matplotlib code for plot tasks (.py)
```

**Convention**: When a sub-agent writes a description, it writes the full text to a file (e.g., `descriptions/desc0.txt`) and stores only the **relative file path** in `pipeline_state.json` (e.g., `"target_diagram_desc0": "descriptions/desc0.txt"`). To read a description, construct the absolute path: `{output_dir}/{relative_path}`.

This convention applies to all description keys (`target_*_desc*`), critic suggestion keys (`target_*_critic_suggestions*`), image path keys (`target_*_image_path`), and code keys (`target_*_code`). All paths in `pipeline_state.json` are **relative to `output_dir`**.

## Step 0: Parse User Input

Parse the user's input to determine:

1. **`task_type`**: "diagram" or "plot"
   - If the user provides a method description, methodology section, or asks for architecture/pipeline/framework diagrams → "diagram"
   - If the user provides raw data (tabular, JSON) or asks for charts/plots/visualizations → "plot"
   - If `--type diagram` or `--type plot` is explicitly specified, use that
   - If ambiguous, ask the user via AskUserQuestion

2. **`content`**: The main input content
   - For diagrams: methodology section text
   - For plots: raw data (tabular, JSON, or text)
   - If the user provides a file path, read the file content

3. **`visual_intent`**: The figure caption or visualization intent
   - For diagrams: the figure caption (e.g., "Overview of the proposed framework")
   - For plots: the visualization intent (e.g., "Bar chart comparing model performance")
   - If not explicitly provided, ask the user

4. **`aspect_ratio`**: Output aspect ratio
   - Default: "1:1"
   - If `--ratio` is specified, use that value
   - Valid options: "16:9", "1:1", "3:2", "21:9"

5. **`max_critic_rounds`**: Maximum critic iteration rounds
   - Default: 3

6. **`retrieval_setting`**: Reference retrieval mode
   - Default: "none" (most users won't have the PaperBananaBench dataset)
   - Set to "auto" only if the user explicitly requests reference-based generation and the dataset exists

## Step 1: Create Working Directory and Initialize Pipeline State

Create the output directory with a timestamp suffix, along with subdirectories:

```bash
OUTPUT_DIR="./paper_banana_output_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUTPUT_DIR/descriptions" "$OUTPUT_DIR/images" "$OUTPUT_DIR/code"
```

Resolve `OUTPUT_DIR` to an absolute path (e.g., via `realpath` or `pwd`), then write `pipeline_state.json` **inside the output directory**:

```json
{
  "task_type": "diagram|plot",
  "content": "<methodology section or raw data>",
  "visual_intent": "<figure caption or visualization intent>",
  "aspect_ratio": "1:1",
  "max_critic_rounds": 3,
  "current_critic_round": 0,
  "retrieval_setting": "none",
  "output_dir": "<absolute path to OUTPUT_DIR>",
  "top10_references": [],
  "retrieved_examples": []
}
```

Note: `pipeline_state.json` is located at `{output_dir}/pipeline_state.json`. The `content` field remains inline; all other long text generated during the pipeline is stored as files.

## Step 2: Dispatch Retriever Agent

Use the Task tool to dispatch the retriever sub-agent:

```
Task(
  subagent_type="paper-banana:retriever",
  prompt="Read pipeline_state.json and retrieve relevant reference examples based on retrieval_setting. Update pipeline_state.json with top10_references and retrieved_examples. The pipeline_state.json is located at: {output_dir}/pipeline_state.json"
)
```

After the retriever completes, read `pipeline_state.json` to verify `top10_references` was updated.

**If `retrieval_setting` is "none"**, you may skip this step entirely (the state already has empty lists).

## Step 3: Dispatch Planner Agent

Use the Task tool to dispatch the planner sub-agent:

```
Task(
  subagent_type="paper-banana:planner",
  prompt="Read pipeline_state.json and generate a detailed textual description for the target figure based on content, visual_intent, and any retrieved reference examples. Write the description to {output_dir}/descriptions/desc0.txt, then set target_{task_type}_desc0 to 'descriptions/desc0.txt' in pipeline_state.json. The pipeline_state.json is located at: {output_dir}/pipeline_state.json"
)
```

After the planner completes, read `pipeline_state.json` to verify `target_{task_type}_desc0` was set.

## Step 4: Dispatch Stylist Agent

Use the Task tool to dispatch the stylist sub-agent:

```
Task(
  subagent_type="paper-banana:stylist",
  prompt="Read pipeline_state.json, then read the planner's description from the file referenced by target_{task_type}_desc0 (relative to output_dir). Refine the description with NeurIPS 2025 aesthetic details. Read the appropriate style guide from ${CLAUDE_PLUGIN_ROOT}/skills/paper-banana-orchestration/references/. Write the refined description to {output_dir}/descriptions/stylist_desc0.txt, then set target_{task_type}_stylist_desc0 to 'descriptions/stylist_desc0.txt' in pipeline_state.json. The pipeline_state.json is located at: {output_dir}/pipeline_state.json"
)
```

After the stylist completes, read `pipeline_state.json` to verify `target_{task_type}_stylist_desc0` was set.

## Step 5: Dispatch Visualizer Agent

Use the Task tool to dispatch the visualizer sub-agent:

```
Task(
  subagent_type="paper-banana:visualizer",
  prompt="Read pipeline_state.json and generate images for all description keys that don't yet have corresponding image paths. Read descriptions from files (paths in pipeline_state.json are relative to output_dir). Save images to {output_dir}/images/. For diagram tasks, use ${CLAUDE_PLUGIN_ROOT}/scripts/generate_diagram.py. For plot tasks, generate matplotlib code, save to {output_dir}/code/, and use ${CLAUDE_PLUGIN_ROOT}/scripts/execute_plot.py. Update pipeline_state.json with relative image paths. The pipeline_state.json is located at: {output_dir}/pipeline_state.json"
)
```

After the visualizer completes, read `pipeline_state.json` to verify image paths were written.

## Step 6: Critic Loop

This is the iterative refinement loop.

### Initialization

```
current_best_image_key = "target_{task_type}_stylist_desc0_image_path"
```

### Loop (up to max_critic_rounds iterations)

```
for round_idx in range(max_critic_rounds):

    # 6a. Update current_critic_round in pipeline_state.json
    Update pipeline_state.json: set "current_critic_round" to round_idx

    # 6b. Dispatch Critic Agent
    Task(
      subagent_type="paper-banana:critic",
      prompt="Read pipeline_state.json (current_critic_round is {round_idx}). Critique the generated image and its description. For round 0, use the stylist output; for round N>0, use critic_desc{N-1}. Read descriptions and images from files (paths are relative to output_dir). Write critic suggestions to {output_dir}/descriptions/critic_suggestions{round_idx}.txt and revised description to {output_dir}/descriptions/critic_desc{round_idx}.txt. Update pipeline_state.json with the relative file paths. The pipeline_state.json is located at: {output_dir}/pipeline_state.json"
    )

    # 6c. Read pipeline_state.json to check critic output
    Read pipeline_state.json

    # 6d. Check early stop condition — read the suggestions file
    suggestions_path = pipeline_state["target_{task_type}_critic_suggestions{round_idx}"]
    suggestions_content = Read({output_dir}/{suggestions_path})
    if suggestions_content.strip() == "No changes needed.":
        break  # Early stop - figure is satisfactory

    # 6e. Dispatch Visualizer Agent for revised description
    Task(
      subagent_type="paper-banana:visualizer",
      prompt="Read pipeline_state.json and generate images for the new critic description key target_{task_type}_critic_desc{round_idx}. Read the description from its file. Save image to {output_dir}/images/. Update pipeline_state.json with relative image path. The pipeline_state.json is located at: {output_dir}/pipeline_state.json"
    )

    # 6f. Read pipeline_state.json to check visualization result
    Read pipeline_state.json

    # 6g. Check if new image was generated successfully
    new_image_key = "target_{task_type}_critic_desc{round_idx}_image_path"
    if new_image_key exists and is valid in pipeline_state:
        current_best_image_key = new_image_key
    else:
        # Visualization failed, rollback to previous best image
        break
```

### After Loop

The final best image is at the path `{output_dir}/{relative_path}` where the relative path is stored in `current_best_image_key` in `pipeline_state.json`.

## Step 7: Present Final Result

1. Read the final image using the Read tool (it supports images) to display it to the user.
   Construct the absolute path: `{output_dir}/{pipeline_state[current_best_image_key]}`
2. Report the pipeline summary:
   - Task type (diagram/plot)
   - Number of critic rounds completed
   - Whether early stop was triggered
   - Final image file path (absolute)
   - Output directory path

Example output:
```
Pipeline complete!
- Task: diagram
- Critic rounds: 2/3 (early stop: critic found no changes needed)
- Final image: ./paper_banana_output_20260226_143052/images/critic_desc1.jpg
- Output directory: ./paper_banana_output_20260226_143052/
```

## Important Notes

- **Always use absolute paths** when dispatching sub-agents, as they run in independent contexts.
- **Always read pipeline_state.json** after each sub-agent completes to verify the expected output was written.
- **pipeline_state.json is inside output_dir** — located at `{output_dir}/pipeline_state.json`.
- **File-based storage** — descriptions, suggestions, images, and code are stored as separate files. Only relative file paths are stored in `pipeline_state.json`. To read content, join `output_dir` + relative path.
- **For plot tasks**, the visualizer agent generates matplotlib code. If code execution fails, the critic will detect the failure and provide a revised description.
- **${CLAUDE_PLUGIN_ROOT}** refers to the root directory of this plugin (i.e., the directory containing `.claude-plugin/`).
