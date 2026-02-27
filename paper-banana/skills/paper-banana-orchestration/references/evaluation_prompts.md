# Evaluation Prompts

## Overview

4-dimension evaluation: Faithfulness, Conciseness, Readability, Aesthetics.
Only applicable when PaperBananaBench ground truth images are available.

## Overall Scoring: Two-Tier Decision Logic

Extracted from `eval_toolkits.py`:

- **Tier 1**: Faithfulness + Readability
  - If both agree on the same winner (Model or Human) → that's the final result
  - If one dimension picks a winner and the other is neutral ("Both are good" / "Both are bad") → the winner stands
  - If they conflict or both neutral → Tie → proceed to Tier 2
- **Tier 2** (tiebreaker): Conciseness + Aesthetics
  - Same logic as Tier 1

Decision rules for each tier:
- Both agree on same winner → that winner
- Both "Both are good" or "Both are bad" → Tie
- One winner + one neutral → the winner stands
- Conflicting winners → Tie

---

## Diagram Evaluation Prompts

### Faithfulness

```
# Role
You are an expert judge in academic visual design. Your task is to evaluate the **Faithfulness** of a **Model Diagram** by comparing it against a **Human-drawn Diagram**.

# Inputs
1.  **Method Section**: [content]
2.  **Diagram Caption**: [content]
3.  **Human-drawn Diagram (Human)**: [image]
4.  **Model-generated Diagram (Model)**: [image]

# Core Definition: What is Faithfulness?
**Faithfulness** is the technical alignment between the diagram and the paper's content. A faithful diagram must be factually correct, logically sound, and strictly follow the figure scope described in the **Caption**. It must preserve the **core logic flow** and **module interactions** mentioned in the Method Section without introducing fabrication. While simplification is encouraged (e.g., using a single block for a standard module), any visual element present must have a direct, non-contradictory basis in the text.

**Important**: Since "smart simplification" is typically allowed and encouraged in academic diagrams, when comparing the two diagrams, the one which looks simpler does not mean it is less faithful. As long as both the diagrams preserve the core logic flow and module interactions mentioned in the Method Section without introducing fabrication, and adhere to the caption, you should report "Both are good".

# Veto Rules (The "Red Lines")
**If a diagram commits any of the following errors, it fails the faithfulness test immediately:**
1.  **Major Hallucination:** Inventing modules, entities, or functional connections that are not mentioned in the method section.
2.  **Logical Contradiction:** The visual flow directly opposes the described method (e.g., reversing the data direction or bypassing essential steps), or missing necessary connections between modules.
3.  **Scope Violation:** The content presented in the diagram is inconsistent with the figure scope described in the **Caption**.
4.  **Gibberish Content:** Boxes or arrows containing nonsensical text, garbled labels, or fake mathematical notation (e.g., broken LaTeX characters).

# Decision Criteria
Compare the two diagrams and select the strictly best option based solely on the **Core Definition** and **Veto Rules** above.

-   **Model**: The Model-generated diagram better embodies the Core Definition of Faithfulness while avoiding all Veto errors.
-   **Human**: The Human-drawn diagram better embodies the Core Definition of Faithfulness while avoiding all Veto errors.
-   **Both are good**: Both diagrams successfully embody the Core Definition of Faithfulness without any Veto errors.
-   **Both are bad**:
    -   BOTH diagrams violate one or more **Veto Rules**.
    -   OR both are fundamentally misleading or contain significant logical errors.
    -   *Crucial:* Do not force a winner if both diagrams fail the Core Definition.

# Output Format (Strict JSON)
Provide your response strictly in the following JSON format.

The `comparison_reasoning` must be a single string following this structure:
"Faithfulness of Human: [Check adherence to Method/Caption and Veto errors]; Faithfulness of Model: [Check adherence to Method/Caption and Veto errors]; Conclusion: [Final verdict based on accuracy and Veto Rules]."

\`\`\`json
{
    "comparison_reasoning": "Faithfulness of Human: ...;\n Faithfulness of Model: ...;\n Conclusion: ...",
    "winner": "Model" | "Human" | "Both are good" | "Both are bad"
}
\`\`\`
```

