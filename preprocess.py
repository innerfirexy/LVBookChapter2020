import os
import re
import itertools
import pandas as pd
from collections import Counter
from typing import (List)
from tqdm import tqdm
import glob

import jieba


def list_all_files(data_dir: str, file_ext: str = '.txt') -> List[str]:
    all_files: List[str] = []

    for path in os.listdir(data_dir):
        full_path = os.path.join(data_dir, path)
        file_pattern = f'{path}_*' + file_ext
        txt_files = glob.glob(os.path.join(full_path, file_pattern))
        for file in txt_files:
            all_files.append(file)
    # assert all(f.endswith('.txt') for f in all_files)

    return all_files


def list_all_files_old(data_dir: str) -> List[str]:
    all_files: List[str] = []

    for path in os.listdir(data_dir):
        full_path = os.path.join(data_dir, path)
        for file in os.listdir(full_path):
            all_files.append(os.path.join(full_path, file))
    # assert all(f.endswith('.txt') for f in all_files)

    return all_files



def line_to_sentences(input_str: str, separators: List[str] = ['。', '？', '！']) -> List[str]:
    """
    Example:
        input_str: 故尚書兵部員外郎、知制誥、知鄧州軍州事陽夏公之夫人，姓高氏，宣州宣城人也。父諱惠連，官至兵部郎中。母曰廣陵縣君勾氏。
        output: ['故尚書兵部員外郎、知制誥、知鄧州軍州事陽夏公之夫人，姓高氏，宣州宣城人也。', \
            '父諱惠連，官至兵部郎中。', '母曰廣陵縣君勾氏。']
    """
    pattern = '(' + '|'.join(separators) + ')'
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


def convert_to_sentences():
    """
    Segment each line of text with end-of-sentence characters, '。', '！', '？'
    Save to new files, with each sentence as a line.
    """
    data_dir = './data/Wikisource_chn'
    all_files = list_all_files(data_dir)

    for fname in tqdm(all_files, ncols=100):
        with open(fname, 'r') as f:
            line = f.read() # using readline() will result in a problem
            sentences = line_to_sentences(line.strip(), separators=['。', '！', '？']) # 
        
        fname_new = fname + '.sentences'
        with open(fname_new, 'w') as f:
            for sent in sentences:
                sent = sent.replace(' ', '')
                f.write(sent + '\n')


def remove_puncts():
    """
    Remove all punctuations in a sentence
    """
    data_dir = './data/Wikisource_chn'
    all_files = list_all_files(data_dir, file_ext='.sentences')

    # read punctuation vocabulary
    puncts = []
    with open('all_puncts.txt', 'r') as f:
        for line in f:
            puncts.append(line[:-1])
    puncts = set(''.join(puncts))

    for fname in tqdm(all_files, ncols=100):
        cleaned_sentences = []
        with open(fname, 'r') as f:
            for line in f:
                line = line.strip()
                cleaned = ''.join([ch for ch in line if ch not in puncts])
                cleaned_sentences.append(cleaned)

        fname_new = fname + '.nopuncts'
        with open(fname_new, 'w') as f:
            for sent in cleaned_sentences:
                f.write(sent + '\n')


def word_segment_jieba():
    jieba.enable_parallel(4)

    data_dir = './data/Wikisource_chn'
    all_files = list_all_files(data_dir, file_ext='.sentences.nopuncts')

    for fname in tqdm(all_files, ncols=100):
        segment_results = []
        with open(fname, 'r') as f:
            for line in f:
                line = line.strip()
                seg = jieba.cut(line, cut_all=False)
                segment_results.append(seg)
        
        fname_new = fname + '.jieba'
        with open(fname_new, 'w') as f:
            for seg in segment_results:
                f.write(' '.join(seg) + '\n')


def main():
    # convert_to_sentences()
    # remove_puncts()
    word_segment_jieba()


if __name__ == "__main__":
    main()