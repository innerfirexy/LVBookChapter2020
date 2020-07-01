import os
import re
import itertools
import pandas as pd
from collections import Counter
from typing import (List)
from tqdm import tqdm

import jieba


def list_all_files(data_dir: str) -> List[str]:
    all_files: List[str] = []

    for path in os.listdir(data_dir):
        full_path = os.path.join(data_dir, path)
        for file in os.listdir(full_path):
            all_files.append(os.path.join(full_path, file))
    assert all(f.endswith('.txt') for f in all_files)

    return all_files


def line_to_sentences(input_str: str, separators: List[str] = ['', '', '']) -> List[str]:
    """
    Example:
        input_str: 故尚書兵部員外郎、知制誥、知鄧州軍州事陽夏公之夫人，姓高氏，宣州宣城人也。父諱惠連，官至兵部郎中。母曰廣陵縣君勾氏。
        output: ['故尚書兵部員外郎、知制誥、知鄧州軍州事陽夏公之夫人，姓高氏，宣州宣城人也。', \
            '父諱惠連，官至兵部郎中。', '母曰廣陵縣君勾氏。']
    """
    pattern = f'({"|".join(separators)})'
    segments = re.split(pattern, input_str)

    # segments looks like: ['姓高氏，宣州宣城人也', '。', '父諱惠連，官至兵部郎中', '。', '母曰廣陵縣君勾氏', '。', '']
    if len(segments) > 1:
        sentences: List[str] = []
    else:
        sentences = segments

    i = 1
    while i < len(segments):
        if segments[i] in separators:
            sent = segments[i-1] + segments[i]
            sentences.append(sent)
            i += 2

    return sentences


def remove_puncts(input_sentence: str, puncts: List[str]) -> str:
    cleaned = ''.join([ch for ch in input_sentence if ch not in puncts])
    return cleaned


def convert_to_sentences():
    """
    Segment each line of text with end-of-sentence characters, '。', '！', '？'
    Save to new files, with each sentence as a line.
    """
    data_dir = './data/Wikisource_chn'
    all_files = list_all_files(data_dir)

    for fname in tqdm(all_files):
        sentences = []
        with open(fname, 'r') as f:
            for line in f.readline():
                sents = line_to_sentences(line.rstrip())
                sentences.append(sents)
        
        sentences = itertools.chain.from_iterable(sentences)
        fname_new = None
        with open(fname_new, 'w') as f:
            pass


def seg_jieba():
    jieba.enable_parallel(4)

    data_dir = ''
    all_files = list_all_files(data_dir)


    pass