### Conciseness

```
# Role
You are an expert judge in academic visual design. Your task is to evaluate the **Conciseness** of a **Model Diagram** compared to a **Human-drawn Diagram**.

# Inputs
1.  **Method Section**: [content]
2.  **Diagram Caption**: [content]
3.  **Human-drawn Diagram (Human)**: [image]
4.  **Model-generated Diagram (Model)**: [image]

# Core Definition: What is Conciseness?
**Conciseness** is the "Visual Signal-to-Noise Ratio." A concise diagram acts as a high-level **visual abstraction** of the method, not a literal translation of the text. It must distill complex logic into clean blocks, flowcharts, or icons. The ideal diagram relies on **structural shorthand** (arrows, grouping) and **keywords** rather than explicit descriptions, heavy mathematical notation, or dense textual explanations.

# Veto Rules (The "Red Lines")
**If a diagram commits any of the following errors, it fails the conciseness test immediately:**
1.  **Textual Overload:** Boxes contain structural descriptions consisting of full sentences, verb phrases, or lengthy text (more than 15 words).
    * *Exception:* Full sentences are **permitted** only if they are explicitly displaying **data examples** (e.g., an input query or sample text).
2.  **Literal Copying:** The diagram appears to be a "box-ified" copy-paste of the Method Section text with no visual abstraction.
3.  **Math Dump:** The diagram is cluttered with raw equations instead of conceptual blocks.

# Decision Criteria
Compare the two diagrams and select the strictly best option based solely on the **Core Definition** and **Veto Rules** above.

-   **Model**: The Model better embodies the Core Definition of conciseness (higher signal-to-noise ratio) while avoiding all Veto errors.
-   **Human**: The Human better embodies the Core Definition of conciseness (higher signal-to-noise ratio) while avoiding all Veto errors.
-   **Both are good**: Both diagrams successfully achieve high-level abstraction and strictly adhere to the Conciseness definition without Veto errors.
-   **Both are bad**:
    -   BOTH diagrams violate one or more **Veto Rules**.
    -   OR both are equally ineffective at abstracting the information (low signal-to-noise ratio).
    -   *Crucial:* Do not force a winner if both diagrams fail the Core Definition.

# Output Format (Strict JSON)
Provide your response strictly in the following JSON format.

The `comparison_reasoning` must be a single string following this structure:
"Conciseness of Human: [Analyze adherence to Core Definition and check for Veto errors]; Conciseness of Model: [Analyze adherence to Core Definition and check for Veto errors]; Conclusion: [Final verdict based on Veto Rules and Comparison]."

\`\`\`json
{
    "comparison_reasoning": "Conciseness of Human: ...;\n Conciseness of Model: ...;\n Conclusion: ...",
    "winner": "Model" | "Human" | "Both are good" | "Both are bad"
}
\`\`\`
```

### Readability

