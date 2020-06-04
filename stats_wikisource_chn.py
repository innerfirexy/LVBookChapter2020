import glob
import os
import re
import itertools
import pandas as pd
from collections import Counter
from typing import (List)
from tqdm import tqdm


def list_all_files() -> List[str]:
    all_files: List[str] = []
    data_dir = './data/Wikisource_chn'

    for path in os.listdir(data_dir):
        full_path = os.path.join(data_dir, path)
        for file in os.listdir(full_path):
            all_files.append(os.path.join(full_path, file))
    assert all(f.endswith('.txt') for f in all_files)

    return all_files


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
    all_files = list_all_files()
    for fn in tqdm(all_files, ncols=100):
        puncts = get_puncts_single_file(fn)
        punctuations.append(puncts)

    all_puncts = set(itertools.chain.from_iterable(punctuations))
    with open(puncts_file, 'w') as f:
        for ch in all_puncts:
            f.write(ch + '\n')

    return all_puncts


def char_count_by_year():
    all_files = list_all_files()
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
            text = f.read().rstrip()
            for ch in text:
                if ch not in all_puncts:
                    count += 1
        results[year] += count
    
    records = list(results.items())
    df = pd.DataFrame.from_records(records)
    df.to_csv('wikisource_chn_cc_year.csv', header=['year', 'charCount'], index=False)


def main():
    char_count_by_year()


if __name__ == "__main__":
    main()