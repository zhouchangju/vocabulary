#!/usr/bin/env python3
"""清理 TOEFL_2000_AND_GREEN_BOOK_UNIQUE.txt 中的指定单词"""

# 要删除的单词列表
WORDS_TO_REMOVE = {
    'ranges',
    'brutelike',
    'pollution-free',
    'virtues',
    'primates',
    'populated',
    'spacelab',
    'Gogh',
    'studies',
    'directors',
    'alternating',
    'hemispheres',
    'irrigated',
    'tabulating',
    'facilities',
    'bombs',
    'products',
    'hi-tsch',
    'rays',
    'Leonardo',
    'lost-and-found',
    'particles',
    'disfection',
    'remote-sensing',
    'milder',
    'levophobia',
    'saline-alkali',
    'implements',
    'Sigmund',
    'faqade',
    'Pablo',
    'latitudes',
    'Delano',
    'seasame',
    'da',
    "doctor's",
    'commodities',
    'bioanthropology',
    'mediterranean',
    'telescop',
    'Representatives',
    "master's",
    'siltation',
}

def clean_file(input_file: str, output_file: str = None):
    """
    清理文件中的指定单词

    Args:
        input_file: 输入文件路径
        output_file: 输出文件路径，如果为None则覆盖原文件
    """
    # 读取文件
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 过滤单词
    filtered_lines = []
    removed_count = 0

    for line in lines:
        word = line.strip()
        # 如果单词不在删除列表中，保留该行
        if word and word not in WORDS_TO_REMOVE:
            filtered_lines.append(line)
        elif word in WORDS_TO_REMOVE:
            removed_count += 1

    # 写入文件
    if output_file is None:
        output_file = input_file

    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(filtered_lines)

    print(f'处理完成！')
    print(f'原始行数: {len(lines)}')
    print(f'删除单词数: {removed_count}')
    print(f'剩余行数: {len(filtered_lines)}')
    print(f'输出文件: {output_file}')

if __name__ == '__main__':
    import os

    # 文件路径
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(base_dir, 'data/vocabulary/TOEFL_2000_AND_GREEN_BOOK_UNIQUE.txt')

    # 执行清理
    clean_file(input_file)