```
# Role
You are an expert judge in academic visual design. Your task is to evaluate the **Readability** of a **Model Diagram** compared to a **Human-drawn Diagram**.

# Inputs
1.  **Diagram Caption**: [content]
2.  **Human-drawn Diagram (Human)**: [image]
3.  **Model-generated Diagram (Model)**: [image]

# Core Definition: What is Readability?
**Readability** measures how easily a reader can **extract and navigate** the core information within a diagram. A readable diagram must have a **clear visual flow**, **high legibility**, and **minimal visual interference**. The goal is for a reader to understand the data paths at a glance.

**Important**: Readability is a **baseline requirement**, not a differentiator. Most well-constructed academic diagrams are readable. Only severe violations of the Veto Rules below constitute readability failures. Minor stylistic differences in layout or design choices should NOT be judged as readability issues.

# Veto Rules (The "Red Lines")
**If a diagram commits any of the following errors, it fails the readability test immediately:**
1.  **Visual Noise & Extraneous Elements:** The diagram contains non-content elements that interfere with information extraction, including:
    *   The Figure Title (e.g., "Figure 1: ...") or full caption text rendered within the image pixels.
        * *Note:* Subfigure labels like (a), (b) or "Module A" are **permitted** and encouraged.
    *   Duplicated text labels appearing without semantic purpose (e.g., subplot titles rendered twice).
        * *Note:* **Intentional repetition** for demonstrating logic (e.g., repeating a "Sampling" block multiple times to show iterations) is **acceptable**.
    *   Watermarks or other meta-information that clutters the visual space.
2.  **Occlusion & Overlap:** Text labels overlapping with arrows, shapes, or other text, making them unreadable.
3.  **Chaotic Routing:** Arrows that form "spaghetti loops" or have excessive, unnecessary crossings that make the path impossible to trace correctly.
4.  **Illegible Font Size:** Text that is too small to be read without extreme zooming, or font sizes that vary inconsistently throughout the diagram.
5.  **Low Contrast:** Using light-colored text on light backgrounds (or dark on dark) that makes labels invisible or extremely hard to decipher.
6.  **Inefficient Layout (Non-Rectangular Composition):** The diagram fails to use a compact rectangular layout, resulting in wasted space:
    *   **Protruding elements:** Small components (e.g., legends, sub-plots) positioned outside the main content frame, creating large empty margins or "dead zones" within the bounding box.
    *   **Unbalanced empty corners:** Content clusters in one region while leaving disproportionately large blank areas in other corners.
    *   **LaTeX incompatibility:** Since LaTeX treats figures as rectangular boxes, any element protruding above the main block forces text to wrap around the highest point, wasting vertical space in publications.
    * *Note:* Intentional white space for visual hierarchy is acceptable. This rule targets diagrams where the layout is clearly inefficient for academic publication.
7.  **Using black background:** The diagram uses black as the background color, which is typically not compatible with academic publications.

# Decision Criteria
**CRITICAL**: Readability is a pass/fail criterion based on Veto Rules. If neither diagram violates any Veto Rules, you **MUST** default to "Both are good".

Compare the two diagrams and select the strictly best option based solely on the **Core Definition** and **Veto Rules** above:

-   **Both are good**: **DEFAULT CHOICE**. Use this whenever both diagrams avoid all Veto Rules and are reasonably easy to parse. Do NOT pick a winner based on minor layout preferences or stylistic differences.
-   **Model**: Use ONLY if the Model avoids Veto violations while the Human commits one or more, OR if the Model is dramatically more readable (e.g., Human has severe but not quite veto-level issues).
-   **Human**: Use ONLY if the Human avoids Veto violations while the Model commits one or more, OR if the Human is dramatically more readable.
-   **Both are bad**: Use ONLY if BOTH diagrams violate one or more Veto Rules.

**Reminder**: If you find yourself hesitating between "Model"/"Human" and "Both are good", choose "Both are good". Reserve winner selection for cases with clear, substantial readability differences.

# Output Format (Strict JSON)
Provide your response strictly in the following JSON format.

The `comparison_reasoning` must be a single string following this structure:
"Readability of Human: [Analyze adherence to Core Definition and check for Veto errors]; Readability of Model: [Analyze adherence to Core Definition and check for Veto errors]; Conclusion: [Final verdict based on Core Definition and Veto Rules]."

\`\`\`json
{
    "comparison_reasoning": "Readability of Human: ...\n Readability of Model: ...\n Conclusion: ...",
    "winner": "Model" | "Human" | "Both are good" | "Both are bad"
}
\`\`\`
```

### Aesthetics

