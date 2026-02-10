#!/usr/bin/env python3
"""
PDF Image and Table Extraction Script for OECD Test Guidelines

Extracts images and table screenshots from PDF pages.
Skips page 1, filters solid black/white images, and saves to images/ folder.
"""

import pdfplumber
import fitz  # PyMuPDF
import numpy as np
from PIL import Image
import io
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Any


def is_solid_color(image: Image.Image, variance_threshold: float = 1.0,
                   black_threshold: int = 15, white_threshold: int = 240,
                   use_edge_detection: bool = True) -> Tuple[bool, str]:
    """
    Check if image is solid black or white using multi-layered analysis.

    Enhanced with edge detection and content density analysis for better
    handling of scientific charts and graphs with white backgrounds.

    Args:
        image: PIL Image to check
        variance_threshold: Maximum variance for solid color (default 1.0)
        black_threshold: Max avg pixel value for black (default 15)
        white_threshold: Min avg pixel value for white (default 240)
        use_edge_detection: Use edge detection for better accuracy (default True)

    Returns:
        Tuple of (is_solid, reason)
    """
    # Convert to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Convert to numpy array
    img_array = np.array(image)

    # ===== Layer 1: Basic variance check =====
    variance = np.var(img_array)
    if variance < variance_threshold:
        return True, f"Low variance ({variance:.4f} < {variance_threshold})"

    # ===== Layer 2: Content density analysis =====
    # Calculate non-white pixel ratio (more lenient threshold)
    # Scientific charts often have < 20% ink (lines, text, data points)
    non_white_ratio = np.sum(img_array < 230) / img_array.size

    # If image has substantial content (> 5%), it's likely valid
    if non_white_ratio > 0.05:
        return False, f"Valid content ({non_white_ratio*100:.1f}% non-white)"

    # ===== Layer 3: Edge detection for scientific charts =====
    if use_edge_detection:
        # Convert to grayscale for edge detection
        if len(img_array.shape) == 3:
            gray = np.mean(img_array, axis=2).astype(np.uint8)
        else:
            gray = img_array.astype(np.uint8)

        # Simple gradient-based edge detection (Sobel-like)
        # Calculate gradients in x and y directions
        gradient_x = np.abs(gray[:-1, :-1].astype(np.int16) - gray[:-1, 1:].astype(np.int16))
        gradient_y = np.abs(gray[:-1, :-1].astype(np.int16) - gray[1:, :-1].astype(np.int16))
        gradient_magnitude = np.maximum(gradient_x, gradient_y)

        # Count edge pixels (gradients > 15)
        edge_pixels = np.sum(gradient_magnitude > 15)
        edge_ratio = edge_pixels / gradient_magnitude.size

        # If significant edges detected (> 1%), it's likely a chart/graph
        if edge_ratio > 0.01:
            return False, f"Has edges ({edge_ratio*100:.1f}% edge pixels)"

    # ===== Layer 4: Color range check (final filter) =====
    avg_pixel = np.mean(img_array)
    if avg_pixel < black_threshold:
        return True, f"Solid black (avg={avg_pixel:.2f} < {black_threshold})"

    # Only flag as solid white if both:
    # 1. Very high average (> 245, increased from 240)
    # 2. Very low content density (< 2%)
    if avg_pixel > 245 and non_white_ratio < 0.02:
        return True, f"Solid white (avg={avg_pixel:.2f} > 245, content={non_white_ratio*100:.1f}%)"

    # Passed all checks - likely a valid image with white background
    return False, f"Valid image (avg={avg_pixel:.1f}, content={non_white_ratio*100:.1f}%)"


