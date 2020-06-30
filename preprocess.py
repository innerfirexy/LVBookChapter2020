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


def line_to_sentences(input_str: str) -> List[str]:
    """
    Example:
        input: 故尚書兵部員外郎、知制誥、知鄧州軍州事陽夏公之夫人，姓高氏，宣州宣城人也。
        output: 故尚書兵部員外郎知制誥知鄧州軍州事陽夏公之夫人姓高氏宣州宣城人也
    """
    
    pass


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