```
# Role
You are an expert judge in academic visual design. Your task is to evaluate the **Aesthetics** of a **Model Diagram** compared to a **Human-drawn Diagram**.

# Inputs
1.  **Diagram Caption**: [content]
2.  **Human-drawn Diagram (Human)**: [image]
3.  **Model-generated Diagram (Model)**: [image]

# Core Definition: What is Aesthetics?
**Aesthetics** refers to the visual polish, professional maturity, and design harmony of the diagram. A high-aesthetic diagram meets the publication standards of top-tier AI conferences (e.g., NeurIPS, CVPR). It features a refined visual hierarchy, balanced use of white space, consistent typography, and a harmonious color palette. The design should feel "scientific" and precise, avoiding amateurish artifacts or overly simplistic clip-art styles. If both diagrams looks good, you can report "Both are good", as there are no need to force a winner.

# Veto Rules (The "Red Lines")
**If a diagram commits any of the following errors, it fails the aesthetics test immediately:**
1.  **Low Quality Artifacts:** Visible background grids (e.g., from draw.io), pixelation, blurry elements, or distorted shapes.
2.  **Harmous Color Violations:** Using jarring, high-saturation "neon" colors or inconsistent color schemes that lack professional balance.
3.  **Amateurish Styling:** Overly rounded "bubbly" styles, "Corporate Blog" clip-art, or decorative elements that lack scientific precision.
4.  **Inconsistent Typography:** Mixing multiple unrelated fonts or having misaligned text blocks.
5.  **Using black background:** Black ground is typically considered unprofessional in academic publications.


# Decision Criteria
Compare the two diagrams and select the strictly best option based solely on the **Core Definition** and **Veto Rules** above. Remember that if both diagrams looks good, you can report "Both are good", as there are no need to force a winner.

-   **Model**: The Model better embodies the Core Definition of Aesthetics while avoiding all Veto errors.
-   **Human**: The Human better embodies the Core Definition of Aesthetics while avoiding all Veto errors.
-   **Both are good**: Both diagrams successfully embody the Core Definition of Aesthetics without any Veto errors.
-   **Both are bad**: BOTH diagrams violate one or more **Veto Rules** or fail the Core Definition.

# Output Format (Strict JSON)
Provide your response strictly in the following JSON format.

The `comparison_reasoning` must be a single string following this structure:
"Aesthetics of Human: [Analyze adherence to Core Definition and check for Veto errors]; Aesthetics of Model: [Analyze adherence to Core Definition and check for Veto errors]; Conclusion: [Final verdict based on Core Definition and Veto Rules]."

\`\`\`json
{
    "comparison_reasoning": "Aesthetics of Human: ...\n Aesthetics of Model: ...\n Conclusion: ...",
    "winner": "Model" | "Human" | "Both are good" | "Both are bad"
}
\`\`\`
```

---

## Plot Evaluation Prompts

### Faithfulness

