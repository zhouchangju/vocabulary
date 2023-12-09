let fs = require('fs');
const path = require('path');
const fileHelper = require('../statFrequency/lib/file');
const pathHelper = require('../statFrequency/lib/path');

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
const easyWordsFile = dir + '/../data/easy.txt';
const collins35WordsFile = dir + '/../data/collins3-5.txt';

const rawFile = dir + '/data/8000_raw.txt';
const filteredFile = dir + '/data/8000_filtered.txt';

const rawWords = fileHelper.getWordsFromFile(rawFile);

// 认识的单词
const knownWords = fileHelper
  .getWordsFromFile(easyWordsFile)
  .concat(fileHelper.getWordsFromFile(collins35WordsFile));

// 过滤掉不需要统计的单词(认识的单词)
filter(knownWords, rawWords, filteredFile);
