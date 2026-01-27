# COCA频率数据下载指南

## 为什么需要COCA数据？

当前TOEFL词汇分类器中的所有单词都标记为"Beyond"（不在COCA语料库中），这是因为：

1. COCA (Corpus of Contemporary American English) 数据需要手动下载
2. 数据文件受版权保护，需要注册账号免费获取
3. 下载后需要正确格式化才能使用

## 下载步骤

### 1. 访问COCA官网

打开浏览器访问：
```
https://www.wordfrequency.info/free.asp?s=y
```

### 2. 免费注册

- 点击页面上的"Sign up"或"Register"链接
- 填写注册表单（免费）
- 验证邮箱账号
- 登录到网站

### 3. 下载数据

登录后：
1. 找到 **"COCA 20000 word frequency list"** 或类似名称的下载链接
2. 选择 **Text format** (文本格式)
3. 下载文件（通常命名为类似 `coca20000.txt`）

### 4. 格式化数据

下载的文件可能是Tab分隔或逗号分隔的格式，预期格式如下：

```
word	rank
the	1
be	2
of	3
and	4
a	5
```

**重要：** 确保文件只有两列（单词 + 排名），没有表头或多余信息

### 5. 安装数据文件

将格式化后的数据文件保存到：
```
toefl_classifier/data/coca_frequency.txt
```

**替换现有的占位符文件**

### 6. 重新处理词汇

运行处理脚本：
```bash
cd /Users/leozhou/git/vocabulary
source venv/bin/activate
python process_toefl_words.py
```

### 7. 更新Web UI

```bash
cp data/vocabulary/TOEFL_CLASSIFIED.json web-ui/data/vocabulary/
```

刷新浏览器即可看到正确的频率分级！

---

## 验证数据格式

正确的coca_frequency.txt格式示例：

```
the	1
be	2
of	3
and	4
a	5
in	6
to	7
it	8
that	9
you	10
he	11
was	12
for	13
on	14
are	15
as	16
with	17
his	18
they	19
I	20
```

**注意：**
- 每行一个单词
- 单词和排名之间用Tab分隔
- 不要有表头行
- 纯文本格式（UTF-8编码）

---

## 如果没有COCA数据怎么办？

**不影响使用！** 分类器仍然可以工作：

### 功能仍然可用：
- ✅ **Word Family** - 词族提取（基于WordNet和spaCy）
- ✅ **Emotion** - 情感分析（基于NRC词库 + 启发式）
- ✅ **Register** - 语域标记（基于启发式分析）
- ✅ **POS** - 词性标注（基于spaCy）
- ✅ **Web UI** - 完整的筛选和导出功能

### 唯一的限制：
- ⚠️ **Frequency分级** - 所有单词显示为"Rare"（Beyond）
- 勾选"Beyond"筛选即可查看所有单词

### 替代方案：
- 使用"搜索"功能查找特定单词
- 按"情感"、"语域"、"词性"筛选
- 所有其他功能完全正常

---

## 常见问题

### Q: COCA数据免费吗？
A: 是的，通过免费注册账号即可下载20000词的频率列表。

### Q: 必须下载COCA数据吗？
A: 不是必须的。没有COCA数据，所有单词标记为"Beyond"，但其他功能正常工作。

### Q: 可以上传到GitHub吗？
A: 不建议。COCA数据受版权保护，请勿上传到公开仓库。已在`.gitignore`中忽略。

### Q: 有其他替代数据源吗？
A: 可以使用其他频率数据，但需要格式化为相同的"单词<Tab>排名"格式。

---

## 技术说明

### 数据用途

COCA频率数据用于：
1. **Frequency Grading** - 将单词分为5个频率等级
2. **TOEFL优先级** - 识别高频词（Band 1-2）
3. **学习策略** - 优先学习高频词

### 频率等级定义

- **Band 1** (Top 3K): 前3000词 - 最常见，必须掌握
- **Band 2** (Common): 3000-5000词 - 常用词
- **Band 3** (Moderate): 5000-10000词 - 中频词
- **Band 4** (Low): 10000-20000词 - 低频词
- **Band 5** (Rare): 20000+词 - 稀有词
- **Beyond**: 不在COCA语料库中

---

## 需要帮助？

如果遇到问题：
1. 检查文件格式是否正确（Tab分隔，两列）
2. 确认文件路径：`toefl_classifier/data/coca_frequency.txt`
3. 重新运行处理脚本
4. 刷新浏览器查看结果
