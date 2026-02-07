let fs = require('fs');
const path = require('path');
const { normalizeWord } = require('./words');

function getWordsFromFile(fileName) {
  let words = fs.readFileSync(fileName).toString().split('\n');
  words = words.map((word) => {
    return normalizeWord(word);
  }).filter((word) => word.length > 0);
  return words;
}

module.exports = {
  getWordsFromFile,
};
