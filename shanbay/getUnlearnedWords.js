/**
 * 抓取未学单词
 * 操作步骤：
 * 1、进入扇贝单词网页版：https://web.shanbay.com/wordsweb/#/words-table
 * 2、复制本脚本，放入console中执行
 */

/**
 * sleep方法
 * @param {*} ms
 */
let sleep = (ms) => {
  return new Promise((resolve) => setTimeout(resolve, ms));
};

function toNextPage() {
  // 获取当前页的分页按钮
  const activeLi = document.querySelector('.index_activePage__3C9pk');

  // 获取分页按钮的下一个兄弟元素即下一页按钮
  const nextLi = activeLi.nextElementSibling;

  // 触发下一页的点击事件
  nextLi.click();
}

function getWords() {
  const words = [];

  // 获取当前页面所有的单词卡片元素(是一些li元素)
  const wordElements = document.querySelectorAll('.index_word__3waO0');

  // 解析单词卡片
  wordElements.forEach((wordElement) => {
    // 单词文本
    const word = wordElement.querySelector('.index_wordName__1lkbV').innerText;
    words.push(word);
    // 单词释义
    const definition = wordElement.querySelector(
      '.index_bottom__XLoPQ'
    ).innerText;
    words.push({
      word,
      definition,
    });
  });

  return words;
}

async function main(startPage, endPage) {
  const unlearnedWords = [];
  for (let i = startPage; i <= endPage; i++) {
    console.log(`开始解析第${i}页`);
    const words = getWords();
    unlearnedWords.push(...words);
    console.log(words);
    if (i % 100 === 0) {
      console.log(JSON.stringify(unlearnedWords));
    }
    toNextPage();
    const sleepTime = Math.random() * 2000 + 2000;
    await sleep(sleepTime);
  }
  console.error('最终结果：');
  console.log(JSON.stringify(unlearnedWords));
}

main(1, 792);
