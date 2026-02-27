#!/usr/bin/env python3
"""
PaperBanana Diagram Generator - Gemini Image Generation API Wrapper

Generates scientific diagrams using Google's Gemini image generation model.
Extracted from PaperBanana's visualizer_agent.py and generation_utils.py.

Usage:
    python generate_diagram.py \
        --description "Detailed diagram description text" \
        [--model "gemini-2.0-flash-preview-image-generation"] \
        [--aspect-ratio "16:9"] \
        [--output PATH]
"""

import argparse
import asyncio
import base64
import io
import os
import sys
import time

from pathlib import Path

DEFAULT_MODEL = "gemini-3-pro-image-preview"
DEFAULT_ASPECT_RATIO = "1:1"
DEFAULT_IMAGE_SIZE = "4K"
VALID_ASPECT_RATIOS = ["21:9", "16:9", "3:2", "1:1"]
VALID_IMAGE_SIZES = ["1K", "2K", "4K"]

# Prompts preserved verbatim from visualizer_agent.py
SYSTEM_INSTRUCTION = (
    "You are an expert scientific diagram illustrator. "
    "Generate high-quality scientific diagrams based on user requests."
)
PROMPT_TEMPLATE = (
    "Render an image based on the following detailed description: {desc}\n"
    " Note that do not include figure titles in the image. Diagram: "
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate scientific diagrams via Gemini image generation API"
    )
    parser.add_argument(
        "--description", required=True,
        help="Detailed diagram description text"
    )
    parser.add_argument(
        "--model", default=DEFAULT_MODEL,
        help=f"Gemini model name (default: {DEFAULT_MODEL})"
    )
    parser.add_argument(
        "--aspect-ratio", default=DEFAULT_ASPECT_RATIO,
        choices=VALID_ASPECT_RATIOS,
        help=f"Output aspect ratio (default: {DEFAULT_ASPECT_RATIO})"
    )
    parser.add_argument(
        "--image-size", default=DEFAULT_IMAGE_SIZE,
        choices=VALID_IMAGE_SIZES,
        help=f"Output image size (default: {DEFAULT_IMAGE_SIZE})"
    )
    parser.add_argument(
        "--output", default=None,
        help="Output file path (default: ./paper_banana_output/diagram_{timestamp}.jpg)"
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
        out_path = out_dir / f"diagram_{timestamp}.jpg"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    return out_path


def convert_png_b64_to_jpg_bytes(png_b64_str: str) -> bytes:
    """
    Convert a base64-encoded PNG (from Gemini) to JPEG bytes.
    Logic from image_utils.py:24-46.
    """
    from PIL import Image as PILImage

    raw_bytes = base64.b64decode(png_b64_str)
    img = PILImage.open(io.BytesIO(raw_bytes)).convert("RGB")
    out_io = io.BytesIO()
    img.save(out_io, format="JPEG", quality=95)
    return out_io.getvalue()


async def generate_image(description: str, model: str, aspect_ratio: str, image_size: str = "1K", max_attempts: int = 5):
    """
    Call Gemini image generation API with retry logic.
    Extracted from generation_utils.py:100-182 and visualizer_agent.py:91-199.
    """
    from google import genai
    from google.genai import types

    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    base_url = os.environ.get("GOOGLE_API_BASE_URL")
    client_kwargs = {"api_key": api_key}
    if base_url:
        client_kwargs["http_options"] = types.HttpOptions(base_url=base_url)
        print(f"Using custom base URL: {base_url}", file=sys.stderr)

    client = genai.Client(**client_kwargs)

    prompt_text = PROMPT_TEMPLATE.format(desc=description)

    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        temperature=1.0,
        candidate_count=1,
        max_output_tokens=50000,
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(
            aspect_ratio=aspect_ratio,
            image_size=image_size,
        ),
    )

    retry_delay = 5
    for attempt in range(max_attempts):
        try:
            response = await client.aio.models.generate_content(
                model=model,
                contents=prompt_text,
                config=config,
            )

            if (
                not response.candidates
                or not response.candidates[0].content.parts
            ):
                print(
                    f"Warning: Empty response on attempt {attempt + 1}, "
                    f"retrying in {retry_delay}s...",
                    file=sys.stderr,
                )
                await asyncio.sleep(retry_delay)
                continue

            # Extract image data from response
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    b64_data = base64.b64encode(part.inline_data.data).decode("utf-8")
                    return b64_data

            print(
                f"Warning: No image data in response on attempt {attempt + 1}, "
                f"retrying in {retry_delay}s...",
                file=sys.stderr,
            )
            await asyncio.sleep(retry_delay)

        except Exception as e:
            current_delay = min(retry_delay * (2 ** attempt), 30)
            print(
                f"Attempt {attempt + 1}/{max_attempts} failed: {e}. "
                f"Retrying in {current_delay}s...",
                file=sys.stderr,
            )
            if attempt < max_attempts - 1:
                await asyncio.sleep(current_delay)
            else:
                print(f"Error: All {max_attempts} attempts failed.", file=sys.stderr)
                return None

    return None


async def main_async():
    args = parse_args()
    out_path = ensure_output_path(args.output)

    b64_image = await generate_image(
        description=args.description,
        model=args.model,
        aspect_ratio=args.aspect_ratio,
        image_size=args.image_size,
    )

    if not b64_image:
        print("Error: Failed to generate image.", file=sys.stderr)
        sys.exit(1)

    # Convert to JPEG and save
    try:
        jpg_bytes = convert_png_b64_to_jpg_bytes(b64_image)
    except Exception as e:
        print(f"Error converting image: {e}", file=sys.stderr)
        sys.exit(1)

    out_path.write_bytes(jpg_bytes)
    # Print absolute path to stdout for caller to capture
    print(str(out_path.resolve()))


def main():
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
