# -*- coding: utf-8 -*-
"""
Created on Thu May  5 21:58:48 2016

Number words.

@author: salo
"""
import re
import nltk
from itertools import groupby
from operator import itemgetter
from word2number import w2n


def consec(data):
    """
    Group numbers in list into sublists of consecutive values.
    """
    ranges = []
    for key, group in groupby(enumerate(data), lambda (index, item): index - item):
        group = map(itemgetter(1), group)
        ranges.append(range(group[0], group[-1]+1))

    return ranges


def word2num(sentence):
    """
    Convert number-words in sentence to numbers.
    """
    numbers = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
               'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety',
               'zero', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen',
               'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen',
               'hundred', 'thousand', 'million', 'billion', 'trillion']
    numbers.sort(key=len, reverse=True)

    string = '|'.join(numbers)
    full = '((' + string + ').+(' + string + '))|(' + string + ')'
    find_numwords = re.compile(full, re.IGNORECASE)

    # Remove characters and words that will break w2n.
    sentence2 = re.sub(r'\band\b', '', sentence)
    sentence2 = sentence2.replace('-', ' ').replace(',', '')
    sentence2 = re.sub(r'\s+', ' ', sentence2)
    if any(number in nltk.word_tokenize(sentence2.lower()) for number in numbers):
        found = re.search(find_numwords, sentence2).group()
        words = nltk.word_tokenize(found)
        idx = [i for i in range(len(words)) if words[i].lower() in numbers]
        idx2 = consec(idx)
        numword_groups = [[words[i] for i in group] for group in idx2]
        
        switch = {}
        c = 0
        for group in numword_groups:
            # word_to_num can fail for partial numbers, like 'million' from '3.1 million'
            # if it fails, just skip that number
            try:
                num = str(w2n.word_to_num(' '.join(group)))
                switch[c] = {'group': group,
                             'num': num}
                c += 1
            except:
                pass

        # Replace number words in sentence with numbers.
        for c in switch.keys():
            group = switch[c]['group']
            num = switch[c]['num']
            sentence = (sentence[:sentence.index(group[0])] + num +
                        sentence[sentence.index(group[-1])+len(group[-1]):])
    return sentence


def get_res():
    """
    """
    candidate_terms = ['subjects', 'adults', 'children', 'users', 'patients',
                       'men', 'women', 'controls', 'volunteers']

    cd_np = re.compile("Chunk\('([^0-9]*(\d+)[^0-9]*)/NP", re.MULTILINE|re.DOTALL)
    cd_cand = re.compile(".*(\\b\d+)(.*[{0}]\\b).*".format('|'.join(candidate_terms)), re.DOTALL)
    return cd_cand, cd_np, candidate_terms


def find_candidates(sentences):
    """
    Select sentences in list of sentences with both candidate terms (words
    associated with samples) and numbers.
    """
    _, _, candidate_terms = get_res()
    or_term = '|'.join(candidate_terms)
    search_term = re.compile(r'\b(%s)\b' % or_term, re.IGNORECASE)

    out_sentences = []
    for sentence in sentences:
        if re.search(search_term, sentence) and any(char.isdigit() for char in sentence):
            out_sentences.append(sentence)
    return out_sentences
