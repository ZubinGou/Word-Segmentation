import os
import sys
import time
from evaluation.segmentor import Segmentor


def seg_test(seg, name, test_set):
    start = time.time()
    fin = open('data/icwb2-data/testing/%s_test.utf8' % test_set,
               'r',
               encoding='utf8')
    fout = open('data/results/%s.%s' % (test_set, name), 'w', encoding='utf8')
    for index, line in enumerate(fin):
        line = line.strip()
        if line == '':
            fout.write('\n')
        else:
            words = getattr(seg, name)(line)
            if type(words[0]) == list:
                words = words[0]
            fout.write(' '.join(words) + '\n')
    fin.close()
    fout.close()
    print("Method={} \ttime(s): {:.3f}".format(name, time.time() - start))


def compare_line(reference, candidate):  # reference 标注
    ref_words = reference.split()
    can_words = candidate.split()

    ref_words_len = len(ref_words)
    can_words_len = len(can_words)

    ref_index = []
    index = 0
    for word in ref_words:
        word_index = [index]
        index += len(word)
        word_index.append(index)
        ref_index.append(word_index)

    can_index = []
    index = 0
    for word in can_words:
        word_index = [index]
        index += len(word)
        word_index.append(index)
        can_index.append(word_index)

    tmp = [val for val in ref_index if val in can_index]
    acc_word_len = len(tmp)

    return ref_words_len, can_words_len, acc_word_len


def test_value(name, test_set):
    fref = open('data/icwb2-data/gold/%s_test_gold.utf8' % test_set,
                'r',
                encoding='utf8')
    fcan = open('data/results/%s.%s' % (test_set, name), 'r', encoding='utf8')
    reference_all = fref.readlines()
    candidate_all = fcan.readlines()
    fref.close()
    fcan.close()

    ref_count = 0
    can_count = 0
    acc_count = 0
    for reference, candidate in zip(reference_all, candidate_all):
        reference = reference.strip()
        candidate = candidate.strip()

        ref_words_len, can_words_len, acc_word_len = compare_line(
            reference, candidate)
        ref_count += ref_words_len
        can_count += can_words_len
        acc_count += acc_word_len

    P = acc_count / can_count * 100
    R = acc_count / ref_count * 100
    F1 = (2 * P * R) / (P + R)

    print('Method={} \tP: {:.2f} \tR: {:.2f} \tF1: {:.2f}'.format(
        name, P, R, F1))


if __name__ == '__main__':

    methods = ['fmm', 'bmm', 'bimm', 'mmseg', 'hmm', 'jieba', 'thulac', 'ltp', 'hanlp']

    for corpus in ['pku', 'msr']:
        print('Corpus: {}'.format(corpus))
        seg = Segmentor(methods, corpus)

        for cur in methods:
            seg_test(seg, cur, corpus)
        for cur in methods:
            test_value(cur, corpus)
