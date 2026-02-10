---
name: oecd-pdf-translator
description: Convert OECD Section 4 animal alternative experiment PDFs to bilingual QMD documents with accurate toxicology terminology. Use for extracting text and images from OECD test guideline PDFs, converting PDF content to structured QMD format, translating OECD guidelines to Chinese with scientific terminology accuracy, and processing OECD TG 432 phototoxicity test documents. Automatically handles table detection, image filtering, and cleanup.
---

# OECD PDF to Chinese QMD Translator

## Overview

This skill automates the conversion of OECD Section 4 test guideline PDFs into professional bilingual (English-Chinese) QMD documents. It extracts text and images while detecting tables, applies accurate toxicology terminology, and produces clean publication-ready output.

### When to Use This Skill

Use this skill when you need to:
- Convert OECD test guideline PDFs to QMD format
- Translate scientific documents with accurate toxicology terminology
- Process OECD TG 432 (phototoxicity test) or similar guidelines
- Extract figures and tables from OECD documents
- Create bilingual versions of OECD guidelines

### Key Features

- **Smart Table Detection**: Automatically detects tables and saves them as screenshots
- **Image Filtering**: Removes solid black/white images
- **Accurate Terminology**: Uses comprehensive glossary for toxicology, experimental, and computational terms
- **Formula Conversion**: Automatically converts mathematical formulas to LaTeX format with `$` (inline) and `$$` (block) delimiters
- **Clean Output**: Only produces `images/` folder and two QMD files
- **Multiple Translation APIs**: Supports Claude, Anthropic, OpenAI, DeepSeek, Qwen, and more

## Workflow

### Quick Start

```bash
# Process a PDF with default settings
python scripts/process_oecd_pdf.py 9789264071162-en.pdf

# With custom settings
python scripts/process_oecd_pdf.py input.pdf ./output "Test Title" "432"
```

### Step-by-Step Process

#### 1. Text Extraction

Extracts text from PDF page by page while detecting tables:
```bash
python scripts/extract_pdf_text.py input.pdf output.md
```

**What it does:**
- Uses `pdfplumber` for text extraction
- Detects tables using `find_tables()`
- Inserts `[TABLE: table_X]` placeholders
- Preserves paragraph structure
- Handles multi-column layouts

**Output:** Markdown file with text and table placeholders

#### 2. Image and Table Extraction

Extracts images and table screenshots:
```bash
python scripts/extract_pdf_images.py input.pdf images/
```

**What it does:**
- Skips page 1 entirely
- Extracts images from pages 2+
- Filters solid black/white images using:
  - Variance threshold (< 1.0)
  - Color range check (black < 15, white > 240)
- Crops tables as high-resolution screenshots
- Saves as `figure_X.png` and `table_X.png`

**Output:** `images/` folder with extracted figures and tables

#### 3. Markdown to QMD Conversion

Converts markdown to structured QMD:
```bash
python scripts/md_to_qmd.py input.md output.qmd "Title" "432"
```

**What it does:**
- Creates proper QMD frontmatter
- Replaces `[TABLE: table_X]` with image references
- **Converts formulas to LaTeX format:**
  - Inline formulas use `$...$` delimiters (e.g., `$IC_{50}$`)
  - Block formulas use `$$...$$` delimiters (e.g., `$$\text{PIF} = \frac{IC_{50}(-\text{Irr})}{IC_{50}(+\text{Irr})}$$`)
  - Automatically detects and converts:
    - Chemical formulas (CO₂, H₂O)
    - Mathematical notation (IC₅₀, PIF, MPE)
    - Units (µg/mL, J/cm², mW/cm²)
    - Concentrations and ratios
    - Temperature and time notation
- Analyzes and fixes headings using:
  - Context analysis (surrounding content)
  - Format analysis (ALL CAPS, short phrases)
  - Content analysis (length, punctuation)
- Converts proper headings to `#`, `##`, `###` format
- Adds figure references

**Output:** English QMD file with proper structure and LaTeX formulas

#### 4. Translation to Chinese

Translates English QMD to Chinese:
```bash
python scripts/translate_qmd.py input_english.qmd output_chinese.qmd claude
```

**What it does:**
- Applies comprehensive terminology glossary
- Preserves all formatting and metadata
- Handles reference citations correctly
- Maintains table image references
- Supports multiple translation APIs (Claude, Anthropic, OpenAI, etc.)