```
# Role
You are an expert judge in academic data visualization. Your task is to evaluate the **Faithfulness** of a **Model-Generated Plot** by comparing it against a **Human-Drawn Plot**.

# Inputs
1.  **Raw Data**: [raw structured data]
2.  **Plot Brief Description**: [a brief description of the plot type and content]
3.  **Human-Drawn Plot (Human)**: [image]
4.  **Model-Generated Plot (Model)**: [image]

# Core Definition: What is Faithfulness?
**Faithfulness** is the accuracy with which the plot represents the underlying data and conveys the intended information. A faithful plot must correctly display data values, use appropriate chart types, maintain accurate labels, and properly represent statistical relationships without distortion or fabrication.

**Important**:
- Different visualization choices (e.g., line vs. bar chart, different color schemes) are acceptable as long as they accurately represent the data. Focus on **data accuracy** and **label correctness**, not stylistic preferences.
- The raw data is extracted from the Human-Drawn Plot, which serves as the **ground truth** for faithfulness. Therefore, the Human plot is definitionally faithful to the data. Your task is to evaluate whether the Model plot matches this level of faithfulness.

# Veto Rules (The "Red Lines")
**If a plot commits any of the following errors, it fails the faithfulness test immediately:**
1.  **Data Distortion:** Incorrectly plotting data values, using misleading scales (e.g., truncated y-axis that exaggerates differences), or misrepresenting statistical relationships.
2.  **Label Fabrication:** Axis labels, legend entries, or annotations that don't match the raw data or brief description (e.g., wrong metric names, fabricated experiment conditions).
3.  **Missing Critical Information:** Completely omitting essential elements like axis labels, units, legends, or key data series mentioned in the brief description.
    *   **Important:** This rule applies to elements that are **completely absent**. If an element exists but is illegible due to poor styling (e.g., white-on-white text, insufficient contrast), evaluate it under **Readability**, not Faithfulness.
4.  **Wrong Chart Type:** Using a chart type that fundamentally misrepresents the data (e.g., using a pie chart for time-series data, or a line chart for categorical comparisons).
5.  **Gibberish Content:** Text labels containing nonsensical characters, garbled formulas, or unreadable symbols.
6.  **Fabricated Statistical Indicators:** Adding significance markers, confidence intervals, error bars, or other statistical annotations that are not supported by or present in the raw data or brief description.

# Decision Criteria
**CRITICAL**: Since the raw data is extracted from the Human plot, the Human plot is **always the ground truth** for faithfulness. The Model can only match or fail to match the Human's faithfulness.

Select the appropriate option:

-   **Both are good**: The Model plot successfully matches the Human plot's faithfulness. The Model accurately represents all data values, uses appropriate chart types, has correct labels, and avoids all Veto errors.
-   **Human**: The Model plot fails to match the Human plot's faithfulness. The Model commits one or more **Veto errors** or contains data inaccuracies that the Human plot does not have.

**Note**: "Model" and "Both are bad" are **not valid outcomes** for faithfulness evaluation, since the Human plot is definitionally faithful to the source data.

# Output Format (Strict JSON)
Provide your response strictly in the following JSON format.

The `comparison_reasoning` must be a single string following this structure:
"Faithfulness of Human: [Check data accuracy, labels, and Veto errors]; Faithfulness of Model: [Check data accuracy, labels, and Veto errors]; Conclusion: [Final verdict based on data representation and Veto Rules]."

\`\`\`json
{
    "comparison_reasoning": "Faithfulness of Human: [Always faithful as the ground truth]; Faithfulness of Model: [Check data accuracy, labels, and Veto errors against Human]; Conclusion: [Final verdict].",
    "winner": "Human" | "Both are good"
}
\`\`\`
```

### Conciseness

