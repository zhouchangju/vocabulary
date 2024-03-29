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
const originFile = dir + '/../data/process/novel.txt';
const wordFrequencyFile = dir + '/../data/process/output.json';
const filteredFile = dir + '/../data/process/unknownWords.txt';
const originWordsFile = dir + '/../data/process/unknownWords.txt.json';
const finalFile = dir + '/../data/process/final.txt';

// 统计文件中每个单词出现的次数
// countWordFrequency(originFile, wordFrequencyFile);

// 认识的单词
const knownWords = fileHelper
  .getWordsFromFile(easyWordsFile)
  .concat(fileHelper.getWordsFromFile(collins35WordsFile));

// 过滤掉不需要统计的单词(认识的单词)
// filter(knownWords, wordFrequencyFile, filteredFile);
// TODO:调用Stanford CoreNLP获取单词的原型

// 再次过滤掉不需要统计的单词(认识的单词)
getOriginOfWord(knownWords, originWordsFile, finalFile);
