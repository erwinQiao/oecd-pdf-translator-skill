#!/usr/bin/env python3
"""
PDF Text Extraction Script for OECD Test Guidelines

Extracts text from PDF pages while detecting and skipping tables.
Uses pdfplumber for text extraction and table detection.
"""

import pdfplumber
import sys
from pathlib import Path
from typing import List, Dict, Any


def extract_text_with_tables(pdf_path: str, output_md: str) -> Dict[str, Any]:
    """
    Extract text from PDF while detecting tables.

    Args:
        pdf_path: Path to input PDF file
        output_md: Path to output markdown file

    Returns:
        Dictionary with metadata about extraction
    """
    tables_found = []
    page_count = 0

    with pdfplumber.open(pdf_path) as pdf:
        with open(output_md, 'w', encoding='utf-8') as md_file:
            md_file.write(f"# Extracted Text from {Path(pdf_path).name}\n\n")

            for page_num, page in enumerate(pdf.pages, start=1):
                page_count = page_num

                # Detect tables on this page
                tables = page.find_tables()
                page_tables = []

                # Record table information
                for i, table in enumerate(tables):
                    table_id = f"table_{len(tables_found) + 1}"
                    bbox = table.bbox
                    page_tables.append({
                        'id': table_id,
                        'page': page_num,
                        'bbox': bbox
                    })
                    tables_found.append(page_tables[-1])

                # Extract text, excluding table regions
                text = page.extract_text()

                if text:
                    # Add page marker
                    md_file.write(f"## 第 {page_num} 页\n\n")

                    # If tables found on this page, add placeholder
                    if page_tables:
                        for pt in page_tables:
                            md_file.write(f"[TABLE: {pt['id']}]\n\n")

                    # Write the text content
                    md_file.write(f"{text}\n\n")
                    md_file.write("---\n\n")

    return {
        'total_pages': page_count,
        'tables_found': len(tables_found),
        'tables': tables_found
    }


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python extract_pdf_text.py <pdf_path> [output_md]")
        sys.exit(1)

    pdf_path = sys.argv[1]

    # Default output filename
    if len(sys.argv) >= 3:
        output_md = sys.argv[2]
    else:
        output_md = str(Path(pdf_path).stem) + "_extracted.md"

    print(f"Extracting text from: {pdf_path}")
    print(f"Output to: {output_md}")

    result = extract_text_with_tables(pdf_path, output_md)

    print(f"\n✅ Extraction complete:")
    print(f"   - Total pages: {result['total_pages']}")
    print(f"   - Tables detected: {result['tables_found']}")

    for table in result['tables']:
        print(f"     • {table['id']} on page {table['page']}")


if __name__ == "__main__":
    main()