**Output:** Chinese QMD file with accurate scientific terminology

#### 5. Cleanup

Removes intermediate files:
- Deletes temporary `.md` files
- Keeps only final `images/` folder and QMD files

## Resources

### scripts/

Executable Python scripts for each processing step:

- **`extract_pdf_text.py`** - Text extraction with table detection
- **`extract_pdf_images.py`** - Image and table screenshot extraction with filtering
- **`convert_formulas.py`** - Formula detection and LaTeX conversion (integrated into md_to_qmd.py)
- **`md_to_qmd.py`** - Markdown to QMD conversion with heading analysis and formula conversion
- **`translate_qmd.py`** - Translation with terminology glossary and multiple API support
- **`process_oecd_pdf.py`** - Main orchestration script (runs all steps)

### references/

Documentation and reference materials:

- **`toxicology-glossary.md`** - Comprehensive English-Chinese terminology glossary with equal priority for:
  - Toxicology terms (phototoxicity, cytotoxicity, IC50, PIF, MPE)
  - Experimental terms (in vitro, in vivo, assay, monolayer, passage number)
  - Computational/statistical terms (concentration-response, regression, bootstrap)
  - General OECD terms, units, and abbreviations

- **`qmd-formatting.md`** - QMD formatting guide covering:
  - Frontmatter templates
  - Heading hierarchy
  - Figure and table referencing
  - Citation formatting
  - Special elements and best practices

**Usage:** Read these files when you need to verify terminology accuracy or formatting standards.

### assets/

This skill does not include assets. All output is generated dynamically from input PDFs.

## Terminology Translation

The skill uses a comprehensive glossary with equal priority for all domains:

### Toxicology Examples
- phototoxicity → 光毒性
- cytotoxicity → 细胞毒性
- IC50 → IC50（半抑制浓度）
- PIF → PIF（光刺激因子）
- Neutral Red Uptake → 中性红摄取

### Experimental Examples
- in vitro → 体外
- in vivo → 体内
- assay → 测定
- monolayer → 单层
- passage number → 传代数

### Computational Examples
- concentration-response curve → 浓度-反应曲线
- non-linear regression → 非线性回归
- bootstrap → 自助法
- standard deviation → 标准差

See `references/toxicology-glossary.md` for complete glossary.

## Translation API Support

The skill supports multiple translation services (in priority order):

1. **Claude (Default)** - Uses current Claude model with terminology glossary
2. **Anthropic API** - Claude API for external requests
3. **OpenAI API** - GPT-4/GPT-3.5
4. **DeepSeek API** - DeepSeek models
5. **阿里云千问 (Qwen)** - Alibaba Qwen API
6. **智谱AI (ChatGLM)** - Zhipu AI API
7. **Kimi/Moonshot** - Moonshot API
8. **Local Models** - Local open-source models (Llama, Qwen, etc.)

Specify method when running translation:
```bash
python scripts/translate_qmd.py input.qmd output.qmd <method>
```

## Output Structure

After processing, you get:

```
output/
├── images/
│   ├── figure_1.png
│   ├── figure_2.png
│   ├── table_1.png
│   └── table_2.png
├── input_英文.qmd
└── input_中文.qmd
```

**Clean output guarantee:** No intermediate `.py` or `.md` files remain.

## Example Usage

### Basic Usage

```bash
# Process OECD TG 432 PDF
python scripts/process_oecd_pdf.py 9789264071162-en.pdf

# Output:
# - images/ folder with figures and tables
# - 9789264071162-en_英文.qmd
# - 9789264071162-en_中文.qmd
```

### Advanced Usage

```bash
# Specify output directory and metadata
python scripts/process_oecd_pdf.py \
    OECD_432.pdf \
    ./output \
    "In Vitro 3T3 NRU Phototoxicity Test" \
    "432"
```

### Individual Steps

```bash
# Step 1: Extract text
python scripts/extract_pdf_text.py input.pdf extracted.md

# Step 2: Extract images and tables
python scripts/extract_pdf_images.py input.pdf images/

# Step 3: Convert to QMD
python scripts/md_to_qmd.py extracted.md english.qmd "Title" "432"

# Step 4: Translate
python scripts/translate_qmd.py english.qmd chinese.qmd claude
```

## Troubleshooting

### Images Not Extracted
- Check if PDF has images after page 1
- Verify images aren't solid black/white (filtered automatically)
- Review console output for filtered image reasons

