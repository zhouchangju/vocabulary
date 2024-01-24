let fs = require('fs');
const path = require('path');
const fileHelper = require('../lib/file');

const dir = path.resolve(__dirname, '.');
const easyWordsFile = dir + '/../data/vocabulary/easy.txt';
const toBeFilteredWordsFile = dir + '/../data/process/toBeFiltered.txt';

// 认识的单词
const easyWords = fileHelper.getWordsFromFile(easyWordsFile);
const toBeFilteredWords = fileHelper.getWordsFromFile(toBeFilteredWordsFile);

fs.writeFileSync(
  `${dir}/data/easy.js`,
  `let easy = ${JSON.stringify(easyWords)}`
);

fs.writeFileSync(
  `${dir}/data/raw.js`,
  `let words = ${JSON.stringify(toBeFilteredWords)}`
);
