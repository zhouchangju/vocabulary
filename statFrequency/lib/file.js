let fs = require('fs');
const path = require('path');

function getWordsFromFile(fileName) {
  let words = fs.readFileSync(fileName).toString().split('\n');
  words = words.map((word) => {
    return word.trim();
  });
  return words;
}

module.exports = {
  getWordsFromFile,
};
