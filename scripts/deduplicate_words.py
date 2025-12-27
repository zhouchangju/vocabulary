#!/usr/bin/env python3
"""
单词文件去重
使用方式：
python deduplicate_words.py inputFile.txt outputFile.txt
"""

import sys


def deduplicate_words(input_file: str, output_file: str, keep_order: bool = True) -> int:
    """
    去除单词文件中的重复单词

    Args:
        input_file: 输入文件路径
        output_file: 输出文件路径
        keep_order: 是否保持原有顺序（默认True）

    Returns:
        去重后的单词数量，重复单词数量
    """
    # 读取所有单词
    with open(input_file, 'r', encoding='utf-8') as f:
        words = [line.strip() for line in f if line.strip()]

    original_count = len(words)
    print(f"读取了 {original_count} 个单词")

    # 去重
    if keep_order:
        # 保持顺序的去重方式
        seen = set()
        unique_words = []
        duplicates = []

        for word in words:
            if word not in seen:
                seen.add(word)
                unique_words.append(word)
            else:
                duplicates.append(word)
    else:
        # 不保持顺序，使用集合去重
        unique_words = list(set(words))
        duplicates = []
        seen = set(unique_words)

    unique_count = len(unique_words)
    duplicate_count = original_count - unique_count

    print(f"去重后: {unique_count} 个单词")
    print(f"重复单词: {duplicate_count} 个")

    if duplicates and len(duplicates) <= 20:
        print(f"重复的单词: {', '.join(duplicates)}")
    elif duplicates:
        print(f"部分重复单词: {', '.join(duplicates[:20])}...")

    # 写入新文件
    with open(output_file, 'w', encoding='utf-8') as f:
        for word in unique_words:
            f.write(word + '\n')

    print(f"已生成新文件: {output_file}")
    return unique_count, duplicate_count


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python deduplicate_words.py <输入文件> [输出文件]")
        print("示例: python deduplicate_words.py words.txt words_unique.txt")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else input_path.replace('.txt', '_unique.txt')

    deduplicate_words(input_path, output_path)
