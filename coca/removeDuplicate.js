/**
 * 
用nodejs编写程序，实现：
1、读取../data/COCA60000.txt的内容，该文件每一行是一个单词，将所有单词转为一个数组，注意保持单词顺序不变
2、对单词进行去重处理和去除两侧的空格处理
3、将去重后的单词写入../data/COCA60000_remove_duplicate.txt文件，一个单词一行，注意保持单词顺序不变

请给出代码
 */
const fs = require('fs');
const path = require('path');

const readFilePath = path.join(__dirname, '../data/COCA60000.txt');
const writeFilePath = path.join(
  __dirname,
  '../data/COCA60000_remove_duplicate.txt'
);

fs.readFile(readFilePath, 'utf8', (err, data) => {
  if (err) {
    console.error('Error reading the file:', err);
    return;
  }

  // Split the content into an array of words and remove whitespace
  const words = data.split('\n').map((word) => word.trim());

  // Remove duplicates while preserving order
  const uniqueWords = Array.from(new Set(words));

  // Join the array back into a string with each word on a new line
  const output = uniqueWords.join('\n');

  // Write the output to a new file
  fs.writeFile(writeFilePath, output, 'utf8', (err) => {
    if (err) {
      console.error('Error writing the file:', err);
      return;
    }

    console.log('File written successfully');
  });
});
