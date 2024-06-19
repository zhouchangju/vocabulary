/*
 * @Description: 将指定目录中的所有PDF文件解析为一个text文件
 * 依赖这个包：
 * https://github.com/modesty/pdf2json
 * npm install pdf2json
 *
 */
let fs = require('fs');
const path = require('path');
const dir = path.resolve(__dirname, '.');

function convertPDF2Txt(PDFFile, textFile) {
  PDFParser = require('pdf2json');
  let pdfParser = new PDFParser(this, 1);
  pdfParser.on('pdfParser_dataError', (errData) =>
    console.error(errData.parserError)
  );
  pdfParser.on('pdfParser_dataReady', (pdfData) => {
    console.log('pdfParser_dataReady');
    // fs.writeFileSync("./output.json", JSON.stringify(pdfData));
    fs.writeFileSync(textFile, pdfParser.getRawTextContent(), { flag: 'a' });
  });

  pdfParser.loadPDF(PDFFile);
}

// 指定要读取的目录路径
const directoryPath = dir + '/../data/pdf';

const finalTextFile = dir + '/../data/process/content.txt';
// 定义一个空数组用于存储文件名
const fileNames = [];

// 定义一个函数用于读取目录下的所有文件
function readDirectory(dirPath) {
  // 读取指定目录下的所有文件和子目录
  const files = fs.readdirSync(dirPath);

  // 遍历每个文件或子目录
  for (const file of files) {
    const filePath = path.join(dirPath, file);
    const stats = fs.statSync(filePath);

    // 如果是文件，将文件名存入数组
    if (stats.isFile()) {
      fileNames.push(file);

      const filePath = path.join(dirPath, file);
      convertPDF2Txt(filePath, finalTextFile);
    }
  }
}

// 调用 readDirectory 函数读取指定目录下的文件
readDirectory(directoryPath);
