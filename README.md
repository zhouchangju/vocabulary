# Learning Vocabulary

本项目致力于通过程序化手段提升英语学习效率。

## 1. 托福精品词书 PDF 处理 (图像扫描版 V6)

针对《学而思国际托福改革后一站式精品词书》(图像扫描版 PDF) 的特殊排版，本项目开发了基于 OCR 和图像预处理的精确提取方案。

**主要功能：**
- **高精度提取**：3.0x 缩放渲染，自动滤除背景红蓝横线，保留主单词，忽略音标、释义和例句。
- **PDF 切分**：将体积巨大的扫描版 PDF 均匀切分为 10 个子文件，方便分段阅读和处理。

**执行命令：**
```bash
# 单词提取 (V6 最终版)
python3 scripts/extract_toefl_pdf.py

# PDF 分块切分 (均匀切分为 10 份)
python3 scripts/split_pdf.py
```
详情参考：[托福 PDF 处理方案](./docs/TOEFL_PDF_EXTRACTION_GUIDE.md)

---

## 2. 词汇比对与筛选

通过比对不同的词汇源，筛选出新增词汇。

**执行命令：**
```bash
# 比对 KMF 新词库与原有词库，提取新增词汇
python3 scripts/compare_kmf_toefl.py
```
- **输出路径**：`data/vocabulary/KMF_EXCLUSIVE_WORDS.txt`

---

## 3. 词汇标注与导出生词本 (HTML 工具)

利用交互式网页工具，快速划掉认识的词汇，保留生词并导出。

### 功能亮点：
- **极简标注**：一行一个单词，单词后跟随“认识/生词”切换按钮，点击即标记。
- **自动释义**：脚本自动为 1500+ 个单词多线程补全中文释义。
- **数据持久化**：标注状态实时保存于浏览器 `localStorage` 中。
- **快速导出**：点击右上角按钮，将所有非“认识”状态的词一键导出为 TXT。

### 执行步骤：
1. **生成工具**：
   ```bash
   python3 scripts/generate_vocab_tool.py
   ```
2. **开始标注**：使用浏览器打开根目录下的 `vocab_marker.html` 即可。

---

## 4. 其它功能

### 词源还原与词频统计 (Stanford CoreNLP)
- 执行 `statFrequency/pdf2text.js` 解析 PDF 文字。
- 执行 `statFrequency/index.js` 还原词源并过滤已知单词。

> **配置提示**：
> 如果本地路径不同，可使用环境变量覆盖默认路径：
> - `STANFORD_CORENLP_DIR`：CoreNLP 安装目录
> - `CORENLP_OUTPUT_DIR`：CoreNLP 输出目录
> - `CORENLP_OUTPUT_FILE`：CoreNLP 输出文件
> - `RUN_CORENLP=true`：在运行 `statFrequency/index.js` 时自动执行 CoreNLP
> - `MIN_WORD_LENGTH` / `MIN_WORD_FREQUENCY` / `WORD_LIMIT`：过滤阈值配置

---

## TODO LIST

<!-- Agent Swarm Test: Comment added on 2026-02-27 to verify agent swarm functionality in worktree -->
- [x] easy 词表只保留一份
- [x] 图像版 PDF 单词高精度 OCR 提取 (V6)
- [x] 网页版单词快速标注工具 (LocalStorage)
- [ ] GPT 一键单词解释、造句功能
- [x] 项目结构优化与脚本归档
- [ ] 优化代码
- [ ] 文章生成器(根据生词和主题，生成文章)
