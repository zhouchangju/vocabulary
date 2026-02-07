let fs = require('fs');
const path = require('path');
const { normalizeWord, isNumeric } = require('../lib/words');

const dir = path.resolve(__dirname, '.');

// Stanford CoreNLP的安装目录
const StanfordCoreNLP_DIR =
  process.env.STANFORD_CORENLP_DIR || '/d/software/stanford-corenlp-4.5.5';
// 输出目录
const OUTPUT_DIR = process.env.CORENLP_OUTPUT_DIR || `${dir}/data`;
// 输出文件
const OUTPUT_FILE = process.env.CORENLP_OUTPUT_FILE || `${OUTPUT_DIR}/unknownWords.txt`;

/**
 * 通过stanford-nlp获取单词的原型
 * 用来解决单复数、时态等导致的单词被重复识别的问题
 * 参考资料：https://stanfordnlp.github.io/CoreNLP/
 */
function getOriginOfWordByStanfordNLP(file) {
  const process = require('child_process');
  if (!fs.existsSync(StanfordCoreNLP_DIR)) {
    throw new Error(`Stanford CoreNLP dir not found: ${StanfordCoreNLP_DIR}`);
  }
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  const targetFile = file || OUTPUT_FILE;
  if (!fs.existsSync(targetFile)) {
    throw new Error(`CoreNLP input not found: ${targetFile}`);
  }
  const cmd = `cd ${StanfordCoreNLP_DIR} && java -mx50g -cp '*' edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators "tokenize,pos,lemma" -outputFormat json -outputDirectory ${OUTPUT_DIR} -file ${targetFile} && cd ${dir}`;
  process.execSync(cmd);
}

/**
 * 读取Stanford CoreNLP处理后的文件，并添加词频信息
 * @param {*} file
 * @returns
 */
function getOriginOfWordFromFile(file) {
  if (!fs.existsSync(file)) {
    throw new Error(`CoreNLP output not found: ${file}`);
  }
  const content = fs.readFileSync(file, 'utf8');
  let nlpResult = JSON.parse(content);
  const words = {};
  nlpResult['sentences'].forEach((d) => {
    d['tokens'].forEach((t) => {
      const lemma = normalizeWord(t['lemma']);
      if (!lemma) {
        return;
      }
      if ('undefined' === typeof words[lemma]) {
        words[lemma] = 0;
      }
      words[lemma] += 1;
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
  const knownWordSet = new Set(knownWords.map((word) => normalizeWord(word)));
  const minLength = Number.parseInt(process.env.MIN_WORD_LENGTH ?? '3', 10);

  const unknownWords = [];
  originWords.forEach((word) => {
    const normalized = normalizeWord(word.word);
    if (!normalized) {
      return;
    }
    if (
      !knownWordSet.has(normalized) &&
      normalized.length >= minLength &&
      word.frequency >= frequency &&
      !isNumeric(normalized)
    ) {
      unknownWords.push(normalized);
    }
  });

  fs.writeFileSync(finalFile, unknownWords.join('\r\n'));
}

getOriginOfWord.runCoreNLP = getOriginOfWordByStanfordNLP;
module.exports = getOriginOfWord;
