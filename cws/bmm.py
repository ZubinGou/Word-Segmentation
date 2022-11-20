#!usr/bin/env python
#-*- coding:utf-8 -*-

from cws.base import BaseSegment


class BMMSegment(BaseSegment):

    def __init__(self):
        super(BMMSegment, self).__init__()
        self.load_dict()

    def cut(self, sentence: str):
        if sentence is None or len(sentence) == 0:
            return []

        result = []
        index = len(sentence)
        window_size = min(index, self.trie.max_word_len)
        # 后向遍历
        while index > 0:
            word = ''
            # 遍历最大词组
            for size in range(index - window_size, index):
                word = sentence[size:index]
                if self.trie.search(word):
                    index = size + 1
                    break
            index = index - 1
            result.append(word)
        result.reverse()
        for word in result:
            yield word


if __name__ == '__main__':
    text = '南京市长江大桥上的汽车'
    segment = BMMSegment()
    print(' '.join(segment.cut(text)))