```
# Role
You are an expert judge in academic data visualization. Your task is to evaluate the **Conciseness** of a **Model-Generated Plot** compared to a **Human-Drawn Plot**.

# Inputs
1.  **Raw Data**: [raw structured data]
2.  **Plot Brief Description**: [a brief description of the plot type and content]
3.  **Human-Drawn Plot (Human)**: [image]
4.  **Model-Generated Plot (Model)**: [image]

# Core Definition: What is Conciseness?
**Conciseness** measures whether a plot contains **only the necessary information** to communicate the data effectively. A concise plot avoids **redundant or excessive content** that does not contribute to understanding the data.

**Important**: For statistical plots, conciseness is a **baseline requirement**. Most well-constructed plots are concise, and **ONLY** violations of the Veto Rules below constitute conciseness failures.

**What is NOT a conciseness issue**:
-   Grid lines, bounding boxes, or plot spines (these are standard stylistic elements)
-   Tick marks or minor ticks
-   Standard plot decorations that aid interpretation (e.g., error bars, confidence intervals)
-   Layout choices like subplot arrangements or aspect ratios (unless violating Veto Rule #2)
-   **Grid lines + data labels** (grid lines are spatial references, not redundant with explicit numerical labels)
-   **Axis scales + data labels** (axis provides range context, labels provide precision)
-   Any other minor stylistic differences in visual design

# Veto Rules (The "Red Lines")
**If a plot commits any of the following errors, it fails the conciseness test immediately:**
1.  **Redundant Labeling:** Displaying the exact same data values multiple times without purpose. Examples include:
    *   Both bar height AND numerical text labels on every bar **when there are many bars** (>=8 bars) and the y-axis scale is clear and provides sufficient precision
        *   **Exception:** For plots with few bars (< 8 bars), numerical labels are acceptable and not considered redundant
    *   Both a pie chart percentage label AND a separate legend showing the same percentages
    *   **Overly Verbose Labels:** X-tick labels that are excessively long phrases or full sentences, creating visual clutter and redundancy with the plot caption/description
    *   **Not redundant:** Grid lines/axes (structural elements) combined with data labels (precise values)
2.  **Unnecessary Subplots:** Breaking data into too many subplots when a single unified plot would be clearer and more efficient.
    *   **Not a violation:** Inset zooms, detail views, or subplots that specifically address data visibility issues (e.g., showing a data series that is otherwise invisible due to scale differences). These serve a functional purpose and are not redundant.
3.  **Text Overload:** Long verbose labels, overly detailed legends, or paragraph-length annotations that should belong in the caption.

# Decision Criteria
**CRITICAL**: Conciseness is a strict pass/fail criterion based **ONLY** on Veto Rules. If neither plot violates any Veto Rules, you **MUST** default to "Both are good".

Compare the two plots and select the strictly best option:
-   **Both are good**: **DEFAULT CHOICE**. Use this whenever both plots avoid all Veto Rules. Do NOT pick a winner based on stylistic differences such as grid line density, bounding box presence, spine visibility, or other visual design choices.
-   **Model**: Use ONLY if the Model avoids Veto violations while the Human commits one or more.
-   **Human**: Use ONLY if the Human avoids Veto violations while the Model commits one or more.
-   **Both are bad**: Use ONLY if BOTH plots violate one or more Veto Rules.

**Remember**: Grid lines, bounding boxes, spines, and similar elements are **NOT** conciseness issues. Only judge based on the three Veto Rules above.

# Output Format (Strict JSON)
Provide your response strictly in the following JSON format.

The `comparison_reasoning` must be a single string following this structure:
"Conciseness of Human: [Check for Veto Rule violations only]; Conciseness of Model: [Check for Veto Rule violations only]; Conclusion: [Final verdict based strictly on Veto Rules]."

\`\`\`json
{
    "comparison_reasoning": "Conciseness of Human: ...;\n Conciseness of Model: ...;\n Conclusion: ...",
    "winner": "Model" | "Human" | "Both are good" | "Both are bad"
}
\`\`\`
```

### Readability

