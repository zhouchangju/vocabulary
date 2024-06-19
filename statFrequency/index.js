/**
 * 解析文本文件，统计词频
 */
let fs = require('fs');
const path = require('path');
const countWordFrequency = require('./countWordFrequency');
const filter = require('./filter');
const fileHelper = require('../lib/file');
const getOriginOfWord = require('./getOriginOfWord');

const dir = path.resolve(__dirname, '.');

const easyWordsFile = dir + '/../data/vocabulary/easy.txt';
const collins35WordsFile = dir + '/../data/vocabulary/collins3-5.txt';
const originFile = dir + '/../data/process/content.txt';
const wordFrequencyFile = dir + '/../data/process/output.json';
const filteredFile = dir + '/../data/process/unknownWords.txt';
const originWordsFile = dir + '/../data/process/content.txt.json';
const finalFile = dir + '/../data/process/final.txt';
const invalidFile = dir + '/../data/process/invalid.txt';

// 统计文件中每个单词出现的次数
// countWordFrequency(originFile, wordFrequencyFile);

// 认识的单词
let knownWords = fileHelper
  .getWordsFromFile(easyWordsFile)
  .concat(fileHelper.getWordsFromFile(collins35WordsFile));

// 过滤掉不需要统计的单词(认识的单词)
// filter(knownWords, wordFrequencyFile, filteredFile);
// TODO:调用Stanford CoreNLP获取单词的原型

// (临时，待注释)过滤掉不合法的单词(识别错误的非正常单词)
// const finalWords = fileHelper.getWordsFromFile(finalFile);
// const invalidWords = fileHelper.getWordsFromFile(invalidFile);
// const validWords = finalWords.filter((word) => !invalidWords.includes(word));
// fs.writeFileSync(finalFile, validWords.join('\r\n'));

// TODO:调用Stanford CoreNLP获取单词的原型

// 如果无需过滤认识的单词，则开启下面这一行
knownWords = [];

// 再次过滤掉不需要统计的单词(认识的单词)
// 如果无需过滤认识的单词，请注意把最后一个参数设置为1
getOriginOfWord(knownWords, originWordsFile, finalFile, 1);
