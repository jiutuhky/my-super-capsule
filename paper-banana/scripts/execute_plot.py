#!/usr/bin/env python3
"""
PaperBanana Plot Executor - Safe matplotlib Code Execution

Executes matplotlib Python code and saves the resulting plot as a JPEG image.
Extracted from PaperBanana's visualizer_agent.py:30-60.

Usage:
    python execute_plot.py --code-file /path/to/code.py [--output PATH]
    python execute_plot.py --code "import matplotlib..." [--output PATH]
    echo "import matplotlib..." | python execute_plot.py --code - [--output PATH]
"""

import argparse
import io
import re
import sys
import time

from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Execute matplotlib code and save plot as JPEG"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--code-file",
        help="Path to a Python file containing matplotlib code"
    )
    group.add_argument(
        "--code",
        help="Inline Python code string (use '-' to read from stdin)"
    )
    parser.add_argument(
        "--output", default=None,
        help="Output file path (default: ./paper_banana_output/plot_{timestamp}.jpg)"
    )
    return parser.parse_args()


def ensure_output_path(output_arg):
    """Determine and create the output file path."""
    if output_arg:
        out_path = Path(output_arg).resolve()
    else:
        out_dir = Path.cwd() / "paper_banana_output"
        out_dir.mkdir(parents=True, exist_ok=True)
        timestamp = int(time.time())
        out_path = out_dir / f"plot_{timestamp}.jpg"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    return out_path


def extract_python_code(code_text: str) -> str:
    """
    Extract Python code from markdown code blocks if present.
    Logic from visualizer_agent.py:37-38.
    """
    match = re.search(r"```python(.*?)```", code_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return code_text.strip()


def execute_and_save(code_text: str, output_path: Path) -> bool:
    """
    Execute matplotlib code and save the resulting figure as JPEG.
    Logic from visualizer_agent.py:30-60.

    Returns True on success, False on failure.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    code_clean = extract_python_code(code_text)

    # Reset matplotlib state
    plt.switch_backend("Agg")
    plt.close("all")
    plt.rcdefaults()

    try:
        exec_globals = {}
        exec(code_clean, exec_globals)

        if not plt.get_fignums():
            print("Error: Code executed but no matplotlib figure was created.", file=sys.stderr)
            return False

        # Save as JPEG
        buf = io.BytesIO()
        plt.savefig(buf, format="jpeg", bbox_inches="tight", dpi=300)
        plt.close("all")

        buf.seek(0)
        output_path.write_bytes(buf.read())
        return True

    except Exception as e:
        print(f"Error executing plot code: {e}", file=sys.stderr)
        return False


def main():
    args = parse_args()
    out_path = ensure_output_path(args.output)

    # Read code from the specified source
    if args.code_file:
        code_file = Path(args.code_file)
        if not code_file.exists():
            print(f"Error: File not found: {code_file}", file=sys.stderr)
            sys.exit(1)
        code_text = code_file.read_text(encoding="utf-8")
    elif args.code == "-":
        code_text = sys.stdin.read()
    else:
        code_text = args.code

    if not code_text.strip():
        print("Error: No code provided.", file=sys.stderr)
        sys.exit(1)

    success = execute_and_save(code_text, out_path)
    if success:
        # Print absolute path to stdout for caller to capture
        print(str(out_path.resolve()))
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
