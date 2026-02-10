#!/usr/bin/env python3
"""
Main Workflow Script for OECD PDF to Chinese QMD Conversion

Orchestrates all steps: text extraction, image/table extraction,
QMD generation, translation, and cleanup.
"""

import sys
import os
import shutil
from pathlib import Path
import subprocess


def run_command(cmd: list, description: str) -> bool:
    """Run a command and return success status."""
    print(f"\n{'='*60}")
    print(f"Step: {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(e.stderr)
        return False


def process_oecd_pdf(pdf_path: str, output_dir: str = None,
                    title: str = None, doc_number: str = None) -> None:
    """
    Complete workflow to process OECD PDF to Chinese QMD.

    Args:
        pdf_path: Path to input PDF file
        output_dir: Output directory (default: current directory)
        title: Document title (extracted from PDF if not provided)
        doc_number: Document number (extracted from PDF if not provided)
    """
    pdf_path = Path(pdf_path).resolve()

    if not pdf_path.exists():
        print(f"❌ Error: PDF file not found: {pdf_path}")
        sys.exit(1)

    # Setup output directory
    if output_dir is None:
        output_dir = pdf_path.parent
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)

    print(f"\n{'='*60}")
    print(f"OECD PDF to Chinese QMD Converter")
    print(f"{'='*60}")
    print(f"Input PDF: {pdf_path.name}")
    print(f"Output directory: {output_dir}")

    # Extract document number and title from filename if not provided
    if doc_number is None:
        # Try to extract from filename (e.g., "OECD_432_..." -> "432")
        import re
        match = re.search(r'(\d{3})', pdf_path.name)
        doc_number = match.group(1) if match else "XXX"

    if title is None:
        title = f"OECD Test Guideline No. {doc_number}"

    # Paths
    scripts_dir = Path(__file__).parent
    temp_md = output_dir / f"{pdf_path.stem}_temp.md"
    extracted_md = output_dir / f"{pdf_path.stem}_extracted.md"
    images_dir = output_dir / "images"
    english_qmd = output_dir / f"{pdf_path.stem}_英文.qmd"
    chinese_qmd = output_dir / f"{pdf_path.stem}_中文.qmd"

    # Step 1: Extract text with table detection
    success = run_command([
        sys.executable,
        str(scripts_dir / "extract_pdf_text.py"),
        str(pdf_path),
        str(extracted_md)
    ], "1. Extract text from PDF (detecting tables)")

    if not success:
        print("❌ Failed to extract text")
        sys.exit(1)

    # Step 2: Extract images and tables
    success = run_command([
        sys.executable,
        str(scripts_dir / "extract_pdf_images.py"),
        str(pdf_path),
        str(images_dir)
    ], "2. Extract images and table screenshots")

    if not success:
        print("❌ Failed to extract images/tables")
        sys.exit(1)

    # Step 3: Convert to QMD (English)
    success = run_command([
        sys.executable,
        str(scripts_dir / "md_to_qmd.py"),
        str(extracted_md),
        str(english_qmd),
        title,
        doc_number
    ], "3. Convert markdown to English QMD")

    if not success:
        print("❌ Failed to convert to QMD")
        sys.exit(1)

    # Step 4: Translate to Chinese
    # Detect if running in Claude Code environment
    translation_method = os.getenv('CLAUDE_CODE_TRANSLATION', 'claude-code')

    success = run_command([
        sys.executable,
        str(scripts_dir / "translate_qmd.py"),
        str(english_qmd),
        str(chinese_qmd),
        translation_method
    ], f"4. Translate QMD to Chinese with terminology (method: {translation_method})")

    if not success:
        print("❌ Failed to translate")
        sys.exit(1)

    # Step 5: Cleanup intermediate files
    print(f"\n{'='*60}")
    print("Step: 5. Cleanup intermediate files")
    print(f"{'='*60}")

    files_to_remove = [
        temp_md,
        extracted_md,
    ]

    for file in files_to_remove:
        if file.exists():
            file.unlink()
            print(f"  🗑️  Removed: {file.name}")

    # Summary
    print(f"\n{'='*60}")
    print("✅ Processing complete!")
    print(f"{'='*60}")
    print(f"\nOutput files:")
    print(f"  📄 {english_qmd.name}")
    print(f"  📄 {chinese_qmd.name}")
    print(f"  📁 {images_dir.name}/")
    print(f"\nTotal items in {images_dir.name}/: {len(list(images_dir.glob('*')))}")

    # Translation completion notice
    if translation_method == "claude-code":
        request_file = chinese_qmd.parent / f"{chinese_qmd.stem}_translation_request.txt"
        if request_file.exists():
            print(f"\n{'='*60}")
            print("📝 Full Translation Required")
            print(f"{'='*60}")
            print(f"\n⚠️  The current Chinese file contains terminology replacements only.")
            print(f"   To complete the full translation, ask Claude Code:")
            print(f"\n   \"Please complete the full translation of {chinese_qmd.name}\"")
            print(f"\n   Or read the translation request file:")
            print(f"   📋 {request_file.name}")
            print(f"\n💡 Tip: For best results, specify:")
            print(f"   \"Translate this QMD file to Chinese using accurate")
            print(f"    toxicology terminology. Preserve all formatting.\"")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python process_oecd_pdf.py <pdf_path> [output_dir] [title] [doc_number]")
        print("\nExample:")
        print("  python process_oecd_pdf.py 9789264071162-en.pdf")
        print("  python process_oecd_pdf.py OECD_432.pdf ./output \"In Vitro 3T3 NRU Phototoxicity Test\" 432")
        print("\nTranslation Methods:")
        print("  Set CLAUDE_CODE_TRANSLATION environment variable:")
        print("  - claude-code: Creates translation request for Claude Code (default)")
        print("  - claude: Uses Anthropic API if available, otherwise term-only")
        print("  - anthropic: Uses Anthropic API directly")
        print("  - openai: Uses OpenAI API")
        print("\nExample with translation method:")
        print("  export CLAUDE_CODE_TRANSLATION=claude-code")
        print("  python process_oecd_pdf.py input.pdf")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) >= 3 else None
    title = sys.argv[3] if len(sys.argv) >= 4 else None
    doc_number = sys.argv[4] if len(sys.argv) >= 5 else None

    process_oecd_pdf(pdf_path, output_dir, title, doc_number)


if __name__ == "__main__":
    main()