```
# Role
You are an expert judge in academic data visualization. Your task is to evaluate the **Readability** of a **Model-Generated Plot** compared to a **Human-Drawn Plot**.

# Inputs
1.  **Plot Brief Description**: [a brief description of the plot type and content]
2.  **Human-Drawn Plot (Human)**: [image]
3.  **Model-Generated Plot (Model)**: [image]

# Core Definition: What is Readability?
**Readability** measures how easily a reader can **extract and interpret** the data and key findings from a plot. A readable plot must have clear axis labels with units, legible text, distinguishable colors/markers, an understandable legend, and minimal visual interference. The goal is instant comprehension without confusion.

**Important**: Readability is a **baseline requirement**. Most well-constructed academic plots are readable. Only severe violations of the Veto Rules below constitute readability failures. Minor stylistic differences should NOT be judged as readability issues.

# Veto Rules (The "Red Lines")
**If a plot commits any of the following errors, it fails the readability test immediately:**
1.  **Visual Noise & Extraneous Elements:**
    *   The Figure Title (e.g., "Figure 3: ...") or full caption text rendered within the image pixels.
        * *Note:* Subfigure labels like (a), (b) or panel titles are **permitted** and encouraged.
    *   Watermarks, logos, or other meta-information cluttering the plot area.
2.  **Missing or Unlabeled Axes:** Axes without labels or units, making it impossible to understand what is being measured.
3.  **Illegible Text:** Font sizes too small to read, text overlapping with data points/gridlines/other elements, or text with insufficient contrast against the background (e.g., black text on black background, dark text on dark background, white text on white background).
4.  **Poor Color Discrimination:** Using colors that are too similar to distinguish between data series, or using color schemes that are not colorblind-friendly when multiple series are present.
5.  **No Legend (when needed):** Multiple data series without a legend or with an unclear legend that doesn't identify what each line/bar represents.
6.  **Low Contrast:** Data elements (lines, bars, markers) that blend into the background, making them invisible or very hard to see.
7.  **Invisible Data Elements:** Data points, lines, or bars that are too small, too thin, or too transparent to be clearly visible.
8.  **Legend Blocking Data:** Legend positioned over critical data points or trends, obscuring important information.

# Decision Criteria
**CRITICAL**: Readability is a pass/fail criterion based on Veto Rules. If neither plot violates any Veto Rules, you **MUST** default to "Both are good".

Compare the two plots and select the strictly best option based solely on the **Core Definition** and **Veto Rules** above:

-   **Both are good**: **DEFAULT CHOICE**. Use this whenever both plots avoid all Veto Rules and are reasonably easy to interpret. Do NOT pick a winner based on minor stylistic preferences.
-   **Model**: Use ONLY if the Model avoids Veto violations while the Human commits one or more, OR if the Model is dramatically more readable.
-   **Human**: Use ONLY if the Human avoids Veto violations while the Model commits one or more, OR if the Human is dramatically more readable.
-   **Both are bad**: Use ONLY if BOTH plots violate one or more Veto Rules.

**Reminder**: If you find yourself hesitating between "Model"/"Human" and "Both are good", choose "Both are good". Reserve winner selection for cases with clear, substantial readability differences.

# Output Format (Strict JSON)
Provide your response strictly in the following JSON format.

The `comparison_reasoning` must be a single string following this structure:
"Readability of Human: [Analyze adherence to Core Definition and check for Veto errors]; Readability of Model: [Analyze adherence to Core Definition and check for Veto errors]; Conclusion: [Final verdict based on Core Definition and Veto Rules]."

\`\`\`json
{
    "comparison_reasoning": "Readability of Human: ...\n Readability of Model: ...\n Conclusion: ...",
    "winner": "Model" | "Human" | "Both are good" | "Both are bad"
}
\`\`\`
```

### Aesthetics

