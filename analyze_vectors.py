import os
import glob
import numpy as np
import pandas as pd
from tqdm import tqdm
from typing import (Dict, Any, Tuple, List)


def read_embeddings(emb_file: str, 
    vec_start_idx: int = 2, 
    normalize: bool = False,
    skip_eos: bool = True) -> Dict[str, np.ndarray]:
    """
    return: a dict object containing word/character embeddings
    """
    vectors: Dict[str, np.ndarray] = {}
    with open(emb_file, 'r') as f:
        header = f.readline()
        num, size = tuple(map(int, header.split()))
        if skip_eos: 
            f.readline() # skip line 2: </s>
        for line in tqdm(f, ncols=100, total=num):
            items = line.rstrip().split()
            token = items[0]
            try:
                vec = np.asarray(list(map(float, items[vec_start_idx:])))
            except ValueError as e:
                print('word: {}'.format(token))
                print('row #: {}'.format(len(vectors)))
                raise
            if normalize:
                norm = np.linalg.norm(vec)
                if norm > 0.0:
                    vec = vec / norm # normalize
            vec = vec.reshape(1,-1)
            vectors[token] = vec
    return vectors


def filter_by_length(word_vectors: Dict[str, np.ndarray], len_to_keep: int) \
    -> Dict[str, np.ndarray]:
    filtered = {key: val for key, val in word_vectors.items() if len(key) == len_to_keep}
    return filtered


def compute_word_norms(word_vectors: Dict[str, np.ndarray]) -> List[Tuple]:
    result: List[Tuple] = []

    for word in word_vectors.keys():
        item = (word, np.linalg.norm(word_vectors[word]))
        result.append(item)
    
    return result


def compute_all_chars_norms(word_vectors: Dict[str, np.ndarray], 
    char_vectors: Dict[str, np.ndarray]) -> List[Tuple]:
    """
    Args:
        word_vectors is the result from filter_by_length, i.e., all words have same length
    Return:
        A list of records, e.g., [(宰相, char1_norm, char2_norm), ...]
        or, [(光禄勋, char1_norm, char2_norm, char3_norm), ...]
    """
    result: List[Tuple] = []

    for word in word_vectors.keys():
        item = [word]
        for ch in word:
            item.append(np.linalg.norm(char_vectors[ch]))
        result.append(tuple(item))
    
    return result


def compute_mean_char_norms(word_vectors: Dict[str, np.ndarray], 
    char_vectors: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
    """
    Return:
        {word -> mean_char_norm}
    """
    mean_char_norms: Dict[str, np.ndarray] = {}
    for word in word_vectors.keys():
        ch_norms: List[Any] = []
        for ch in word:
            if ch in char_vectors:
                ch_norms.append(np.linalg.norm(char_vectors[ch]))
        if len(ch_norms) == 0:
            mean_char_norms[word] = None
        else:
            mean = np.mean(ch_norms)
            mean_char_norms[word] = mean
    
    return mean_char_norms


def compute_norm_ratios(word_vectors: Dict[str, np.ndarray], char_vectors: Dict[str, np.ndarray]) -> Dict[str, np.float]:
    mean_char_norms = compute_mean_char_norms(word_vectors, char_vectors)

    norm_ratios: Dict[str, np.ndarray] = {}
    for word, vec in word_vectors.items():
        mean_word = np.mean(vec)
        norm_ratios[word] = mean_word / mean_char_norms[word]

    return norm_ratios


def words_by_length(vectors: Dict[str, np.ndarray]) -> \
    Tuple[Dict[str, np.ndarray], Dict[str, np.ndarray], Dict[str, np.ndarray]]:
    wv_2char: Dict[str, np.ndarray] = {}
    wv_3char: Dict[str, np.ndarray] = {}
    wv_4char: Dict[str, np.ndarray] = {}

    for w, v in vectors.items():
        if len(w) == 2:
            wv_2char[w] = v
        elif len(w) == 3:
            wv_3char[w] = v
        elif len(w) == 4:
            wv_4char[w] = v
    
    return wv_2char, wv_3char, wv_4char


def experiment1_chn():
    results_dir = './data/group_year_span/100years_cutoff1951'

    ## cbow = 1, cwe_type = 1 (CWE)
    word_emb_file = 'wordvec_cbow1_size300_cwetype1.txt'
    char_emb_file = 'charvec_cbow1_size300_cwetype1.txt'

    for group_folder in glob.glob(os.path.join(results_dir, 'group*')):
        print(f'reading embeddings for {group_folder}')
        word_full_path = os.path.join(group_folder, word_emb_file)
        char_full_path = os.path.join(group_folder, char_emb_file)
        word_vectors = read_embeddings(emb_file = word_full_path)
        char_vectors = read_embeddings(emb_file = char_full_path, skip_eos=False) # character embedding file does not contain '</s>'

        word_base_name = os.path.splitext(word_full_path)[0]
        char_base_name = os.path.splitext(char_full_path)[0]
        
        # Compute word norms
        print(f'computing word norms for {group_folder}')
        res_word = compute_word_norms(word_vectors = word_vectors)
        res_word_df = pd.DataFrame(res_word)
        res_word_df.to_csv(word_base_name + '_wordnorms.csv', header=['word', 'norm'], index=False)

        # Compute char norms for word_len = 1, 2, 3, 4
        for i in [1,2,3,4]:
            print(f'computing character norms for {group_folder}, len = {i}')
            word_vectors_sub = filter_by_length(word_vectors, len_to_keep=i)
            res_char = compute_all_chars_norms(word_vectors_sub, char_vectors)
            res_char_df = pd.DataFrame(res_char)
            res_char_df.to_csv(char_base_name + f'charnorms_len{i}.csv', index=False)


def main():
    experiment1_chn()


if __name__ == "__main__":
    main()