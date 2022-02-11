#!/usr/bin/env python3
"""
统计四字成语的字频及含高频字最多的成语。
动机来自于：汉兜 https://handle.antfu.me/
成语词典取自：https://raw.githubusercontent.com/beifeng600/nlp_storeroom/master/dict/zh/%E6%B1%89%E8%AF%AD%E6%88%90%E8%AF%AD%E8%AF%8D%E5%85%B8_%E8%AF%8D%E8%A1%A8_23889%E6%9D%A1.txt
"""
import os

TOP_CHAR_COUNT = 20
TOP_CHENGYU_COUNT = 10

def stat(input_path: str, output_path: str) -> None:
    if input_path is None or len(input_path) <= 0:
        raise ValueError(f'Input path "{input_path}" not valid!')

    char_count = {}
    chengyu_count = {}
    with open(input_path, 'r', encoding='utf8') as f:
        for line in f.readlines():
            line = line.rstrip(os.linesep)
            if len(line) != 4:
                continue

            for char in line:
                if char not in char_count:
                    char_count[char] = 0
                char_count[char] += 1
        
        f.seek(0)

        for line in f.readlines():
            line = line.rstrip(os.linesep)
            if line not in chengyu_count:
                chengyu_count[line] = 0
                
            for char in line:
                chengyu_count[line] += char_count[char]

    top100_chars = sorted(char_count.keys(), key=lambda k: char_count[k], reverse=True)[:TOP_CHAR_COUNT]
    top10_chengyu = sorted(filter(lambda c: len(set(c)) == 4, chengyu_count.keys()), key=lambda k: chengyu_count[k], reverse=True)[:TOP_CHENGYU_COUNT]
    with open(output_path, 'w', encoding='utf8') as out:
        out.write(f'四字成语中的高频{TOP_CHAR_COUNT}字：\n')
        out.write('汉字  次数\n')
        
        for char in top100_chars:
            out.write(f'{char}  {char_count[char]}\n')
        
        out.write(f'{TOP_CHENGYU_COUNT}个含高频汉字最多且四字不重复的成语：\n')
        
        for chengyu in top10_chengyu:
            out.write(f'{chengyu}\n')

if __name__ == '__main__':
    input_path = 'D:\\chengyu_dict_4.txt'
    stat(input_path, 'chengyu_dict_4_stat.txt')
