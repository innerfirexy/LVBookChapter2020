import numpy as np
from tqdm import tqdm
from typing import (Dict, Any)


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