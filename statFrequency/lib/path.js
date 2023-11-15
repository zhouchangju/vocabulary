const path = require('path');

function getBasePath(filePath) {
  let extName = path.extname(filePath);
  return filePath.slice(0, -extName.length);
}

module.exports = {
  getBasePath,
};
