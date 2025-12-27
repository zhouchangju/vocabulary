#!/usr/bin/env python3
"""
打乱单词文件中的单词顺序
使用方式：
python shuffle_words.py inputFile.txt outputFile.txt
"""

import random
import sys


def shuffle_words(input_file: str, output_file: str, seed: int = None) -> int:
    """
    打乱单词文件的顺序

    Args:
        input_file: 输入文件路径
        output_file: 输出文件路径
        seed: 随机种子（可选），用于可重现的打乱结果

    Returns:
        处理的单词数量
    """
    # 读取所有单词
    with open(input_file, 'r', encoding='utf-8') as f:
        words = [line.strip() for line in f if line.strip()]

    print(f"读取了 {len(words)} 个单词")

    # 设置随机种子（如果提供）
    if seed is not None:
        random.seed(seed)
        print(f"使用随机种子: {seed}")

    # 打乱顺序
    random.shuffle(words)
    print("单词顺序已打乱")

    # 写入新文件
    with open(output_file, 'w', encoding='utf-8') as f:
        for word in words:
            f.write(word + '\n')

    print(f"已生成新文件: {output_file}")
    return len(words)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python shuffle_words.py <输入文件> [输出文件] [随机种子]")
        print("示例: python shuffle_words.py TOEFL_GREEN_BOOK.txt TOEFL_GREEN_BOOK_shuffled.txt")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else input_path.replace('.txt', '_shuffled.txt')
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else None

    shuffle_words(input_path, output_path, seed)
