"""
Created on Thu May  5 13:21:52 2016

@author: salo
"""

from glob import glob
import pandas as pd
import nltk
from .utils import word2num, find_candidates, reduce_candidates, get_res
from pattern.en import parsetree
import re
from os.path import join, splitext, basename


def return_nes(sentences):
    """
    """
    cd_cand, cd_np, candidate_terms = get_res()
    nps = []
    sentences = parsetree(sentences)
    for sentence in sentences:
        for chunk in sentence.chunks:
            match = re.match(cd_np, str(chunk))
            if match is not None and any([term in nltk.word_tokenize(chunk.string) for term in candidate_terms]):
                np = match.group(1)
                nps += [np]
    nps = [(re.match(cd_cand, ne).group(2).strip(), re.match(cd_cand, ne).group(1).strip()) for ne in nps]
    return nps


def find_corpus(folder, clean=True):
    """
    """
    samples = []

    files = glob(join(folder, '*.txt'))
    for f in files:
        name = basename(splitext(f)[0])
        with open(f, 'rb') as fo:
            text = fo.read()

        if clean:
            text = clean_str(text)

        samples.append([name, findall(text)])
    df = pd.DataFrame(columns=['id', 'sample size'],
                      data=samples)
    return df


def findall(text):
    """
    """
    sentences = nltk.sent_tokenize(text)
    sentences = [convert_words_to_numbers(sentence) for sentence in sentences]
    subj_sentences = find_candidates(sentences)
    num_sentences = ' '.join(reduce_candidates(subj_sentences))
    nes = return_nes(num_sentences)
    return nes
