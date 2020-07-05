import glob
import os
import re
import itertools
import pickle
import pandas as pd
from collections import Counter
from typing import (List)
from tqdm import tqdm

from preprocess import list_all_files


def get_puncts_single_file(fname: str):
    # Unicode range for Chinese
    MIN = 0x4E00
    MAX = 0x9FFF

    puncts: List[str] = []
    with open(fname, 'r') as f:
        text = f.read()
        for ch in text.rstrip():
            if ord(ch) < MIN or ord(ch) > MAX:
                if ch not in puncts:
                    puncts.append(ch)
    
    return puncts


def get_all_puncts():
    puncts_file = 'wikisource_chn_puncts.txt' 
    if os.path.exists(puncts_file) and os.path.isfile(puncts_file):
        all_puncts: List[str] = []
        with open(puncts_file, 'r') as f:
            for line in f:
                all_puncts.append(line.rstrip())
        return set(all_puncts)
    
    punctuations: List[str] = []
    all_files = list_all_files(data_dir='./data/Wikisource_chn')
    for fn in tqdm(all_files, ncols=100):
        puncts = get_puncts_single_file(fn)
        punctuations.append(puncts)

    all_puncts = set(itertools.chain.from_iterable(punctuations))
    with open(puncts_file, 'w') as f:
        for ch in all_puncts:
            f.write(ch + '\n')

    return all_puncts


def char_count_by_year():
    all_files = list_all_files(data_dir='./data/Wikisource_chn')
    all_puncts = get_all_puncts()
    results = Counter()

    for fname in tqdm(all_files, ncols=100):
        base_name = os.path.basename(fname)
        m = re.match(r'^\d+(?=_)', base_name)
        if m is None:
            print(fname)
            raise FileNotFoundError

        year = m.group()
        count = 0
        with open(fname, 'r') as f:
            text = f.read().strip()
            for ch in text:
                if ch not in all_puncts:
                    count += 1
        results[year] += count
    
    records = list(results.items())
    df = pd.DataFrame.from_records(records)
    df.to_csv('wikisource_chn_cc_year.csv', header=['year', 'charCount'], index=False)


def word_count_by_year():
    all_files = list_all_files(data_dir='./data/Wikisource_chn',\
        file_ext='.nopuncts.jieba') 
    counter = Counter()
    vocab_per_year = {}

    for fname in tqdm(all_files, ncols=100):
        base_name = os.path.basename(fname)
        m = re.match(r'^\d+(?=_)', base_name)
        if m is None:
            print(fname)
            raise FileNotFoundError
        year = m.group()
        
        if year not in vocab_per_year:
            vocab_per_year[year] = Counter()

        with open(fname, 'r') as f:
            tmp_count = 0
            for line in f:
                words = line.strip().split()
                tmp_count += len(words)
                for w in words:
                    vocab_per_year[year][w] += 1
            counter[year] += tmp_count
        
    word_count_records = list(counter.items())
    df = pd.DataFrame.from_records(word_count_records)
    df.to_csv('wikisource_chn_word_count_year.csv', header=['year', 'wordCount'], index=False)

    vocab_records = [(key, len(val)) for key, val in vocab_per_year.items()]
    df2 = pd.DataFrame.from_records(vocab_records)
    df2.to_csv('wikisource_chn_vocab_size_year.csv', header=['year', 'vocabSize'], index=False)
        
    pickle.dump(vocab_per_year, open('chn_vocab_per_year.pkl', 'wb'))


def main():
    # char_count_by_year()

    # all_puncts = get_all_puncts()
    # with open('all_puncts.txt', 'w') as f:
    #     for p in all_puncts:
    #         f.write(f'{p}\n')
    
    word_count_by_year()


if __name__ == "__main__":
    main()