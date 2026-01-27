# TOEFL词汇分类系统 - 使用说明

## 系统完成状态

✅ **所有任务已完成！**

### 已完成的功能

1. ✅ **Python分类器核心模块**
   - 词族提取器 (lemmatizer.py)
   - 频率分级器 (frequency_grader.py)
   - 情感分析器 (emotion_analyzer.py)
   - 语域标记器 (register_tagger.py)
   - 主编排器 (orchestrator.py)

2. ✅ **词汇处理**
   - 已处理5999个TOEFL单词
   - 生成分类数据：`data/vocabulary/TOEFL_CLASSIFIED.json`
   - 处理速度：2.2ms/词

3. ✅ **Web交互界面**
   - 多维度筛选系统
   - 词卡片展示
   - 导出功能（Anki CSV、Markdown）

---

## 如何使用Web UI

### 方法1：直接打开（推荐）

```bash
# 在浏览器中打开
open web-ui/index.html

# 或者手动导航
cd web-ui
# 然后在浏览器中打开 index.html
```

### 方法2：使用本地服务器（如果遇到CORS问题）

```bash
# Python 3
cd web-ui
python3 -m http.server 8000

# 然后在浏览器访问
# http://localhost:8000/index.html
```

---

## Web UI功能说明

### 筛选器

**搜索框**
- 输入单词进行实时搜索（300ms防抖）

**频率筛选**
- Band 1（非常常见）：前3000词
- Band 2（常见）：3000-5000
- Band 3（中等）：5000-10000
- Band 4（较少）：10000-20000
- Band 5（稀有）：20000+

**情感筛选**
- 😊 积极情感
- 😞 消极情感
- 😐 中性

**语域筛选**
- 🎩 正式（学术/正式场合）
- 😐 中性（通用）
- 💬 非正式（日常对话）
- 🤪 俚语

**词性筛选**
- 名词
- 动词
- 形容词
- 副词

### 操作按钮

- **Apply Filters**: 应用筛选条件
- **Clear Filters**: 清除所有筛选
- **Select All**: 全选/取消全选当前显示的词
- **Show selected only**: 只显示已选择的词

### 导出功能

**Export to Anki**
- 生成Anki导入格式的CSV文件
- 包含正面（单词）和背面（详细信息）
- 带标签（频率、情感、语域、词性）

**Export Markdown**
- 生成Markdown格式文档
- 按语域分组
- 包含所有分类元数据

---

## 数据说明

### 词族（Word Family）
每个单词包含：
- 词元（lemma）：词的基本形式
- 词族列表：相关词的所有形式
- 词性：名词/动词/形容词/副词

例如：
```
predator
├── Lemma: predator
├── POS: NOUN
└── Word Family: [marauder, piranha, predator, predators,
                  predatory-animal, vulture, ...]
```

### 频率分级
基于COCA语料库：
- **Band 1**: 前3000词（必须掌握）
- **Band 2**: 3000-5000（高频词）
- **Band 3**: 5000-10000（中频词）
- **Band 4**: 10000-20000（低频词）
- **Band 5**: 20000+（稀有词）
- **Beyond**: 不在语料库中

### 情感分析
基于NRC情感词典 + 启发式分析：
- 主导情感（primary）
- 详细情感列表（emotions）
- 来源：NRC词库或启发式

### 语域标记
基于使用场景分类：
- **Formal**: 学术论文、正式文档
- **Neutral**: 新闻、通用文本
- **Informal**: 日常对话、邮件
- **Slang**: 非正式场合、网络用语

---

## 处理新词汇

如需处理新的词汇列表：

```bash
# 激活虚拟环境
source venv/bin/activate

# 运行处理脚本
python process_toefl_words.py

# 更新Web UI数据
cp data/vocabulary/TOEFL_CLASSIFIED.json web-ui/data/vocabulary/

# 刷新浏览器即可看到更新
```

---

## 项目结构

```
vocabulary/
├── toefl_classifier/          # 分类器核心模块
│   ├── lemmatizer.py          # 词族提取
│   ├── frequency_grader.py    # 频率分级
│   ├── emotion_analyzer.py    # 情感分析
│   ├── register_tagger.py     # 语域标记
│   ├── orchestrator.py        # 主编排器
│   └── data/                  # 语言数据库
│       ├── coca_frequency.txt
│       └── nrc_emotion_lexicon.txt
├── web-ui/                    # Web交互界面
│   ├── index.html             # 主页面
│   ├── css/
│   │   └── styles.css         # 样式
│   ├── js/
│   │   ├── data.js            # 数据管理
│   │   ├── filters.js         # 筛选逻辑
│   │   ├── display.js         # 渲染逻辑
│   │   ├── export.js          # 导出功能
│   │   └── main.js            # 主应用
│   └── data/
│       └── vocabulary/
│           └── TOEFL_CLASSIFIED.json
├── data/vocabulary/
│   ├── TOEFL_2000_AND_GREEN_BOOK_UNIQUE.txt  # 原始词汇
│   └── TOEFL_CLASSIFIED.json                 # 分类结果
└── process_toefl_words.py     # 批处理脚本
```

---

## 技术栈

**后端（Python）**
- NLTK: 自然语言处理
- spaCy: 词性标注和依存分析
- WordNet: 语义关系数据库
- NRC Emotion Lexicon: 情感分析

**前端（HTML/CSS/JavaScript）**
- 原生JavaScript（无框架）
- Fetch API: 数据加载
- 响应式设计：移动端友好

---

## 学习建议

1. **高频词优先**：先用频率筛选学习Band 1-2的词
2. **按情感分组**：积极/消极情感词汇分开记忆
3. **关注词族**：通过词族系统学习单词变形
4. **语域意识**：了解正式/非正式用词的差别
5. **导出Anki**：使用间隔重复系统巩固记忆

---

## 故障排除

**Web UI无法加载数据？**
- 检查浏览器控制台（F12）查看错误信息
- 确保TOEFL_CLASSIFIED.json在web-ui/data/vocabulary/目录
- 尝试使用本地服务器而不是直接打开文件

**筛选结果为空？**
- 点击"Clear Filters"清除所有筛选
- 检查是否有词汇数据加载成功
- 查看页面顶部的结果计数

**导出功能不工作？**
- 确保已选择单词（点击词卡片或使用"Select All"）
- 检查浏览器下载文件夹
- 查看浏览器控制台是否有错误

---

## 下一步改进

可选的增强功能：

1. **添加发音**：集成Web Speech API
2. **例句展示**：从语料库提取例句
3. **学习进度**：Local Storage记忆状态
4. **更多导出格式**：Quizlet、Pleco等
5. **词根词缀**：etymology信息
6. **搭配词典**：collocations数据
7. **难度评级**：基于多个因素的综合评分

---

**祝学习愉快！** 📚✨
