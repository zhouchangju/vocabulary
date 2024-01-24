let fs = require('fs');
const path = require('path');
const fileHelper = require('../lib/file');
const pathHelper = require('../lib/path');

function filter(knownWords, rawWords, outputFile) {
  const unknownWords = [];
  let learned = 0;
  rawWords.forEach((word) => {
    if (knownWords.includes(word)) {
      learned++;
    }

    if (!knownWords.includes(word) && Number.isNaN(Number(word.word))) {
      unknownWords.push(word);
    }
  });

  console.log(`已经学会的单词数：${learned}`);
  // 只截取前面一部分背诵
  // const WORD_LENGTH_LIMIT = 6000;
  // unknownWords.splice(WORD_LENGTH_LIMIT);

  fs.writeFileSync(outputFile, unknownWords.join('\r\n'));
}

const dir = path.resolve(__dirname, '.');
const easyWordsFile = dir + '/../data/vocabulary/easy.txt';
const collins35WordsFile = dir + '/../data/vocabulary/collins3-5.txt';

// 需要处理的原始文件
const rawFile = dir + '/data/10000_raw.txt';
// 存放结果的文件
const filteredFile = dir + '/data/10000_filtered.txt';

const rawWords = fileHelper.getWordsFromFile(rawFile);

// 认识的单词
const knownWords = fileHelper
  .getWordsFromFile(easyWordsFile)
  .concat(fileHelper.getWordsFromFile(collins35WordsFile));

// 过滤掉不需要统计的单词(认识的单词)
filter(knownWords, rawWords, filteredFile);