### Tables Not Detected
- Ensure tables have clear structure in PDF
- Check if pdfplumber can detect table boundaries
- Manual cropping may be needed for complex tables

### Translation Terminology Issues
- Review `references/toxicology-glossary.md`
- Add missing terms to glossary in `scripts/translate_qmd.py`
- Check if translation API preserves formatting

### Heading Errors
- Review heading detection rules in `scripts/md_to_qmd.py`
- Manually edit QMD file if needed
- Report false positives for improvement

## Dependencies

**Required Python packages:**
- `pdfplumber` - PDF text and table detection
- `PyMuPDF` (fitz) - PDF image extraction
- `Pillow` - Image processing
- `numpy` - Image variance calculation
- `PyYAML` - QMD frontmatter handling

**Optional translation API clients:**
- `anthropic` - Anthropic API
- `openai` - OpenAI API
- `deepseek` - DeepSeek API
- `dashscope` - 阿里云千问 API
- `zhipuai` - 智谱AI API
- `moonshot` - Kimi/Moonshot API

Install dependencies:
```bash
pip install pdfplumber PyMuPDF Pillow numpy PyYAML
pip install anthropic openai  # Optional, for API fallbacks
```

## Best Practices

1. **Always test with sample PDF first** - Verify output quality before batch processing
2. **Check terminology accuracy** - Review translated terms against glossary
3. **Verify table extraction** - Ensure tables are properly cropped and readable
4. **Validate QMD rendering** - Test HTML/PDF output in Quarto
5. **Keep glossary updated** - Add new terms as you encounter them

## Limitations

- **Complex tables**: Multi-page or merged cell tables may not extract perfectly
- **Scanned PDFs**: Text extraction requires selectable text (not images)
- **Special characters**: Some Unicode characters may need manual review
- **Format preservation**: Complex layouts may not transfer perfectly to QMD

## Future Enhancements

Potential improvements:
- Support for Annex documents
- Batch processing of multiple PDFs
- Interactive table editing
- Custom terminology per document type
- Integration with reference databases

## Formula Conversion

The skill automatically converts mathematical and chemical formulas to LaTeX format for proper rendering in QMD documents.

### Automatic Conversions

**Inline Formulas** (using `$...$`):
- `IC50` → `$IC_{50}$`
- `CO2` → `$CO_{2}$`
- `5 J/cm2` → `5~$\text{J/cm}^2$`
- `1.7 mW/cm2` → `1.7~$\text{mW/cm}^2$`
- `µg/mL` → `$\mu\text{g/mL}$`
- `°C` → `$°C$`

**Block Formulas** (using `$$...$$`):
- PIF calculation: `$$\text{PIF} = \frac{IC_{50}(-\text{Irr})}{IC_{50}(+\text{Irr})}$$`
- Time calculation: `$$t (\text{min}) = \frac{\text{irradiation dose (J/cm}^2) \times 1000}{\text{irradiance (mW/cm}^2) \times 60}$$`
- MPE formula: `$$\text{MPE} = \frac{\sum_{i=1}^{n} w_i \times PE_{c_i}}{\sum_{i=1}^{n} w_i}$$`

### Supported Formula Types

1. **Chemical formulas**: CO₂, H₂O, O₂
2. **Mathematical notation**: IC₅₀, PIF, MPE, subscripts, superscripts
3. **Units**: µg/mL, J/cm², mW/cm², mM, °C, nm
4. **Concentrations and ratios**: Dilution factors, percentages
5. **Time and temperature notation**: h, min, sec, °C
6. **Wavelengths**: nm, UVA, UVB

### Manual Formula Entry

If you need to add formulas manually, use:
- **Inline**: `$formula$` - e.g., `The $IC_{50}$ value was...`
- **Block**: `$$formula$$` - e.g., `$$PIF = \frac{IC_{50}(-Irr)}{IC_{50}(+Irr)}$$`

### Formula Examples in Context

```markdown
The concentration reducing cell viability to 50% ($IC_{50}$) was calculated.
A dose of 5~$\text{J/cm}^2$ was determined to be non-cytotoxic.
$$\text{PIF} = \frac{IC_{50}(-\text{Irr})}{IC_{50}(+\text{Irr})}$$
```

This renders properly in Quarto/PDF output with formatted mathematical notation.
