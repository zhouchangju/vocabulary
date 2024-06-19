/***
 * node.exe "d:\git\vocabulary\anki\import.js" > 900.csv
 */

const fs = require('fs');
const path = require('path');

// 指定文件路径
const filePath = path.join(__dirname, 'topics.json');

// 读取文件内容
fs.readFile(filePath, 'utf8', (err, fileContents) => {
  if (err) {
    console.error('读取文件时发生错误:', err);
    return;
  }

  try {
    // 将文件内容解析为JSON对象
    const topics = JSON.parse(fileContents);
    generateTabulation(topics);
  } catch (parseError) {
    console.error('解析JSON时发生错误:', parseError);
  }
});

function generateTabulation(topics) {
  // anki的字段分割符
  const SPLIT_CHAR = '|';
  Object.keys(topics).forEach((topic) => {
    const question = `<h2>${topic}</h2>`;
    // console.log(`${topic}`);
    const answer = ['<div style="text-align:left">'];
    topics[topic].forEach((item, index) => {
      const color = index % 2 === 0 ? '#eee' : 'white';
      answer.push(
        `<div style="background-color:${color}"><h3>${item.english}</h3><p>${item.chinese}</p></div>`
      );
      // console.log(`${item.english}`);
    });
    answer.push('</div>');
    console.log(`${question}${SPLIT_CHAR}${answer.join('')}`);
  });
}
