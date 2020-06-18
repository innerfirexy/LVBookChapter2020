import os
import re
import itertools
import pandas as pd
from collections import Counter
from typing import (List)
from tqdm import tqdm


def list_all_files(data_dir: str) -> List[str]:
    all_files: List[str] = []
    # data_dir = './data/Wikisource_chn'

    for path in os.listdir(data_dir):
        full_path = os.path.join(data_dir, path)
        for file in os.listdir(full_path):
            all_files.append(os.path.join(full_path, file))
    assert all(f.endswith('.txt') for f in all_files)

    return all_files


