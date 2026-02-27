# OECD PDF Translator Skill

> 自动将 OECD 测试指南 PDF 转换为专业的双语文档（英文+中文），支持模板定制和术语准确翻译。

## 简介

**OECD PDF Translator** 是一个用于处理 OECD 第 4 部分（动物替代实验）测试指南 PDF 的自动化工具。它能够提取 PDF 中的文本和图表，自动检测表格，应用准确的毒理学术语，并生成清晰的可发布文档。

### 主要特点

- **智能表格检测**：自动检测表格并保存为截图
- **图像过滤**：自动移除纯黑/纯白图像
- **术语准确翻译**：使用全面的毒理学词汇表
- **公式自动转换**：将数学公式转换为 LaTeX 格式（`$` 内联，`$$` 块级）
- **清晰输出**：仅生成 `images/` 文件夹和两个 QMD 文件
- **多种翻译 API**：支持 Claude、Anthropic、OpenAI、DeepSeek、千问等
- **模板定制**：支持自定义 QMD 模板，灵活控制输出格式

## 安装

### Claude Code Skills 目录位置

[Claude Code安装](https://www.beautyhubcode.com/docs/CodeandData/AI/claudecodeinstall.html)可以参考该方法进行国产大模型的替换

Claude Code 的 skills 目录位置：
- **Linux/macOS**: `~/.config/claude-code/skills/`
- **Windows**: `%APPDATA%\claude-code\skills\`

**检查当前 skills 目录：**
```bash
# Linux/macOS
ls ~/.config/claude-code/skills/

# 或者查看配置
cat ~/.config/claude-code/config.json
```

### 安装步骤

**方法 1：复制 skill 目录**
```bash
# 1. 复制整个 skill 目录到 Claude Code skills 目录
cp -r oecd-pdf-translator-skill ~/.config/claude-code/skills/

# 2. 验证安装
ls ~/.config/claude-code/skills/oecd-pdf-translator-skill/
# 应该看到：SKILL.md, README.md, scripts/, references/, assets/

# 3. 重启 Claude Code 或重新加载 skills
```

**验证安装成功：**
在 Claude Code 中输入：

```
我有哪些可用的 skills？
```
应该能看到 `oecd-pdf-translator` 在列表中。

## 在 Claude Code 中使用

### 基本用法

安装完成后，您可以直接在 Claude Code 对话中调用这个 skill：

**示例 1：处理 PDF 文件**
```
请使用 oecd-pdf-translator 处理这个 PDF：9789264071162-en.pdf
```

**示例 2：转换为双语文档**
```
帮我把 OECD_432.pdf 转换为英汉双语 QMD 文档
```

**示例 3：使用默认设置**
```
用 oecd-pdf-translator skill 处理当前的 PDF 文件
```

### 指定参数

您可以在对话中指定输出参数：

```
请处理 OECD_432.pdf，输出到 ./output 目录，
标题设置为 "In Vitro 3T3 NRU Phototoxicity Test"，
文档编号是 432
```

**使用自定义模板：**
```
请使用 my_template.qmd 模板处理这个 PDF，
发布日期是 "18 June 2019"
```

### 单独执行步骤

如果需要更精细的控制，可以单独执行各个步骤：

**仅提取文本：**
```
请从这个 PDF 中提取文本内容，检测表格
```

**仅提取图像和表格：**
```
请从 PDF 中提取图像和表格截图
```

**仅翻译 QMD 文件：**
```
请将这个英文 QMD 文件翻译成中文，使用准确的毒理学术语
```

**仅转换为 QMD 格式：**
```
请将这个 markdown 文件转换为 QMD 格式，
添加公式转换和标题分析
```

### 完整工作流示例

**示例对话：**

```
用户：我有一个 OECD 测试指南 PDF 文件 "TG432.pdf"，想转换为双语文档

Claude：我可以使用 oecd-pdf-translator skill 来处理这个文件。这个 skill 会：
1. 提取文本和检测表格
2. 提取图像和表格截图
3. 转换为 QMD 格式（英文）
4. 翻译为中文（使用毒理学术语表）

是否开始处理？
```

**使用命令行脚本：**

如果您更喜欢直接使用 Python 脚本（不通过 skill）：

```bash
# 使用默认设置处理 PDF
python scripts/process_oecd_pdf.py 9789264071162-en.pdf

# 自定义设置
python scripts/process_oecd_pdf.py input.pdf ./output "Test Title" "432"

# 使用自定义模板和发布日期
python scripts/process_oecd_pdf.py \
    input.pdf \
    output \
    "Title" \
    "432" \
    custom_template.qmd \
    "18 June 2019"
```

### Claude Code vs 命令行

| 方式 | 优点 | 适用场景 |
|------|------|----------|
| **Claude Code** | 自然语言交互，自动参数解析，智能错误处理 | 快速处理、不确定参数时 |
| **命令行** | 完全控制、可脚本化、批量处理 | 批量处理、自动化流程 |

## 模板定制

### 默认模板

默认模板位于 `assets/template.qmd`：

```yaml
---
title: "OECD测试指南第{{DOC_NUMBER}}号：{{TITLE}}"
subtitle: "{{TITLE}}"
author: "OECD (经济合作与发展组织)"
date: "{{DATE}}"
description: "OECD化学品测试指南 - {{TITLE}}"
keywords: [OECD, 测试指南, 毒理学, 体外测试]
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

### 模板变量

| 变量 | 说明 | 示例 |
|------|------|------|
| `{{DOC_NUMBER}}` | OECD 指南编号 | `432` |
| `{{TITLE}}` | 文档标题 | `In Vitro 3T3 NRU Phototoxicity Test` |
| `{{DATE}}` | 当前日期 | `2026-02-10` |
| `{{PUBLICATION_DATE}}` | 原始发布日期 | `18 June 2019` |
| `{{CONTENT}}` | 主文档内容 | (提取的文本) |
| `{{REFERENCES}}` | 参考文献部分 | (文献列表) |

### 创建自定义模板

1. **复制默认模板：**
   ```bash
   cp assets/template.qmd my_template.qmd
   ```

2. **编辑模板：**
   ```yaml
   ---
   title: "{{TITLE}} - My Custom Format"
   format:
     html:
       theme: cosmo
       code-fold: true
   ---
   ```

## 注意事项

### API 使用和 Token 消耗

**重要提示：**
- 翻译功能使用 LLM API，会消耗较多 Tokens
- 对于大型 OECD 文档（通常 50-100 页），完整翻译成本较高
- **建议先测试小段内容**，评估 Token 消耗和翻译质量
- Token 消耗取决于：
  - 文档长度
  - 翻译 API 选择（Claude vs OpenAI vs DeepSeek 等）
  - 术语复杂度

### 替代翻译方案

如果不想使用 API 翻译，可以采用以下方法：

**方案 1：Google 翻译**
```bash
# 1. 生成英文 QMD（不翻译）
python scripts/process_oecd_pdf.py input.pdf output "Title" "432"

# 2. 打开 output/input_英文.qmd，复制到 Google 翻译

# 3. 保存翻译结果为 input_中文.qmd
```

**方案 2：DeepL**
- DeepL 提供更高质量的科学文献翻译
- 支持批量文档翻译
- 可以保留 Markdown 格式

## 输出结果

处理完成后，您将得到：

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

**输出保证：** 不会保留中间的 `.py` 或 `.md` 文件。


完整词汇表请参见 `references/toxicology-glossary.md`

## 项目结构

```
oecd-pdf-translator-skill/
├── SKILL.md              # Claude Code skill 定义
├── README.md             # 本文档
├── scripts/              # 可执行 Python 脚本
│   ├── extract_pdf_text.py      # 文本提取和表格检测
│   ├── extract_pdf_images.py    # 图像和表格截图提取
│   ├── convert_formulas.py      # 公式检测和 LaTeX 转换
│   ├── md_to_qmd.py             # Markdown 转 QMD
│   ├── translate_qmd.py         # 翻译和术语表应用
│   └── process_oecd_pdf.py      # 主流程脚本
├── references/           # 参考文档
│   ├── toxicology-glossary.md   # 英汉术语词汇表
│   └── qmd-formatting.md        # QMD 格式指南
└── assets/               # 模板和配置
    └── template.qmd              # 默认 QMD 模板
```

## 最佳实践

1. **先测试示例 PDF** - 批量处理前验证输出质量
2. **检查术语准确性** - 对照词汇表检查翻译术语
3. **验证表格提取** - 确保表格正确裁剪且可读
4. **验证 QMD 渲染** - 在 Quarto 中测试 HTML/PDF 输出
5. **保持词汇表更新** - 遇到新术语时添加到词汇表

## 限制

- **复杂表格**：多页或合并单元格的表格可能无法完美提取
- **扫描 PDF**：文本提取需要可选择文本（非图像）
- **特殊字符**：某些 Unicode 字符可能需要人工审核
- **格式保留**：复杂布局可能无法完美转移到 QMD
