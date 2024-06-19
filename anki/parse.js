/**
 * 解析HTML结构，提取中英文内容
 */
const topics = {};
let topic = '';
var container = document.getElementById('article-container');

for (var i = 0; i < container.children.length; i++) {
  var child = container.children[i];
  var tagName = child.tagName; // 获取标签名

  // 判断标签类型并执行相应操作
  switch (tagName) {
    case 'H3':
      console.log('这是一个 h3 元素');
      var id = child.getAttribute('id'); // 获取id属性的值
      topic = id;
      topics[topic] = [];
      console.log('子元素的ID是:', id);
      break;
    case 'UL':
      console.log('这是一个 ul 元素');

      // 获取所有li元素
      var liElements = child.querySelectorAll('li');

      liElements.forEach(function (li) {
        let chinese = '';
        // 获取p元素的所有子节点
        var pChildren = li.querySelector('p').childNodes;

        // 遍历子节点，寻找p和br之间的文本
        var textContent = '';
        pChildren.forEach(function (node, index) {
          if (node.nodeName === '#text') {
            // 这是一个文本节点
            // 将文本节点的内容添加到textContent字符串
            textContent += node.textContent;
          } else if (node.nodeName === 'BR') {
            // 如果是br节点，结束当前文本的收集
            console.log('中文：', textContent); // 显示p和br之间的文本
            chinese = textContent;
            textContent = '';
          }
        });

        // 获取code元素的内容
        var codeContent = li.querySelector('code').textContent;
        console.log('code元素的内容是:', codeContent);

        topics[topic].push({
          chinese,
          english: codeContent,
        });
      });

      break;
    // 可以继续添加更多的case来匹配其他标签
    default:
      console.log('这是一个 ' + tagName + ' 元素');
  }
}

console.log('topics:', topics);
