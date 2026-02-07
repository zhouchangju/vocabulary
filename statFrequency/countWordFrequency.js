let fs = require('fs');
const path = require('path');
const { splitContentToWords } = require('../lib/words');
// 频率限制，<=这个频率的，就忽略掉
const FREQUENCY_LIMIT = 3;

function countWordsForFile(fileName) {
  console.log(fileName);
  const content = fs.readFileSync(fileName).toString();
  let words = splitContentToWords(content);
  let wordMap = {};
  words.forEach((word) => {
    if ('undefined' === typeof wordMap[word]) {
      wordMap[word] = 0;
    }
    wordMap[word]++;
  });

  const statArr = [];
  Object.keys(wordMap).forEach((word) => {
    // TODO:待调整参数
    if (wordMap[word] >= FREQUENCY_LIMIT) {
      statArr.push({
        word,
        frequency: wordMap[word],
      });
    }
  });

  statArr.sort((a, b) => {
    return b.frequency - a.frequency;
  });

  return statArr;
}

function countWordFrequency(inputFile, outputFile) {
  const words = countWordsForFile(inputFile);
  fs.writeFileSync(outputFile, JSON.stringify(words));

  // const uniqWords = [];
  // words.forEach((word) => {
  //   uniqWords.push(word.word);
  // });
  // fs.writeFileSync(dir + '/data/uniqWords.txt', uniqWords.join('\r\n'));
}

module.exports = countWordFrequency;
