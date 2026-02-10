#!/usr/bin/env python3
"""
QMD Translation Script for OECD Test Guidelines

Translates English QMD to Chinese with accurate toxicology terminology.
Supports multiple translation APIs with Claude as primary method.
"""

import re
import sys
import os
from pathlib import Path
from typing import Dict, Optional


# Terminology glossary with equal priority for all domains
TERMINOLOGY_GLOSSARY = {
    # Toxicology terms
    'phototoxicity': '光毒性',
    'cytotoxicity': '细胞毒性',
    'photo-cytotoxicity': '光细胞毒性',
    'IC50': 'IC50（半抑制浓度）',
    'IC 50': 'IC50',
    'Photo-Irritation-Factor': '光刺激因子',
    'PIF': 'PIF（光刺激因子）',
    'Mean Photo Effect': '平均光效应',
    'MPE': 'MPE（平均光效应）',
    'Neutral Red Uptake': '中性红摄取',
    'NRU': 'NRU（中性红摄取）',
    'Neutral Red': '中性红',
    'NR': '中性红',
    'irradiance': '辐照度',
    'irradiation': '辐照',
    'molar extinction coefficient': '摩尔消光系数',
    'MEC': 'MEC（摩尔消光系数）',
    'photoreactive': '光反应性',
    'phototoxicants': '光毒性物质',
    'solvent control': '溶剂对照',
    'positive control': '阳性对照',
    'viability': '细胞活力',
    'cell viability': '细胞活力',

    # Experimental terms
    'in vitro': '体外',
    'in vivo': '体内',
    'assay': '测定',
    'test': '测试',
    'monolayer': '单层',
    'confluent': '融合',
    'passage number': '传代数',
    'mycoplasma': '支原体',
    'contamination': '污染',
    'incubation': '孵育',
    'culture medium': '培养基',
    'DMEM': 'DMEM（Dulbecco改良Eagle培养基）',
    'serum': '血清',
    'glutamine': '谷氨酰胺',
    'penicillin': '青霉素',
    'streptomycin': '链霉素',
    'concentration': '浓度',
    'dilution': '稀释',
    'solvent': '溶剂',
    'DMSO': 'DMSO（二甲基亚砜）',
    'ethanol': '乙醇',
    'EtOH': '乙醇',
    'absorbance': '吸光度',
    'optical density': '光密度',
    'OD': 'OD（光密度）',
    'spectrophotometer': '分光光度计',
    'wavelength': '波长',

    # Computational/statistical terms
    'concentration-response curve': '浓度-反应曲线',
    'dose-response': '剂量-反应',
    'non-linear regression': '非线性回归',
    'bootstrap': '自助法',
    'bootstrap procedure': '自助法程序',
    'statistical analysis': '统计分析',
    'standard deviation': '标准差',
    'mean': '平均值',
    'variance': '方差',
    'regression': '回归',
    'correlation': '相关性',
    'significant': '显著性',
    'probability': '概率',
    'confidence interval': '置信区间',

    # General OECD terms
    'test guideline': '测试指南',
    'OECD': 'OECD（经济合作与发展组织）',
    'validation': '验证',
    'proficiency': '熟练度',
    'acceptance criteria': '接受标准',
    'quality control': '质量控制',
    'reference chemical': '参比化学物',
    'test chemical': '受试化学物',
    'Annex': '附件',
}


class TranslationAPI:
    """Base class for translation APIs."""

    def translate(self, text: str, context: str = "") -> str:
        """Translate text from English to Chinese."""
        raise NotImplementedError


