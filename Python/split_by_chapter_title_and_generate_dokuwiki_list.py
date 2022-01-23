#!/usr/bin/env python3
import re
import os
from typing import List
import urllib.parse

"""
author: weijie ou
This script is to generate text files and the list to the pages in dokuwiki
from a large consolidated book. The script will split the chapters by the chapter
title format, which you can customize in CHAPTER_REGEX.

Note that dokuwiki accepts url safe encoding filenames by default.
"""

CHARS_TO_CLEAN = ['（', '）', '(', ')', '‘', '’', '“', '”']
# \s includes unicode whitespaces
# ([\s\-\d\/]*)[\s]*
CHAPTER_REGEX = r'^[\s]*第(.*)章[\s]*([^\s\d]+)[\s]?(.*)$'
chapter_search_re = re.compile(CHAPTER_REGEX)

def print_dokuwiki_list(names: List[str], category_name: str) -> None:
    for name in names:
        print(f'  - [{category_name}:{name}|]]')

def save_to_file(chapter: str, chapter_file_name: str, output_folder: str) -> None:
    # New chatper, save last chapter then start over.
    if len(chapter) > 0 and len(chapter_file_name) > 0:
        output_path = os.path.join(output_folder, chapter_file_name)
        with open(output_path, 'w', encoding='utf8') as w:
            w.writelines(chapter)

def split_chapters(input_path: str, category_name: str, output_folder: str = 'output') -> None:
    if input_path is None or len(input_path) <= 0:
        raise ValueError(f'Input path "{input_path}" not valid!')

    with open(input_path, 'r', encoding='utf8') as f:
        chapter = []
        chapter_count = ''
        chapter_name = ''
        chapter_title = ''
        chapter_file_name = ''
        all_chapter_names = []

        if not os.path.exists('output_folder'):
            os.mkdir(output_folder)
        
        for line in f.readlines():
            match = chapter_search_re.match(line)
            if match:
                if chapter_count == match.group(1):
                    continue
                if match.group(2) == '完':
                    continue

                save_to_file(chapter, chapter_file_name, output_folder)

                # print(match.group(0), {match.group(1)}, {match.group(2)}, {match.group(3)})
                chapter_count = match.group(1)
                chapter_name = match.group(2)
                for char in CHARS_TO_CLEAN:
                    chapter_name = chapter_name.replace(char, '_')
                chapter_name = chapter_name.rstrip('_').lstrip('_')
                chapter_name = chapter_name.replace('__', '_')
                chapter_name = f'第{chapter_count}章_{chapter_name}'
                all_chapter_names.append(chapter_name)
                chapter_file_name = urllib.parse.quote(chapter_name) + '.txt'
                chapter_title = f'===== 第{chapter_count}章 {match.group(2)} ====='
                chapter = [chapter_title, os.linesep, match.group(3), os.linesep]
            else:
                chapter.append(line.replace(' ', '　'))
    
    save_to_file(chapter, chapter_file_name, output_folder)
    print(len(all_chapter_names))
    print_dokuwiki_list(all_chapter_names, category_name)
    
if __name__ == '__main__':
    input_path = 'D:\\source.txt'
    category_name = '你的书'
    split_chapters(input_path, urllib.parse.quote(category_name), category_name)
