let fs = require('fs');
const path = require('path');
const pathHelper = require('../lib/path');

function filter(knownWords, inputFile, outputFile) {
  const content = fs.readFileSync(inputFile).toString();
  const words = JSON.parse(content);

  const unknownWords = [];
  const unknownWordArr = [];
  let learned = 0;
  words.forEach((word) => {
    if (knownWords.includes(word.word)) {
      learned++;
    }

    if (
      !knownWords.includes(word.word) &&
      word.word.length >= 3 &&
      word.frequency >= 3 &&
      Number.isNaN(Number(word.word))
    ) {
      unknownWords.push(word.word);
      unknownWordArr.push(word);
    }
  });

  console.log(`已经学会的单词数：${learned}`);
  // 只截取前面一部分背诵
  const WORD_LENGTH_LIMIT = 6000;
  unknownWords.splice(WORD_LENGTH_LIMIT);
  unknownWordArr.splice(WORD_LENGTH_LIMIT);

  fs.writeFileSync(outputFile, unknownWords.join('\r\n'));

  let fileName = pathHelper.getBasePath(outputFile);
  fs.writeFileSync(fileName + '.json', JSON.stringify(unknownWordArr));
}

module.exports = filter;