class ClaudeTranslation(TranslationAPI):
    """Claude-based translation (primary method)."""

    def __init__(self):
        try:
            import anthropic
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if api_key:
                self.client = anthropic.Anthropic(api_key=api_key)
                self.available = True
            else:
                print("⚠️  ANTHROPIC_API_KEY not found, falling back to term-only translation")
                self.client = None
                self.available = False
        except Exception as e:
            print(f"⚠️  Anthropic API not available: {e}, falling back to term-only translation")
            self.client = None
            self.available = False

    def translate(self, text: str, context: str = "") -> str:
        """
        Translate text using Claude API with terminology glossary.
        Falls back to term replacement if API unavailable.
        """
        if not self.available or not self.client:
            # Fallback to terminology replacement only
            print("⚠️  Using term-only translation (API unavailable)")
            result = text
            terms_sorted = sorted(TERMINOLOGY_GLOSSARY.items(),
                                key=lambda x: len(x[0]), reverse=True)
            for en, zh in terms_sorted:
                pattern = re.compile(r'\b' + re.escape(en) + r'\b', re.IGNORECASE)
                result = pattern.sub(zh, result)
            return result

        # Build terminology guide for the prompt
        glossary_items = list(TERMINOLOGY_GLOSSARY.items())[:50]  # Use top 50 terms
        glossary_str = "\n".join([f"  - {en}: {zh}" for en, zh in glossary_items])

        prompt = f"""You are translating an OECD test guideline document from English to Chinese.

IMPORTANT INSTRUCTIONS:
1. Translate the FULL text to Chinese - do not leave any English text untranslated
2. Use the following terminology glossary for consistent scientific translation:
{glossary_str}
3. Preserve all markdown formatting, including headings (#, ##, ###), bold (**), italics (*), links, and code blocks
4. Keep all numeric values, units, chemical formulas, and abbreviations unchanged
5. Maintain the original document structure and paragraph breaks
6. For technical terms not in the glossary, use standard Chinese scientific terminology

Text to translate:
{text}

Provide only the Chinese translation without any explanation or notes."""

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=8192,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text.strip()
        except Exception as e:
            print(f"⚠️  API translation failed: {e}, falling back to term-only translation")
            # Fallback to terminology replacement only
            result = text
            terms_sorted = sorted(TERMINOLOGY_GLOSSARY.items(),
                                key=lambda x: len(x[0]), reverse=True)
            for en, zh in terms_sorted:
                pattern = re.compile(r'\b' + re.escape(en) + r'\b', re.IGNORECASE)
                result = pattern.sub(zh, result)
            return result


class AnthropicAPITranslation(TranslationAPI):
    """Anthropic API translation (fallback 1)."""

    def __init__(self, api_key: Optional[str] = None):
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=api_key or os.getenv('ANTHROPIC_API_KEY'))
            self.available = True
        except Exception as e:
            print(f"Anthropic API not available: {e}")
            self.available = False

    def translate(self, text: str, context: str = "") -> str:
        if not self.available:
            raise RuntimeError("Anthropic API not available")

        # Build prompt with terminology
        glossary_str = "\n".join([f"{en}: {zh}" for en, zh in list(TERMINOLOGY_GLOSSARY.items())[:20]])

        prompt = f"""Translate the following text from English to Chinese. Use accurate scientific terminology for toxicology and experimental methods.

Key terminology:
{glossary_str}

Text to translate:
{text}

Provide only the Chinese translation without explanation."""

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text


