/**
 * 生成单词表格
 * 注意用PowerShell运行，并指定编码为UTF8
 * [Console]::OutputEncoding = [System.Text.Encoding]::UTF8; node .\generateExcel.js > ..\data\words.xlsx
 */
const words = require('./words');

words.forEach((wordObj) => {
  const { word, definition } = wordObj;
  if (word && definition) {
    console.log(`${word}\t${definition}`);
  }
});
