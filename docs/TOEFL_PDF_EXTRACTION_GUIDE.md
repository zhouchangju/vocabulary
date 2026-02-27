# 学而思托福精品词书 PDF 处理方案 (V6 最终版)

本文档详细介绍了如何处理《学而思国际托福改革后一站式精品词书》这一大型图像版 PDF。

## 1. 单词提取方案 (V6 Ultimate Precise)

针对扫描版 PDF 的复杂排版和背景干扰，我们最终采用了 **V6 高精度提取方案** (`scripts/extract_toefl_pdf.py`)。

### 技术核心：
- **3.0 倍超清渲染**：通过 `fitz` 以 300% 比例渲染页面左侧关键区域。
- **黑通道分量过滤**：利用 RGB 阈值 (RGB < 125) 剔除干扰 OCR 的红蓝背景行线。
- **智能碎片拼接**：自动识别并重新组合因背景干扰被 OCR 切断的长单词。
- **条目锚定逻辑**：基于每页固定 6 个词条的特征，精准锁定主单词位置，排除例句和释义干扰。

### 执行提取：
```bash
python3 scripts/extract_toefl_pdf.py
```
- **输出**：`data/vocabulary/TOEFL_V6_FINAL.txt`

---

## 2. PDF 文件切分

由于原始 PDF 体积巨大（约 250MB），我们提供了 `scripts/split_pdf.py` 脚本将其均匀切分为 10 个较小的文件。

### 功能特点：
- **逻辑分块**：自动计算页数，确保切分点在页面之间，不会截断单词。
- **自动命名**：生成的文件名包含页码范围，如 `TOEFL_Part_01_001-077.pdf`。

### 执行切分：
```bash
python3 scripts/split_pdf.py
```
- **输出目录**：`data/vocabulary/pdf_chunks/`
