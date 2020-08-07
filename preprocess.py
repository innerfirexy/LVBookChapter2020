import os
import re
import itertools
import pandas as pd
from collections import Counter
from typing import (List)
from tqdm import tqdm
import subprocess
import platform
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


def merge_rows():
    """
    """
    data_dir = './data/Wikisource_chn'
    all_files = list_all_files(data_dir, file_ext='.sentences.nopuncts.jieba')

    for fname in tqdm(all_files, ncols=100):
        merged: List[str] = []
        with open(fname, 'r') as f:
            lines = [line.strip() for line in f]
            lengths = [len(line.split()) for line in lines]

            min_len = 10
            i = 0
            sub_str = ''
            sub_len = 0
            while i < len(lengths):
                sub_str = ' '.join([sub_str, lines[i]])
                sub_len += lengths[i]
                if sub_len >= min_len:
                    merged.append(sub_str.strip())
                    sub_str = ''
                    sub_len = 0
                i += 1
            if sub_len > 0:
                merged[-1] = ' '.join([merged[-1], sub_str])
            
        # write merged lines to new file
        fname_new = fname + '.merged'
        with open(fname_new, 'w') as f:
            for line in merged:
                f.write(line + '\n')


def group_year_span(span: int = 100, file_type: str = '.jieba'):
    """
    span: number of years as the span
    """
    df_wcount = pd.read_csv('wikisource_chn_word_count_year.csv')

    start_year = df_wcount['year'].min()
    end_year = df_wcount['year'].max()
    boundaries = list(range(start_year, end_year, span))
    # use 1951 as a cut-off
    cut_off = 1951
    boundaries = [year for year in boundaries if abs(year - cut_off) > 50] + [cut_off]

    data_dir = './data/Wikisource_chn'
    all_years = sorted(map(int, os.listdir(data_dir)))

    # create output folders
    output_dir = './data/group_year_span'
    if not os.path.exists(output_dir) or os.path.isfile(output_dir):
        os.mkdir(output_dir)
    
    parent_folder = f'{span}years_cutoff{cut_off}'
    parent_dir = os.path.join(output_dir, parent_folder)
    if not os.path.exists(parent_dir):
        os.mkdir(parent_dir)

    for i in range(len(boundaries)-1):
        group_dir = os.path.join(parent_dir, 'group'+str(i+1))
        if not os.path.exists(group_dir):
            os.mkdir(group_dir)

        # obtain the years in group i from `all_years`
        start = boundaries[i]
        end = boundaries[i+1]
        target_years = [y for y in all_years if y >= start and y < end]
        with open(os.path.join(group_dir, 'years.txt'), 'w') as f:
            for y in target_years:
                f.write(str(y) + '\n')
        
        # obtain the segmented text files in group i
        text_files: List[str] = []
        for year in target_years:
            year_data_dir = os.path.join(data_dir, str(year))
            for file in glob.glob(os.path.join(year_data_dir, f'{year}_*' + file_type)):
                text_files.append(file)
        with open(os.path.join(group_dir, 'text_files.txt'), 'w') as f:
            for file in text_files:
                f.write(file + '\n')
        
        # write data
        print(f'writing data for group {i}')
        with open(os.path.join(group_dir, 'data.txt'), 'w') as fout:
            for file in tqdm(text_files, ncols=100):
                with open(file, 'r') as fin:
                    fout.write(fin.read())
        
        # shuffle data
        in_file = os.path.join(group_dir, 'data.txt')
        out_file = os.path.join(group_dir, 'data_shuf.txt')
        print(f'shuffling {in_file} to {out_file}')
        if platform.platform().startswith('Darwin'):
            cmd = f'cat {in_file} | gshuf > {out_file}'
            subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        elif platform.platform().startswith('Linux'):
            cmd = f'cat {in_file} | shuf > {out_file}'
            subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)


def sample_lines(nsamples = 30000):
    """
    Why:
        When we run `find ./ -name "data_shuf.txt" | xargs wc -l`, here is the result:
            98400 .//group7/data_shuf.txt
            165578 .//group9/data_shuf.txt
            90146 .//group8/data_shuf.txt
            80422 .//group1/data_shuf.txt
            76030 .//group6/data_shuf.txt
            33127 .//group3/data_shuf.txt
            54528 .//group4/data_shuf.txt
            44276 .//group5/data_shuf.txt
            58338 .//group2/data_shuf.txt
            700845 total
        This unbalanced data distribution could be the cause of the observed word/char norms patterns

    Solution:
        Sample 30000 lines from each data_shuf.txt, and use them to train.
    """
    data_dir = './data/group_year_span'
    parent_folder = '100years_cutoff1951'
    parent_dir = os.path.join(data_dir, parent_folder)

    for i in range(1,10):
        child_dir = os.path.join(parent_dir, f'group{i}')
        in_file = os.path.join(child_dir, 'data_shuf.txt')
        out_file = os.path.join(child_dir, 'data_shuf_sample.txt')
        print(f'sampling {in_file} to {out_file}')

        if platform.platform().startswith('Darwin'):
            cmd = f'cat {in_file} | gshuf | head -n {nsamples} > {out_file}'
            subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        elif platform.platform().startswith('Linux'):
            cmd = f'cat {in_file} | shuf | head -n {nsamples} > {out_file}'
            subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)


def main():
    # convert_to_sentences()
    # remove_puncts()
    # word_segment_jieba()
    # merge_rows()

    # group_year_span(span=100)
    # group_year_span(span=100, file_type='.jieba.merged')
    sample_lines(nsamples=30000)



if __name__ == "__main__":
    main()