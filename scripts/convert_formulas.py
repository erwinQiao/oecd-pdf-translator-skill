#!/usr/bin/env python3
"""
Formula Detection and Conversion to LaTeX for OECD PDFs

Identifies mathematical formulas in text and converts them to LaTeX format
for use in QMD documents with $ (inline) or $$ (block) delimiters.
"""

import re


class FormulaConverter:
    """Convert text-based formulas to LaTeX format."""

    def __init__(self):
        """Initialize the formula converter with common patterns."""
        pass

    def convert_inline_formulas(self, text: str) -> str:
        """
        Convert inline formulas in text.

        Args:
            text: Input text containing formulas

        Returns:
            Text with formulas converted to LaTeX
        """
        result = text

        # IC50 notation - most common in OECD docs
        result = re.sub(r'\bIC\s*[-_]?\s*50\b', r'IC$_{50}$', result, flags=re.IGNORECASE)
        result = re.sub(r'\bIC\s*\(\s*50\s*\)', r'IC$_{50}$', result, flags=re.IGNORECASE)

        # Chemical formulas
        result = re.sub(r'\bCO2\b', r'CO$_2$', result)
        result = re.sub(r'\bH2O\b', r'H$_2$O', result)
        result = re.sub(r'\bO2\b', r'O$_2$', result)

        # PIF and MPE notation
        result = re.sub(r'\bPIF\b', r'PIF', result)
        result = re.sub(r'\bMPE\b', r'MPE', result)

        # UV notation
        result = re.sub(r'\bUVA\b', r'UVA', result)
        result = re.sub(r'\bUVB\b', r'UVB', result)
        result = re.sub(r'\bUVC\b', r'UVC', result)

        # Concentration units
        result = re.sub(r'(\d+)\s*µg/mL', r'\1~µg/mL', result)
        result = re.sub(r'(\d+)\s*mM\b', r'\1~mM', result)
        result = re.sub(r'(\d+)\s*µM\b', r'\1~µM', result)

        # Temperature
        result = re.sub(r'(\d+)\s*°\s*C\b', r'\1~°C', result)
        result = re.sub(r'37\s*0\s*C', r'37°C', result)

        # Dose notation
        result = re.sub(r'(\d+)\s*J/cm2\b', r'\1~J/cm$^2$', result)
        result = re.sub(r'(\d+)\s*mW/cm2\b', r'\1~mW/cm$^2$', result)

        # Time notation
        result = re.sub(r'(\d+)\s*h\b', r'\1~h', result)
        result = re.sub(r'(\d+)\s*min\b', r'\1~min', result)

        # Wavelengths
        result = re.sub(r'(\d+)\s*nm\b', r'\1~nm', result)

        # Ratios with colon
        result = re.sub(r'(\d+)\s*:\s*(\d+)', r'\1:\2', result)

        # Percentages
        result = re.sub(r'(\d+)\s*%', r'\1\\%', result)

        # Superscript notation like 2+
        result = re.sub(r'(\d+)\s*\+\s*', r'\1$^+$', result)

        # Subscripts in chemical notation
        result = re.sub(r'([A-Z][a-z]?)\s*_\s*(\d+)', r'\1$_{\2}$', result)

        return result


def main():
    """Main entry point for standalone usage."""
    import sys

    print("OECD Formula Converter")
    print("====================")
    print()
    print("Common conversions:")
    converter = FormulaConverter()

    examples = [
        "IC50",
        "The IC50 value was calculated",
        "CO2 and H2O",
        "5 J/cm2",
        "1.7 mW/cm2",
        "37°C",
        "UVA and UVB",
        "50 µg/mL",
    ]

    for example in examples:
        converted = converter.convert_inline_formulas(example)
        print(f"  {example:30s} → {converted}")
    print()
    print("Formula converter is integrated into md_to_qmd.py")


if __name__ == "__main__":
    main()
