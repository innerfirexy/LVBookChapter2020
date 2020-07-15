import numpy as np
from tqdm import tqdm
from typing import (Dict, Any, Tuple, List)


def read_embeddings(emb_file: str, 
    vec_start_idx: int = 2, 
    normalize: bool = False) -> Dict[str, np.ndarray]:
    """
    return: a dict object containing word/character embeddings
    """
    vectors: Dict[str, np.ndarray] = {}
    with open(emb_file, 'r') as f:
        header = f.readline()
        num, size = tuple(map(int, header.split()))
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


def get_all_char_norms(word_vectors: Dict[str, np.ndarray], 
    char_vectors: Dict[str, np.ndarray]) -> List[Tuple[Any]]:
    """
    Args:
        word_vectors is the result from filter_by_length, i.e., all words have same length
    Return:
        A list of records, e.g., [(宰相, char1_norm, char2_norm), ...]
        or, [(光禄勋, char1_norm, char2_norm, char3_norm), ...]
    """
    
    pass


def get_mean_char_norms(word_vectors: Dict[str, np.ndarray], 
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


def get_norm_ratios(word_vectors: Dict[str, np.ndarray], char_vectors: Dict[str, np.ndarray]) -> Dict[str, np.float]:
    mean_char_norms = get_mean_char_norms(word_vectors, char_vectors)

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



    pass


def main():

    pass


if __name__ == "__main__":
    main()