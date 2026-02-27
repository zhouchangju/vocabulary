import json
import os
import requests
import re
from concurrent.futures import ThreadPoolExecutor

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 简单的翻译函数
def get_definition(word):
    try:
        url = f"https://dict.youdao.com/suggest?q={word}&num=1&doctype=json"
        resp = requests.get(url, timeout=3)
        data = resp.json()
        if 'data' in data and 'entries' in data['data'] and len(data['data']['entries']) > 0:
            return data['data']['entries'][0]['explain']
    except:
        pass
    return "暂无释义"

def generate_html(words_with_defs):
    html_template = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>单词快速标注工具 (KMF 专版)</title>
    <style>
        body { font-family: system-ui, -apple-system, sans-serif; margin: 0; padding-top: 70px; background: #f0f2f5; }
        .header { position: fixed; top: 0; width: 100%; background: #fff; border-bottom: 1px solid #ddd; padding: 10px 20px; display: flex; gap: 20px; align-items: center; z-index: 100; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .stats { font-weight: bold; color: #666; font-size: 14px; }
        .stats span { color: #1890ff; margin-right: 15px; }
        button.export-btn { padding: 8px 20px; background: #ff4d4f; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; }
        button.export-btn:hover { background: #cf1322; }
        
        .list-container { max-width: 1000px; margin: 20px auto; background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding-bottom: 50px; }
        .word-row { display: flex; align-items: center; padding: 12px 20px; border-bottom: 1px solid #f0f0f0; transition: all 0.2s; }
        .word-row:hover { background: #fafafa; }
        .word-row.status-easy { background: #f6ffed; opacity: 0.4; filter: grayscale(1); }
        .word-row.status-hard { background: #fff1f0; border-left: 4px solid #ff4d4f; }
        
        .word-text { width: 220px; font-size: 19px; font-weight: 600; color: #2c3e50; font-family: "Georgia", serif; }
        .actions { width: 180px; display: flex; gap: 10px; }
        .btn { padding: 6px 14px; border-radius: 4px; border: 1px solid #ddd; cursor: pointer; font-size: 14px; transition: all 0.2s; }
        .btn-easy { background: #fff; border-color: #b7eb8f; color: #389e0d; }
        .btn-easy:hover { background: #f6ffed; }
        .word-row.status-easy .btn-easy { background: #389e0d; color: #fff; }
        
        .btn-hard { background: #fff; border-color: #ffa39e; color: #cf1322; }
        .btn-hard:hover { background: #fff1f0; }
        .word-row.status-hard .btn-hard { background: #cf1322; color: #fff; }
        
        .definition { flex: 1; color: #5c5c5c; font-size: 15px; margin-left: 20px; line-height: 1.4; }
        .filter-options { margin-left: auto; display: flex; gap: 15px; align-items: center; font-size: 14px; color: #666; }
    </style>
</head>
<body>
    <div class="header">
        <div class="stats">
            全部: <span id="total-count">0</span>
            已标注认识: <span id="easy-count">0</span>
            <strong style="color:#cf1322">待导出(生词): <span id="to-export-count">0</span></strong>
        </div>
        <div class="filter-options">
            <label style="cursor:pointer"><input type="checkbox" id="hide-easy" onchange="renderList()"> 隐藏已认识单词</label>
        </div>
        <button class="export-btn" onclick="exportHardWords()">导出生词本 (剩余所有词)</button>
    </div>

    <div class="list-container" id="word-list">
        <!-- 单词行加载中... -->
    </div>

    <script>
        const allWords = """ + json.dumps(words_with_defs, ensure_ascii=False) + """;
        // 从 localStorage 加载标注状态
        let wordStatus = JSON.parse(localStorage.getItem('vocab_status_kmf_v2') || '{}');

        function updateStats() {
            let easyCount = 0;
            Object.values(wordStatus).forEach(s => {
                if (s === 'easy') easyCount++;
            });
            const total = allWords.length;
            document.getElementById('total-count').innerText = total;
            document.getElementById('easy-count').innerText = easyCount;
            // 待导出 = 总数 - 已认识
            document.getElementById('to-export-count').innerText = total - easyCount;
        }

        function setStatus(word, status) {
            if (wordStatus[word] === status) {
                delete wordStatus[word]; 
            } else {
                wordStatus[word] = status;
            }
            localStorage.setItem('vocab_status_kmf_v2', JSON.stringify(wordStatus));
            updateStats();
            renderList();
        }

        function renderList() {
            const container = document.getElementById('word-list');
            const hideEasy = document.getElementById('hide-easy').checked;
            container.innerHTML = '';

            allWords.forEach(item => {
                const status = wordStatus[item.word];
                if (hideEasy && status === 'easy') return;

                const row = document.createElement('div');
                row.className = 'word-row' + (status ? ' status-' + status : '');
                row.innerHTML = `
                    <div class="word-text">${item.word}</div>
                    <div class="actions">
                        <button class="btn btn-easy" onclick="setStatus('${item.word}', 'easy')">认识</button>
                        <button class="btn btn-hard" onclick="setStatus('${item.word}', 'hard')">生词</button>
                    </div>
                    <div class="definition">${item.def}</div>
                `;
                container.appendChild(row);
            });
        }

        function exportHardWords() {
            const wordsToExport = allWords
                .filter(item => wordStatus[item.word] !== 'easy')
                .map(item => item.word);
            
            if (wordsToExport.length === 0) {
                alert('所有单词都已标注为认识，无需导出！');
                return;
            }

            if (!confirm("确定导出剩余的 " + wordsToExport.length + " 个单词吗？")) return;

            const content = wordsToExport.join('
');
            const blob = new Blob([content], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'KMF_REMAINING_WORDS.txt';
            a.click();
        }

        updateStats();
        renderList();
    </script>
</body>
</html>
    """
    return html_template

def main():
    input_file = os.path.join(BASE_DIR, "data/vocabulary/KMF_EXCLUSIVE_WORDS.txt")
    output_html = os.path.join(BASE_DIR, "vocab_marker.html")
    
    if not os.path.exists(input_file):
        print("Error: {} not found.".format(input_file))
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        words = [line.strip() for line in f if line.strip()]

    print("正在获取 {} 个单词的释义...".format(len(words)))
    
    words_with_defs = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        defs = list(executor.map(get_definition, words))
    
    for word, definition in zip(words, defs):
        words_with_defs.append({"word": word, "def": definition})

    print("生成 HTML...")
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(generate_html(words_with_defs))

    print("完成！请在浏览器中打开: " + os.path.abspath(output_html))

if __name__ == "__main__":
    main()
