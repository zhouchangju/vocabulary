let fs = require('fs');
const path = require('path');
const pathHelper = require('../lib/path');
const { normalizeWord, isNumeric } = require('../lib/words');

function filter(knownWords, inputFile, outputFile) {
  const content = fs.readFileSync(inputFile).toString();
  let words;
  try {
    words = JSON.parse(content);
  } catch (error) {
    throw new Error(`Invalid JSON in ${inputFile}: ${error.message}`);
  }
  const knownWordSet = new Set(knownWords.map((word) => normalizeWord(word)));

  const minLength = Number.parseInt(process.env.MIN_WORD_LENGTH ?? '3', 10);
  const minFrequency = Number.parseInt(
    process.env.MIN_WORD_FREQUENCY ?? '3',
    10
  );
  const wordLimit = Number.parseInt(process.env.WORD_LIMIT ?? '6000', 10);

  const unknownWords = [];
  const unknownWordArr = [];
  let learned = 0;
  words.forEach((word) => {
    const normalized = normalizeWord(word.word);
    if (!normalized) {
      return;
    }
    if (knownWordSet.has(normalized)) {
      learned++;
    }

    if (
      !knownWordSet.has(normalized) &&
      normalized.length >= minLength &&
      word.frequency >= minFrequency &&
      !isNumeric(normalized)
    ) {
      unknownWords.push(normalized);
      unknownWordArr.push({ ...word, word: normalized });
    }
  });

  console.log(`已经学会的单词数：${learned}`);
  // 只截取前面一部分背诵
  if (wordLimit > 0) {
    unknownWords.splice(wordLimit);
    unknownWordArr.splice(wordLimit);
  }

  fs.writeFileSync(outputFile, unknownWords.join('\r\n'));

  let fileName = pathHelper.getBasePath(outputFile);
  fs.writeFileSync(fileName + '.json', JSON.stringify(unknownWordArr));
}

module.exports = filter;
