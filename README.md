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

Stanford CoreNLP 命令：

```shell
cd /d/software/stanford-corenlp-4.5.5 && java -mx50g -cp '*' edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators "tokenize,pos,lemma" -outputFormat json   -outputDirectory /d/git/vocabulary/statFrequency/data -file /d/git/vocabulary/statFrequency/data/unknownWords.txt && cd /d/git/vocabulary
```
