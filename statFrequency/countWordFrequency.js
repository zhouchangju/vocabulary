let fs = require('fs');
const path = require('path');
// 频率限制，<=这个频率的，就忽略掉
const FREQUENCY_LIMIT = 3;

function trim(str) {
  // 使用正则表达式删除开头和结尾的空白字符
  return str.replace(/^\s+|\s+$/g, '');
}

function countWordsForFile(fileName) {
  console.log(fileName);
  const content = fs.readFileSync(fileName).toString();
  let words = splitContentToWords(content);
  let wordMap = {};
  words.forEach((word) => {
    word = trim(word.toLowerCase());
    if ('' !== word && 'undefined' === typeof wordMap[word]) {
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

/**
 * 将文本拆分为单词
 * TODO:换行导致单词被截断的情况，尚未处理
 * @param {*} content
 */
function splitContentToWords(content) {
  var reg = new RegExp(
    '\r\n|\n|,|\\.|:|’|”|“|‘|’|？|…|\\!|！|\\?|~|\\)|\\(|\\+|\\-|\\*|>|<|%|=|"',
    'g'
  );
  return content.replace(reg, ' ').toLowerCase().split(' ');
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
