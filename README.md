# Learning Vocabulary

最近意识到英语的重要性，工作中越来越多的资料都是英文的，所以决定开始学习英语。

鉴于我这不堪入目的英语水平(词汇量 3000)，第一步必须得先把词汇量提升上去，因此写了个工具辅助我背单词。

这个工具的目的是帮我走捷径(尽量少背单词)，功能主要有如下几个：

1、解析英文 PDF，抽取出单词(用于筛选出专业术语)

2、通过 Stanford CoreNLP 分词，还原词源

3、过滤掉认识的单词

最终生成的单词列表会导入扇贝单词，生成单词书进行背诵。

## 仅过滤掉认识的单词

使用 coca/filter.js

1、设置这 2 个文件的路径

```javascript
// 需要处理的原始文件
const rawFile = dir + '/../data/vocabulary/COCA20000.txt';
// 存放结果的文件
const filteredFile = dir + '/data/20000_filtered.txt';
```

2、执行 `coca/filter.js`

## 通过 Stanford CoreNLP 分词，还原词源后，过滤掉认识的单词

使用 statFrequency/index.js

1、将初步过滤好的单词写入 statFrequency/data/unknownWords.txt

2、执行 Stanford CoreNLP 命令：

```shell
cd /d/software/stanford-corenlp-4.5.5 && \
java -mx50g -cp '*' edu.stanford.nlp.pipeline.StanfordCoreNLP \
-annotators "tokenize,pos,lemma" \
-outputFormat json   \
-outputDirectory /d/git/vocabulary/data/process \
-file /d/git/vocabulary/data/process/unknownWords.txt && \
cd /d/git/vocabulary
```

3、执行 `statFrequency/index.js`

即可在 statFrequency/data/final.txt 中看到最终的单词列表

## 手动筛选认识的单词

1、将初步过滤好的单词写入 data/process/toBeFiltered.txt

2、执行脚本 classify/generateWords.js

3、打开 classify/index.html

4、勾选认识的单词，点击“导出简单词并复制到剪贴板”

5、将剪贴板中的内容粘贴到 classify/easy.js 和 data/easy.txt

6、执行上面的 **仅过滤掉认识的单词** 的步骤

## TODO LIST

- [x] easy 词表只保留一份
- [x] 简单词的筛选做成拖动版，可以拖入单词，拖出单词
- [ ] 实时存储，尽量减少手动文件操作
- [ ] GPT 一键单词解释、造句功能
- [x] Stanford CoreNLP 单词词源查询工具
- [ ] 修改文件结构和命名
- [ ] 优化代码
- [ ] 文章生成器(根据生词和主题，生成文章)

## 用 PDF 生成单词书

1、将 pdf 文件(可以是多个)放入 data/pdf 目录下

2、执行脚本 `statFrequency/pdf2text.js`，会将所有 pdf 文件的内容写入 data/process/pdf.txt 中

3、执行 Stanford CoreNLP 命令：

```shell
cd /d/software/stanford-corenlp-4.5.5 && \
java -mx50g -cp '*' edu.stanford.nlp.pipeline.StanfordCoreNLP \
-annotators "tokenize,pos,lemma" \
-outputFormat json   \
-outputDirectory /d/git/vocabulary/data/process \
-file /d/git/vocabulary/data/process/pdf.txt && \
cd /d/git/vocabulary
```

4、执行 `statFrequency/index.js`的如下逻辑：

```javascript
// 认识的单词
const knownWords = fileHelper
  .getWordsFromFile(easyWordsFile)
  .concat(fileHelper.getWordsFromFile(collins35WordsFile));

// 最后一个参数是保留的词频设置，即词频大于等于 3 的单词会被保留
getOriginOfWord(knownWords, originWordsFile, finalFile, 3);
```

即可在 statFrequency/data/final.txt 中看到最终的单词列表
