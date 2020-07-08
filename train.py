import subprocess
import glob
import os


def run_CWE(bin_dir: str, data_dir: str, 
        cbow: int = 1, size: int = 300, cwe_type: int = 1):
    """
    cbow: 1 for cbow, 0 for skipgram
    cwe_type: 2(CWE+P), 1(CWE), 0(word2vec), 3(CWE+L), 4(CWE+LP), 5(CWE+N)
    """
    groups = glob.glob(os.path.join(data_dir, '*'))
    for grp in groups:
        data_file = os.path.join(grp, 'data_shuf.txt')
        word_vec_file = os.path.join(grp, f'wordvec_cbow{cbow}_size{size}_cwetype{cwe_type}.txt')
        char_vec_file = os.path.join(grp, f'charvec_cbow{cbow}_size{size}_cwetype{cwe_type}.txt')

        cmd = f'{bin_dir} -train {data_file} -output-word {word_vec_file} -output-char {char_vec_file} \
            -cbow {cbow} -size {size} -cwe-type {cwe_type}'
        subprocess.Popen(cmd, shell=True)
    pass


def main():
    run_CWE(bin_dir = '/Users/xy/GitHub/CWE/src/cwe', 
        data_dir = './data/group_year_span/100years_cutoff1951')


if __name__ == "__main__":
    main()