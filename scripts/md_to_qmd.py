#!/usr/bin/env python3
"""
Markdown to QMD Conversion Script for OECD Test Guidelines

Converts extracted markdown to structured QMD format with proper frontmatter,
heading analysis, table placeholder processing, and formula conversion to LaTeX.
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple
from datetime import datetime
from convert_formulas import FormulaConverter


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
                            doc_number: str = "XXX") -> None:
    """
    Convert extracted markdown to QMD format with formula conversion.

    Args:
        md_path: Path to input markdown file
        output_qmd: Path to output QMD file
        title: Document title
        doc_number: Document number
    """
    # Initialize formula converter
    formula_converter = FormulaConverter()

    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Create frontmatter
    today = datetime.now().strftime("%Y-%m-%d")
    frontmatter = f"""---
title: "OECD测试指南第{doc_number}号：{title}"
subtitle: "{title}"
author: "OECD (经济合作与发展组织)"
date: "{today}"
description: "OECD化学品测试指南 - {title}"
keywords: [OECD, 测试指南, 毒理学, 体外测试]
lang: zh-CN
format:
  html:
    toc: true
    number-sections: true
  pdf:
    toc: true
    number-sections: true
---

# 文档信息

| 属性 | 内容 |
|------|------|
| **指南编号** | 第{doc_number}号 |
| **文档类型** | OECD测试指南 |
| **主题** | {title} |

---

# 原文内容

"""

    # Process content
    processed_lines = []
    table_counter = 0

    for i, line in enumerate(lines):
        prev_line = lines[i - 1] if i > 0 else ""
        next_line = lines[i + 1] if i < len(lines) - 1 else ""

        # Process table placeholders
        if '[TABLE:' in line:
            table_counter += 1
            table_id = f"table_{table_counter}"
            processed_lines.append(f"\n![表格 {table_counter}](images/{table_id}.png){{#tbl-{table_counter}}}\n\n")
            continue

        # Analyze and convert headings
        is_heading, level = analyze_heading_quality(line.strip(),
                                                     prev_line.strip(),
                                                     next_line.strip())

        if is_heading and not line.strip().startswith('#'):
            # Convert to heading
            content = line.strip()
            # Capitalize first letter of each word
            content = ' '.join(word.capitalize() for word in content.split())
            processed_lines.append(f"{level}{content}\n\n")
        else:
            # Apply formula conversion to non-heading lines
            converted_line = formula_converter.convert_inline_formulas(line)
            processed_lines.append(converted_line)

    # Write QMD file
    with open(output_qmd, 'w', encoding='utf-8') as f:
        f.write(frontmatter)
        f.writelines(processed_lines)

    print(f"✅ Processed {len(lines)} lines")
    print(f"   - Tables referenced: {table_counter}")
    print(f"   - Output: {output_qmd}")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python md_to_qmd.py <md_path> [output_qmd] [title] [doc_number]")
        sys.exit(1)

    md_path = sys.argv[1]

    if len(sys.argv) >= 4:
        output_qmd = sys.argv[2]
        title = sys.argv[3]
    elif len(sys.argv) >= 3:
        output_qmd = sys.argv[2]
        title = "OECD Test Guideline"
    else:
        output_qmd = str(Path(md_path).stem) + ".qmd"
        title = "OECD Test Guideline"

    doc_number = sys.argv[4] if len(sys.argv) >= 5 else "XXX"

    print(f"Converting: {md_path}")
    print(f"Title: {title}")
    print(f"Document number: {doc_number}")

    convert_markdown_to_qmd(md_path, output_qmd, title, doc_number)


if __name__ == "__main__":
    main()
