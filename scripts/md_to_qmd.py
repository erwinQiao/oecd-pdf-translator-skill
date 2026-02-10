#!/usr/bin/env python3
"""
Markdown to QMD Conversion Script for OECD Test Guidelines

Converts extracted markdown to structured QMD format with proper frontmatter,
heading analysis, table placeholder processing, and formula conversion to LaTeX.
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple, Optional
from datetime import datetime
from convert_formulas import FormulaConverter


# Default template path
DEFAULT_TEMPLATE_PATH = Path(__file__).parent.parent / "assets" / "template.qmd"


def load_template(template_path: Optional[Path] = None) -> str:
    """
    Load QMD template file.

    Args:
        template_path: Path to template file. Uses default if None.

    Returns:
        Template content as string

    Raises:
        FileNotFoundError: If template file doesn't exist
    """
    if template_path is None:
        template_path = DEFAULT_TEMPLATE_PATH

    if not template_path.exists():
        raise FileNotFoundError(f"Template file not found: {template_path}")

    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()


def fill_template(template: str, **kwargs) -> str:
    """
    Fill template placeholders with provided values.

    Args:
        template: Template content with {{PLACEHOLDER}} variables
        **kwargs: Key-value pairs for placeholder replacement

    Returns:
        Filled template content
    """
    content = template
    for key, value in kwargs.items():
        placeholder = "{{" + key + "}}"
        content = content.replace(placeholder, str(value))
    return content


def analyze_heading_quality(line: str, prev_line: str, next_line: str) -> Tuple[bool, str]:
    """
    Analyze if a line should be a heading using multi-method approach.

    Args:
        line: Current line to analyze
        prev_line: Previous line
        next_line: Next line

    Returns:
        Tuple of (is_heading, heading_level)
    """
    line = line.strip()

    # Skip empty lines
    if not line:
        return False, ""

    # Already a markdown heading
    if line.startswith('#'):
        level = len(re.match(r'^#+', line).group())
        return True, f"{'#' * min(level, 6)} "

    # Method 1: Format analysis
    # Check for ALL CAPS short lines (common in OECD docs)
    if len(line) < 100 and line.isupper() and not line.endswith('.'):
        # Likely a heading
        if len(line.split()) <= 10:  # Short phrases
            return True, "## "

    # Method 2: Content analysis
    # Check for common section markers
    heading_patterns = [
        r'^(INTRODUCTION|PRINCIPLE|DESCRIPTION|PREPARATION|PROCEDURE)',
        r'^(DEFINITIONS|LITERATURE|ANNEX)',
        r'^(Test conditions|Controls|Results|Discussion)',
        r'^(Initial Consideration|Principle of the Test Method)',
        r'^(Irradiation Conditions|Dosimetry|Interpretation)',
        r'^(Evaluation of Results|Test Report)',
    ]

    for pattern in heading_patterns:
        if re.match(pattern, line, re.IGNORECASE):
            return True, "### "

    # Check: Short lines without ending punctuation
    if len(line) < 80 and not line.endswith(('.', ',', ';', ':')):
        # Check context
        words = line.split()
        if 2 <= len(words) <= 8:  # Likely a heading
            # Check if surrounded by blank lines
            prev_blank = not prev_line.strip() or prev_line.strip() == ""
            next_blank = not next_line.strip() or next_line.strip() == ""
            if prev_blank or next_blank:
                return True, "### "

    return False, ""


def convert_markdown_to_qmd(md_path: str, output_qmd: str,
                            title: str = "OECD Test Guideline",
                            doc_number: str = "XXX",
                            template_path: Optional[Path] = None,
                            publication_date: str = "") -> None:
    """
    Convert extracted markdown to QMD format with formula conversion.

    Args:
        md_path: Path to input markdown file
        output_qmd: Path to output QMD file
        title: Document title
        doc_number: Document number
        template_path: Optional path to custom template file
        publication_date: Original publication date from PDF
    """
    # Initialize formula converter
    formula_converter = FormulaConverter()

    # Load template
    template = load_template(template_path)

    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Process content
    processed_lines = []
    table_counter = 0
    references_lines = []
    in_references = False

    # Pattern to detect reference section headings
    ref_pattern = re.compile(
        r'^(#{1,3}\s*)?(Literature|References|参考文献|文献)$',
        re.IGNORECASE
    )

    for i, line in enumerate(lines):
        prev_line = lines[i - 1] if i > 0 else ""
        next_line = lines[i + 1] if i < len(lines) - 1 else ""

        # Check if this is a references section heading
        line_stripped = line.strip()
        if ref_pattern.match(line_stripped):
            in_references = True

        # Process table placeholders
        if '[TABLE:' in line:
            table_counter += 1
            table_id = f"table_{table_counter}"
            if in_references:
                references_lines.append(f"\n![表格 {table_counter}](images/{table_id}.png){{#tbl-{table_counter}}}\n\n")
            else:
                processed_lines.append(f"\n![表格 {table_counter}](images/{table_id}.png){{#tbl-{table_counter}}}\n\n")
            continue

        # Analyze and convert headings
        is_heading, level = analyze_heading_quality(line_stripped,
                                                     prev_line.strip(),
                                                     next_line.strip())

        if is_heading and not line_stripped.startswith('#'):
            # Convert to heading
            content = line_stripped
            # Capitalize first letter of each word
            content = ' '.join(word.capitalize() for word in content.split())
            converted_line = f"{level}{content}\n\n"
        else:
            # Apply formula conversion to non-heading lines
            converted_line = formula_converter.convert_inline_formulas(line)

        # Add to appropriate section
        # Skip the references heading itself from main content
        if in_references and not ref_pattern.match(line_stripped):
            references_lines.append(converted_line)
        elif not in_references:
            processed_lines.append(converted_line)

    # Prepare template variables
    today = datetime.now().strftime("%Y-%m-%d")
    content = ''.join(processed_lines).strip()
    references = ''.join(references_lines).strip() if references_lines else "参见原文末尾参考文献列表"

    template_vars = {
        'DOC_NUMBER': doc_number,
        'TITLE': title,
        'DATE': today,
        'PUBLICATION_DATE': publication_date or "未知",
        'CONTENT': content,
        'REFERENCES': references,
    }

    # Fill template and write output
    filled_template = fill_template(template, **template_vars)

    with open(output_qmd, 'w', encoding='utf-8') as f:
        f.write(filled_template)

    print(f"✅ Processed {len(lines)} lines")
    print(f"   - Tables referenced: {table_counter}")
    print(f"   - Output: {output_qmd}")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python md_to_qmd.py <md_path> [output_qmd] [title] [doc_number] [template_path] [publication_date]")
        print("")
        print("Arguments:")
        print("  md_path          Path to input markdown file (required)")
        print("  output_qmd       Path to output QMD file (optional)")
        print("  title            Document title (optional)")
        print("  doc_number       Document number (optional)")
        print("  template_path    Path to custom template file (optional)")
        print("  publication_date Original publication date (optional)")
        print("")
        print("Examples:")
        print("  python md_to_qmd.py input.md")
        print("  python md_to_qmd.py input.md output.qmd")
        print("  python md_to_qmd.py input.md output.qmd 'My Title' '432'")
        print("  python md_to_qmd.py input.md output.qmd 'My Title' '432' '../custom_template.qmd'")
        print("  python md_to_qmd.py input.md output.qmd 'My Title' '432' '' '18 June 2019'")
        sys.exit(1)

    md_path = sys.argv[1]

    # Parse arguments
    output_qmd = sys.argv[2] if len(sys.argv) >= 3 else str(Path(md_path).stem) + ".qmd"
    title = sys.argv[3] if len(sys.argv) >= 4 else "OECD Test Guideline"
    doc_number = sys.argv[4] if len(sys.argv) >= 5 else "XXX"
    template_path = Path(sys.argv[5]) if len(sys.argv) >= 6 and sys.argv[5] else None
    publication_date = sys.argv[6] if len(sys.argv) >= 7 else ""

    print(f"Converting: {md_path}")
    print(f"Output: {output_qmd}")
    print(f"Title: {title}")
    print(f"Document number: {doc_number}")
    if template_path:
        print(f"Template: {template_path}")
    if publication_date:
        print(f"Publication date: {publication_date}")

    convert_markdown_to_qmd(md_path, output_qmd, title, doc_number, template_path, publication_date)


if __name__ == "__main__":
    main()