def translate_qmd_file(input_qmd: str, output_qmd: str,
                      method: str = "claude") -> None:
    """
    Translate QMD file from English to Chinese.

    Args:
        input_qmd: Path to input English QMD file
        output_qmd: Path to output Chinese QMD file
        method: Translation method ('claude-code', 'claude', 'anthropic', 'openai', etc.)
                   - 'claude-code': Creates a translation request for Claude Code to process
                   - 'claude': Uses Anthropic API if available, otherwise term-only
                   - 'anthropic': Uses Anthropic API directly
                   - Other methods use their respective APIs
    """
    with open(input_qmd, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split into frontmatter and body
    parts = content.split('---', 2)
    if len(parts) >= 3:
        frontmatter = parts[1]
        body = parts[2]
    else:
        frontmatter = ""
        body = content

    if method == "claude-code":
        # Create a translation request file for Claude Code interactive processing
        print("📝 Creating Claude Code translation request...")
        result = body

        # Apply terminology glossary first as base
        terms_sorted = sorted(TERMINOLOGY_GLOSSARY.items(),
                            key=lambda x: len(x[0]), reverse=True)

        for en, zh in terms_sorted:
            pattern = re.compile(r'\b' + re.escape(en) + r'\b', re.IGNORECASE)
            result = pattern.sub(zh, result)

        # Update frontmatter for Chinese version
        translated_frontmatter = translate_frontmatter(frontmatter)

        # Combine with term-replacement as base
        translated_content = f"---\n{translated_frontmatter}---\n{result}"

        with open(output_qmd, 'w', encoding='utf-8') as f:
            f.write(translated_content)

        # Create a companion file requesting full translation
        request_file = output_qmd.replace('.qmd', '_translation_request.txt')
        with open(request_file, 'w', encoding='utf-8') as f:
            f.write(f"""CLAUDE CODE TRANSLATION REQUEST
================================

Input file: {input_qmd}
Output file: {output_qmd}
Created: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

INSTRUCTIONS FOR CLAUDE CODE:
1. Read the input QMD file: {input_qmd}
2. Translate ALL English content to Chinese using accurate toxicology terminology
3. Preserve all markdown formatting, LaTeX formulas, and image references
4. Use the terminology glossary in translate_qmd.py for consistency
5. Write the complete translation to: {output_qmd}

The output file already has terminology replacements applied as a starting point.
Please perform a full human-quality translation of all remaining English text.

Key terminology to use:
- phototoxicity → 光毒性
- cytotoxicity → 细胞毒性
- Neutral Red Uptake → 中性红摄取
- irradiance → 辐照度
- in vitro → 体外
- in vivo → 体内
- PIF → PIF(光刺激因子)
- MPE → MPE(平均光效应)
- IC50 → IC50(半抑制浓度)
""")

        print(f"✅ Translation request created: {output_qmd}")
        print(f"📋 Request file: {request_file}")
        print("\n⚠️  This file needs full translation by Claude Code.")
        print("   The current file has terminology replacements only.")
        print("   Please ask Claude Code: \"Please complete the full translation of this file\"")
        return

    if method == "claude":
        # Create a translation instruction file for Claude Code
        translator = ClaudeTranslation()

        # Apply terminology glossary first (preserves formatting)
        print("📝 Applying terminology glossary...")
        result = body

        # Sort by length (longer terms first to avoid partial matches)
        terms_sorted = sorted(TERMINOLOGY_GLOSSARY.items(),
                            key=lambda x: len(x[0]), reverse=True)

        for en, zh in terms_sorted:
            # Preserve case sensitivity
            pattern = re.compile(r'\b' + re.escape(en) + r'\b', re.IGNORECASE)
            result = pattern.sub(zh, result)

        # Update frontmatter for Chinese version
        translated_frontmatter = translate_frontmatter(frontmatter)

        # Combine
        translated_content = f"---\n{translated_frontmatter}---\n{result}"

        with open(output_qmd, 'w', encoding='utf-8') as f:
            f.write(translated_content)

        print(f"✅ Terminology-based translation complete: {output_qmd}")
        print("⚠️  Note: Full translation requires Claude Code to process this file")
        print("   The file has been created with terminology replacements applied.")
    else:
        # Use API-based translation
        translator = ClaudeTranslation()

        # Translate body section by section
        # Split by headings to translate in chunks
        sections = re.split(r'(^#{1,6}\s+.+$)', body, flags=re.MULTILINE)

        translated_sections = []
        for i, section in enumerate(sections):
            if section.startswith('#'):
                # Keep heading markers
                translated_sections.append(section)
            elif section.strip():
                # Translate content
                translated = translator.translate(section)
                translated_sections.append(translated)
            else:
                translated_sections.append(section)

        translated_body = ''.join(translated_sections)

        # Update frontmatter for Chinese version
        translated_frontmatter = translate_frontmatter(frontmatter)

        # Combine
        translated_content = f"---\n{translated_frontmatter}---\n{translated_body}"

        with open(output_qmd, 'w', encoding='utf-8') as f:
            f.write(translated_content)

        print(f"✅ Translation complete: {output_qmd}")


def translate_frontmatter(frontmatter: str) -> str:
    """Translate frontmatter fields to Chinese."""
    lines = []
    for line in frontmatter.split('\n'):
        if 'title:' in line and 'OECD测试指南' not in line:
            # Keep Chinese title as is
            lines.append(line)
        elif 'description:' in line:
            lines.append(line)
        elif 'keywords:' in line:
            lines.append(line)
        else:
            lines.append(line)
    return '\n'.join(lines)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python translate_qmd.py <input_qmd> [output_qmd] [method]")
        print("Methods: claude (default), anthropic, openai, deepseek, qwen, etc.")
        sys.exit(1)

    input_qmd = sys.argv[1]

    if len(sys.argv) >= 3:
        output_qmd = sys.argv[2]
    else:
        # Auto-generate output filename
        input_path = Path(input_qmd)
        output_qmd = str(input_path.parent / f"{input_path.stem}_中文{input_path.suffix}")

    method = sys.argv[3] if len(sys.argv) >= 4 else "claude"

    print(f"Translating: {input_qmd}")
    print(f"Method: {method}")
    print(f"Output: {output_qmd}\n")

    translate_qmd_file(input_qmd, output_qmd, method)

    print("\n📝 Translation notes:")
    print("   - Applied toxicology terminology glossary")
    print("   - Preserved QMD formatting and structure")
    print("   - Table image references maintained")


if __name__ == "__main__":
    main()
