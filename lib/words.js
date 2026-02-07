function normalizeWord(word) {
  if (typeof word !== 'string') {
    return '';
  }
  return word.trim().toLowerCase();
}

function isNumeric(word) {
  if (typeof word !== 'string') {
    return false;
  }
  const normalized = word.trim();
  if (!normalized) {
    return false;
  }
  return /^[-+]?(\d+(\.\d*)?|\.\d+)(e[-+]?\d+)?$/i.test(normalized);
}

function splitContentToWords(content) {
  if (typeof content !== 'string') {
    return [];
  }
  const matches =
    content.match(/[\p{L}\p{N}]+(?:[’'-][\p{L}\p{N}]+)*/gu) || [];
  return matches.map(normalizeWord).filter((word) => word.length > 0);
}

module.exports = {
  normalizeWord,
  isNumeric,
  splitContentToWords,
};
