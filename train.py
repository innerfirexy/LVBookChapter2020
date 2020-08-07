import subprocess
import glob
import os


def run_CWE(bin_dir: str, data_dir: str, data: str,
        cbow: int = 1, size: int = 300, cwe_type: int = 1):
    """
    cbow: 1 for cbow, 0 for skipgram
    cwe_type: 2(CWE+P), 1(CWE), 0(word2vec), 3(CWE+L), 4(CWE+LP), 5(CWE+N)
    """
    groups = glob.glob(os.path.join(data_dir, '*'))
    for grp in groups:
        train_data = os.path.join(grp, data)
        data_name, _ = os.path.splitext(data)
        print(data_name)
        word_vec_file = os.path.join(grp, f'wordvec_cbow{cbow}_size{size}_cwetype{cwe_type}_{data_name}.txt')
        char_vec_file = os.path.join(grp, f'charvec_cbow{cbow}_size{size}_cwetype{cwe_type}_{data_name}.txt')

        print(f'train {grp}')
        cmd = f'{bin_dir} -train {train_data} -output-word {word_vec_file} -output-char {char_vec_file} -cbow {cbow} -size {size} -cwe-type {cwe_type}'
        print(cmd)
        subprocess.run(cmd, shell=True)
        print('done.')


def main():
    CWE_BIN_DIR = '/Users/xy/GitHub/CWE/src/cwe'

    # 100 years per group
    DATA_DIR1 = './data/group_year_span/100years_cutoff1951'
    # DATA = 'data_shuf.txt'
    DATA = 'data_shuf_sample.txt'
    # run_CWE(bin_dir = CWE_BIN_DIR, data_dir = DATA_DIR1, data = DATA, cbow=1, size=300, cwe_type=1)
    run_CWE(bin_dir = CWE_BIN_DIR, data_dir = DATA_DIR1, data = DATA, cbow=0, size=300, cwe_type=1)


if __name__ == "__main__":
    main()