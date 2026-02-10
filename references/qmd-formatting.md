# QMD Formatting Guide for OECD Test Guidelines

This reference guide documents the standard QMD structure for OECD test guideline documents based on existing examples.

## Frontmatter Template

Every QMD file should begin with YAML frontmatter:

```yaml
---
title: "OECD测试指南第XXX号：[English Title]"
subtitle: "[English Title]"
author: "OECD (经济合作与发展组织)"
date: "YYYY-MM-DD"
description: "OECD化学品测试指南 - [Brief Description]"
keywords: [OECD, 测试指南, 毒理学, 体外测试, 具体关键词]
lang: zh-CN
format:
  html:
    toc: true
    number-sections: true
    theme: flatly
  pdf:
    toc: true
    number-sections: true
  docx:
    toc: true
    number-sections: true
---
```

### Frontmatter Fields

- **title**: Chinese title with document number
- **subtitle**: Original English title
- **author**: Always "OECD (经济合作与发展组织)"
- **date**: Current date in ISO format
- **description**: Brief description of the guideline
- **keywords**: Relevant keywords for indexing
- **lang**: Set to "zh-CN" for Chinese content
- **format**: Output format options (HTML, PDF, DOCX)

## Document Structure

### 1. Document Information Table

After frontmatter, include a summary table:

```markdown
# 文档信息

| 属性 | 内容 |
|------|------|
| **指南编号** | 第XXX号 |
| **发布日期** | DD MMMM YYYY |
| **文档类型** | OECD测试指南 |
| **主题** | [Test Name] |
| **总页数** | NN |
| **章节** | 第4节 - 健康效应 |
```

### 2. Main Content Sections

```markdown
# 原文内容

## 第 1 页

[Page 1 content]

---

## 第 2 页

[Page 2 content]

---

[Continue for all pages]
```

## Heading Hierarchy

### Level 1 (#) - Main Sections
Use for major document divisions:
- 文档信息
- 原文内容
- 参考文献
- 附录

### Level 2 (##) - Page Divisions
Use for page markers:
```markdown
## 第 1 页
## 第 2 页
```

### Level 3 (###) - Content Headings
Use for section headings within content:
```markdown
### Introduction
### Principle Of The Test Method
### Description Of The Test Method
```

### Level 4 (####) - Subsections
Use for subtopics:
```markdown
#### Preparations
#### Cells
#### Media and culture conditions
```

## Figure Referencing

### Standard Format
```markdown
![Figure description](images/figure_X.png){#fig-X}
```

### With Caption
```markdown
![Figure X. Description](images/figure_X.png){#fig-X}

Figure X: Detailed description of the figure content.
```

### Example
```markdown
![Figure 1. Spectral power distribution](images/figure_1.png){#fig-1}

Figure 1: Spectral power distribution of a filtered solar simulator.
```

## Table Referencing

Tables are stored as images in the `images/` folder:

```markdown
![表格 1](images/table_1.png){#tbl-1}

Table 1: Proficiency chemicals
```

## Text Formatting

### Emphasis
- **Bold**: `**text**` or `__text__`
- *Italic*: `*text*` or `_text_`
- ***Bold italic***: `***text***`

### Code/Inline
- `Inline code`: `` `code` ``
- Code block:
  ````markdown
  ```python
  code here
  ```
  ````

### Lists
Bullet lists:
```markdown
- Item 1
- Item 2
  - Nested item
  - Another nested item
- Item 3
```

Numbered lists:
```markdown
1. First item
2. Second item
3. Third item
```

## Citation Formatting

### In-text Citations
```markdown
According to Spielmann et al. (1998), the test method...

The in vitro 3T3 NRU phototoxicity test (8)(9)(10)(11) was shown to be predictive...
```

### Reference List
```markdown
### Literature

(1) Author A. (Year). Title. Journal, Volume(Issue): pages.

(2) Author B., Author C. (Year). Title. In: Book Title. Publisher: Location.
```