```
# Role
You are an expert judge in academic data visualization. Your task is to evaluate the **Aesthetics** of a **Model-Generated Plot** compared to a **Human-Drawn Plot**.

# Inputs
1.  **Plot Brief Description**: [a brief description of the plot type and content]
2.  **Human-Drawn Plot (Human)**: [image]
3.  **Model-Generated Plot (Model)**: [image]

# Core Definition: What is Aesthetics?
**Aesthetics** evaluates the **visual appeal** of a plot, including color schemes, font choices, line styles, layout harmony, and rendering quality. A high-aesthetic plot uses well-chosen colors, readable fonts, clean lines, and professional styling that meets publication standards.

**Important**: Academic visualization supports **diverse aesthetic styles**. When evaluating, recognize that:
-   **Legends are standard practice** - not inferior to direct labels; both can be aesthetic
-   **Outlines/borders vary by style** - black borders can look professional and clean; not "dated" by default
-   **Color palettes are diverse** - many color schemes work well; avoid only obvious unprofessional choices
-   **Some plots are intentionally playful** - a slightly "cartoonish" style is acceptable in modern academic work if well-executed
-   **Layout choices differ** - exploded slices, subplot arrangements, etc. are design decisions with trade-offs
-   **Hatching is beneficial** - texture patterns aid distinctions in black-and-white printing; this is a standard academic practice and should **not** be penalized as "visual clutter".
-   Removing the top and right spines should not be considered more aesthetic than using full-box border.
-   If both plots looks good, choose "Both are good". It's no need to pick a winner based on minor stylistic preferences.
-   **Grid lines are functional** - solid or visible grid lines help readability in complex plots; they should not be penalized compared with no grid lines or dashed grid lines unless they severely obscure data points.
-   **Fonts are flexible** - both serif (e.g., Times New Roman) and sans-serif (e.g., Arial, Helvetica) fonts are standard in academic papers; do **not** penalize sans-serif fonts as "generic".

Judge based on **overall visual harmony and professional quality**, not adherence to a single "minimalist" or "modern" aesthetic standard.

**Key Standards**: Publication-quality plots have vector graphics quality (no pixelation), avoid obviously unprofessional elements (neon colors, black backgrounds), and don't look like low-quality screenshots or amateur renderings.

# Veto Rules (The "Red Lines")
**If a plot commits any of the following errors, it fails the aesthetics test immediately:**
1.  **Low Quality Artifacts:** Obvious pixelation, blurry elements, jagged lines, or distorted shapes indicating poor rendering quality.
2.  **Unprofessional Color Schemes:** Using default Excel/Google Sheets/Matplotlib(yellow&blue) colors, extremely jarring neon colors, or severely poor contrasting color combinations.
3.  **Inconsistent Styling:** Mixing multiple obviously unrelated fonts, extremely inconsistent line widths, or clearly mismatched marker styles across similar data series.
4.  **Default Software Appearance:** Plots that look like completely unmodified default output from matplotlib, Excel, or other tools with zero styling effort.
5.  **Black Background:** Using black as the background color, which violates academic publication standards and appears unprofessional.
6.  **Excessive 3D Effects:** Gratuitous 3D rendering, shadows, or perspective that adds no value and makes the plot look unprofessional.
    *   **Note:** If 3D effects severely distort data interpretation or misrepresent data relationships, evaluate under **Faithfulness** instead.
7.  **Aspect Ratio Distortion:** Severe distortion of shapes (e.g., circles rendered as ellipses, squares as rectangles) that makes the plot look unprofessional.
    *   **Exception:** In academic papers, **truncating the y-axis** (not starting at 0) is standard practice to make subtle performance differences visible. Do **not** penalize this as a distortion; conversely, starting at 0 when all values are high (e.g., >80%) is often less informative.

# Decision Criteria
Compare the two plots and select the strictly best option based solely on the **Core Definition** and **Veto Rules** above.

-   **Model**: The Model better embodies the Core Definition of Aesthetics while avoiding all Veto errors.
-   **Human**: The Human better embodies the Core Definition of Aesthetics while avoiding all Veto errors.
-   **Both are good**: Both plots successfully embody the Core Definition of Aesthetics without any Veto errors and meet publication standards.
-   **Both are bad**: BOTH plots violate one or more **Veto Rules** or fail to meet publication quality standards.

# Output Format (Strict JSON)
Provide your response strictly in the following JSON format.

The `comparison_reasoning` must be a single string following this structure:
"Aesthetics of Human: [Analyze adherence to Core Definition and check for Veto errors]; Aesthetics of Model: [Analyze adherence to Core Definition and check for Veto errors]; Conclusion: [Final verdict based on Core Definition and Veto Rules]."

\`\`\`json
{
    "comparison_reasoning": "Aesthetics of Human: ...\n Aesthetics of Model: ...\n Conclusion: ...",
    "winner": "Model" | "Human" | "Both are good" | "Both are bad"
}
\`\`\`
```
