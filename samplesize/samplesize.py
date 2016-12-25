"""
Created on Thu May  5 13:21:52 2016

@author: salo
"""

from glob import glob
import pandas as pd
import nltk
from .utils import word2num, find_candidates, get_res
from pattern.en import parsetree
import re
from os.path import join, splitext, basename


def return_nes(sentences):
    """
    Find noun phrases/named entities within relevant sentences that contain
    both a candidate term and a number.
    """
    cd_cand, cd_np, candidate_terms = get_res()
    nps = []
    
    # The parser keeps n=X together, but separates n = X.
    sentences = re.sub('n = ', 'n=', sentences)
    sentences = parsetree(sentences)
    for sentence in sentences:       
        for i, chunk in enumerate(sentence.chunks):            
            if any([term in nltk.word_tokenize(chunk.string) for term in\
                    candidate_terms]):
                # n = X type
                for j in range(i+1, len(sentence.chunks)):
                    if any([term in nltk.word_tokenize(sentence.chunks[j].string)\
                            for term in candidate_terms]):
                        break
                    
                    match0 = re.match('\s*n=(\d+)', sentence.chunks[j].string)
                    if match0 is not None:
                        n = match0.group(1)
                        chunks = sentence.chunks[i:j]
                        chunks = [n] + [c.string for c in chunks]
                        np = ' '.join(chunks)
                        nps += [np]
                        break
                
                # X subjects type
                match1 = re.match(cd_np, str(chunk))
                if match1 is not None:
                    np = match1.group(1)
                    nps += [np]

    # One final check
    out_nps = []
    for ne in nps:            
        if re.match(cd_cand, ne):
            out_nps.append((re.match(cd_cand, ne).group(2).strip(),
                            re.match(cd_cand, ne).group(1).strip()))

    if len(out_nps) == 0:
        out_nps = None

    return out_nps


def find_corpus(folder, clean=True):
    """
    Find sample sizes for all text files in folder.
    
    Parameters
    ----------
    folder : str
        Folder containing text files from which to extract sample sizes.
    
    clean : bool
        To clean the strings from the text files or not. Default = True.
    
    Returns
    ----------
    df : pandas.DataFrame
        DataFrame where row index is the name of the file and the first
        column's values are the found sample sizes.
    """
    samples = []

    files = glob(join(folder, '*.txt'))
    files = files[100:500]
    for f in files:
        name = basename(splitext(f)[0])
        with open(f, 'rb') as fo:
            text = fo.read()

        if clean:
            text = clean_str(text)

        samples.append([name, findall(text)])
    df = pd.DataFrame(columns=['id', 'samples'],
                      data=samples)
    return df


def findall(text):
    """
    Find sample sizes within a piece of text.
    
    Parameters
    ----------
    text : str
        Text to clean.
    
    Returns
    ----------
    nes : list of tuples or None
        Pairs of sample sizes and groups.
    """
    sentences = nltk.sent_tokenize(text)
    sentences = [word2num(sentence) for sentence in sentences]
    cand_sentences = ' '.join(find_candidates(sentences))
    nes = return_nes(cand_sentences)
    return nes


def clean_str(text):
    """
    Apply some standard text cleaning with regex.
        1. Remove unicode characters.
        2. Combine multiline hyphenated words.
        3. Remove newlines and extra spaces.
    
    Parameters
    ----------
    text : str
        Text to clean.
    
    Returns
    ----------
    text : str
        Cleaned text.
    
    Examples
    ----------
    >>> text = 'I am  a \nbad\r\n\tstr-\ning.'
    >>> print(text)
    I am  a
    bad
        str-
    ing.
    >>> text = clean_str(text)
    >>> print(text)
    I am a bad string.
    """
    # Remove unicode characters.
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)

    # Combine multiline hyphenated words.
    text = re.sub('-[\s]*[\r\n\t]+', '', text, flags=re.MULTILINE)

    # Remove newlines and extra spaces.
    text = re.sub('[\r\n\t]+', ' ', text, flags=re.MULTILINE)
    text = re.sub('[\s]+', ' ', text, flags=re.MULTILINE)
    return text