### Examples
```markdown
(1) Spielmann, H., Lovell, W.W., Hölzle, E., Johnson, B.E., Maurer, T.,
Miranda, M.A., Pape, W.J.W., Sapora, O., and Sladowski, D. (1994).
In vitro phototoxicity testing: The report and recommendations of
ECVAM Workshop 2. ATLA, 22, 314-348.

(2) OECD (2018). Guidance Document on Good In Vitro Methods Practices
(GIVIMP). OECD Series on Testing and Assessment No. 286.
```

## Special Elements

### Callout Boxes
```markdown
::: {.box-summary}
## Important Note

This is an important note or warning.
:::
```

### Horizontal Rules
```markdown
---
```

### Line Breaks
```markdown
End of line.
 Two spaces creates line break.

New paragraph (blank line).
```

## Mathematical Notation

### Inline Math
```markdown
The concentration is calculated as $C = V / N$.
```

### Display Math
```markdown
$$
IC_{50} = \frac{[Irr]^{-}}{[Irr]^{+}}
$$
```

## Units and Measurements

### Formatting
- Leave space between number and unit: `5 J/cm²` not `5J/cm²`
- Use superscript for exponents: `cm²`, `m³`
- Use Greek letters: `µg/mL`, `°C`

### Common Units in OECD Guidelines
- Concentration: `µg/mL`, `mg/L`, `mM`, `ppm`
- Temperature: `°C`
- Time: `sec`, `min`, `h`
- Light dose: `J/cm²`, `mW/cm²`
- Wavelength: `nm`

## Section Numbering

When `number-sections: true` is set in frontmatter, sections are automatically numbered.

To manually number:
```markdown
### 1. Introduction
### 2. Principle Of The Test Method
#### 2.1 Preparations
#### 2.2 Test Conditions
### 3. Results
```

## Character Encoding

- Always use UTF-8 encoding
- Support Chinese characters (Simplified)
- Support special scientific symbols: µ, °, ±, ², ³, etc.

## Best Practices

1. **Consistency**: Use consistent formatting throughout
2. **Clarity**: Keep headings descriptive and concise
3. **Accessibility**: Add alt text and descriptions for figures
4. **Validation**: Test rendering in HTML, PDF, and DOCX formats
5. **Version Control**: Track changes in git with clear commit messages

## Example Complete Document Structure

```markdown
---
title: "OECD测试指南第432号：In Vitro 3T3 NRU Phototoxicity Test"
subtitle: "In Vitro 3T3 NRU Phototoxicity Test"
author: "OECD (经济合作与发展组织)"
date: "2026-02-09"
description: "OECD化学品测试指南 - 体外3T3 NRU光毒性测试"
keywords: [光毒性, 体外测试, 3T3细胞, NRU, OECD]
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
| **指南编号** | 第432号 |
| **发布日期** | 18 June 2019 |
| **文档类型** | OECD测试指南 |
| **主题** | 体外3T3 NRU光毒性测试 |

---

# 原文内容

## 第 1 页

[Content page 1]

---

## 第 2 页

### Introduction

Phototoxicity is defined as a toxic response...

![Figure 1](images/figure_1.png){#fig-1}

### Initial Consideration

Many types of chemicals...

---

[Continue for all pages]

### Literature

(1) Author A. (Year). Title. Journal...

---

## Annex A. Definitions

[Annex content]
```

## Output Formats

### HTML
- Supports interactive navigation
- Best for online viewing
- Include table of contents

### PDF
- Best for printing
- Professional layout
- Include page numbers

### DOCX
- For Microsoft Word users
- Editable format
- Include tracking changes if needed

## Troubleshooting

### Images Not Displaying
- Check image paths are relative: `images/figure_1.png`
- Ensure images folder exists in output directory
- Verify image files are not corrupted

### Table of Contents Not Generated
- Ensure `toc: true` in frontmatter
- Use proper heading levels (#, ##, ###)
- Check heading hierarchy is logical

### Chinese Characters Display Issues
- Confirm UTF-8 encoding
- Check font supports Chinese characters
- Verify `lang: zh-CN` in frontmatter

### Math Notation Not Rendering
- Use proper LaTeX syntax: `$...$` for inline, `$$...$$` for display
- Check math delimiters are balanced
- Ensure output format supports MathJax/KaTeX
