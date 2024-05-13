let fs = require('fs');
const path = require('path');

const dir = path.resolve(__dirname, '.');

// Stanford CoreNLP的安装目录
const StanfordCoreNLP_DIR = '/d/software/stanford-corenlp-4.5.5';
// 输出目录
const OUTPUT_DIR = `${dir}/data`;
// 输出文件
const OUTPUT_FILE = `${OUTPUT_DIR}/unknownWords.txt`;

/**
 * 通过stanford-nlp获取单词的原型
 * 用来解决单复数、时态等导致的单词被重复识别的问题
 * 参考资料：https://stanfordnlp.github.io/CoreNLP/
 */
function getOriginOfWordByStanfordNLP(file) {
  const process = require('child_process');
  const cmd = `cd ${StanfordCoreNLP_DIR} && java -mx50g -cp '*' edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators "tokenize,pos,lemma" -outputFormat json   -outputDirectory ${OUTPUT_DIR} -file ${OUTPUT_FILE} && cd ${dir}`;
  process.execSync(cmd);
}

/**
 * 读取Stanford CoreNLP处理后的文件，并添加词频信息
 * @param {*} file
 * @returns
 */
function getOriginOfWordFromFile(file) {
  let nlpResult = require(file);
  const words = {};
  nlpResult['sentences'].forEach((d) => {
    d['tokens'].forEach((t) => {
      if ('undefined' === typeof words[t['lemma']]) {
        words[t['lemma']] = 0;
      }
      words[t['lemma']] += 1;
    });
  });

  let wordArray = [];
  Object.keys(words).forEach((key) => {
    wordArray.push({
      word: key,
      frequency: words[key],
    });
  });

  // 这个词频意义不大了
  wordArray.sort((a, b) => b.frequency - a.frequency);
  return wordArray;
}

function getOriginOfWord(
  knownWords,
  originWordsFile,
  finalFile,
  frequency = 1
) {
  const originWords = getOriginOfWordFromFile(originWordsFile);

  const unknownWords = [];
  originWords.forEach((word) => {
    if (
      !knownWords.includes(word.word) &&
      word.word.length >= 3 &&
      word.frequency >= frequency &&
      Number.isNaN(Number(word.word))
    ) {
      unknownWords.push(word.word);
    }
  });

  fs.writeFileSync(finalFile, unknownWords.join('\r\n'));
}

module.exports = getOriginOfWord;
