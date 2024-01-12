# Learning Vocabulary

Tools to learn vocabulary

## 仅过滤掉认识的单词

使用 coca/filter.js

1、设置这 2 个文件的路径

```javascript
// 需要处理的原始文件
const rawFile = dir + '/../data/COCA20000.txt';
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
-outputDirectory /d/git/vocabulary/statFrequency/data \
-file /d/git/vocabulary/statFrequency/data/unknownWords.txt && \
cd /d/git/vocabulary
```

3、执行 `statFrequency/index.js`

即可在 statFrequency/data/final.txt 中看到最终的单词列表

## 手动筛选认识的单词

1、将初步过滤好的单词写入 classify/raw.js

2、打开 classify/index.html

3、勾选认识的单词，点击“导出简单词并复制到剪贴板”

4、将剪贴板中的内容粘贴到 classify/easy.js 和 data/easy.txt

5、执行上面的 **仅过滤掉认识的单词** 的步骤

## TODO LIST

- [ ] easy 词表只保留一份
- [ ] 简单词的筛选做成拖动版，可以拖入单词，拖出单词，且实时存储，尽量减少手动文件操作
- [ ] GPT 一键单词解释、造句功能
- [ ] Stanford CoreNLP 单词词源查询工具
- [ ] 修改文件结构和命名
- [ ] 优化代码
- [ ] 文章生成器(根据生词和主题，生成文章)