def extract_images_and_tables(pdf_path: str, images_dir: str,
                              variance_threshold: float = 1.0) -> Dict[str, Any]:
    """
    Extract images and table screenshots from PDF.

    Args:
        pdf_path: Path to input PDF file
        images_dir: Directory to save extracted images
        variance_threshold: Variance threshold for solid color filtering

    Returns:
        Dictionary with extraction metadata
    """
    images_path = Path(images_dir)
    images_path.mkdir(exist_ok=True)

    # Open PDF with both libraries
    pdf_doc = fitz.open(pdf_path)
    pdf_plumber = pdfplumber.open(pdf_path)

    figure_count = 0
    table_count = 0
    filtered_images = []
    filtered_tables = []

    # Process pages (skip page 1, start from page 2 which is index 1)
    for page_num in range(1, len(pdf_doc)):
        page_index = page_num  # fitz uses 0-based index
        plumber_page = pdf_plumber.pages[page_index]

        print(f"Processing page {page_num + 1}...")

        # Extract regular images using PyMuPDF
        image_list = pdf_doc[page_index].get_images(full=True)
        for img_index, img in enumerate(image_list):
            base_image = pdf_doc.extract_image(img[0])
            image_bytes = base_image["image"]

            # Convert to PIL Image
            pil_image = Image.open(io.BytesIO(image_bytes))

            # Check if solid color (with edge detection enabled)
            is_solid, reason = is_solid_color(pil_image, variance_threshold,
                                             use_edge_detection=True)

            if is_solid:
                filtered_images.append({
                    'page': page_num + 1,
                    'image_index': img_index,
                    'reason': reason
                })
                continue

            # Save valid image
            figure_count += 1
            image_filename = images_path / f"figure_{figure_count}.png"
            pil_image.save(image_filename, 'PNG')
            print(f"  ✅ Saved: {image_filename.name}")

        # Extract tables as screenshots using pdfplumber
        tables = plumber_page.find_tables()

        for table_index, table in enumerate(tables):
            # Get table bounding box
            bbox = table.bbox  # (x0, top, x1, bottom)

            # Crop the page region containing the table
            # pdfplumber bbox is (x0, top, x1, bottom)
            # We need to use pdfplumber's crop method
            table_crop = plumber_page.crop(bbox)

            # Convert to PIL Image
            table_image = table_crop.to_image(resolution=300)  # High resolution
            pil_table_image = table_image.original

            # Check if solid color (with edge detection enabled)
            is_solid, reason = is_solid_color(pil_table_image, variance_threshold,
                                             use_edge_detection=True)

            if is_solid:
                filtered_tables.append({
                    'page': page_num + 1,
                    'table_index': table_index,
                    'reason': reason
                })
                continue

            # Save valid table screenshot
            table_count += 1
            table_filename = images_path / f"table_{table_count}.png"
            pil_table_image.save(table_filename, 'PNG')
            print(f"  ✅ Saved table: {table_filename.name}")

    # Close PDFs
    pdf_doc.close()
    pdf_plumber.close()

    return {
        'figures_extracted': figure_count,
        'tables_extracted': table_count,
        'filtered_images': filtered_images,
        'filtered_tables': filtered_tables
    }


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python extract_pdf_images.py <pdf_path> [images_dir]")
        sys.exit(1)

    pdf_path = sys.argv[1]

    # Default images directory
    if len(sys.argv) >= 3:
        images_dir = sys.argv[2]
    else:
        images_dir = "images"

    print(f"Extracting from: {pdf_path}")
    print(f"Output directory: {images_dir}")
    print("Skipping page 1...\n")

    result = extract_images_and_tables(pdf_path, images_dir)

    print(f"\n✅ Extraction complete:")
    print(f"   - Figures saved: {result['figures_extracted']}")
    print(f"   - Tables saved: {result['tables_extracted']}")
    print(f"   - Images filtered: {len(result['filtered_images'])}")
    print(f"   - Tables filtered: {len(result['filtered_tables'])}")

    if result['filtered_images']:
        print("\nFiltered images:")
        for img in result['filtered_images']:
            print(f"  • Page {img['page']}, image {img['image_index']}: {img['reason']}")

    if result['filtered_tables']:
        print("\nFiltered tables:")
        for tbl in result['filtered_tables']:
            print(f"  • Page {tbl['page']}, table {tbl['table_index']}: {tbl['reason']}")


if __name__ == "__main__":
    main()
