import numpy as np
from tqdm import tqdm
from typing import (Dict, Any, Tuple, List)


def emb2dict(emb_file: str, vec_start_idx: int = 2, normalize: bool = False) -> Dict[str, np.ndarray]:
    """
    return: a dict object containing word embeddings
    This function is slower than data_producer.emb2dict
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


def get_mean_char_norms(word_vectors: Dict[str, np.ndarray], char_vectors: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
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
    # TODO:
    
    pass


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