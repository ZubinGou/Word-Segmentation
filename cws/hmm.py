#!usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import re
import pickle
from tqdm import tqdm
from cws.base import BaseSegment


class HMMSegment(BaseSegment):
    B_TOKEN = 'B'
    M_TOKEN = 'M'
    E_TOKEN = 'E'
    S_TOKEN = 'S'

    def __init__(self):
        super(HMMSegment, self).__init__()
        self.epsilon = sys.float_info.epsilon
        self.state_list = [
            self.B_TOKEN, self.M_TOKEN, self.E_TOKEN, self.S_TOKEN
        ]
        self.start_p = {}
        self.trans_p = {}
        self.emit_p = {}
        self.state_dict = {}
        self.__init_parameters()

    def __init_parameters(self):
        for state in self.state_list:
            self.start_p[state] = 1 / len(self.state_list)
            # 转移矩阵
            self.trans_p[state] = {
                s: 1 / len(self.state_list)
                for s in self.state_list
            }
            self.emit_p[state] = {}  # 发射矩阵
            self.state_dict[state] = 0

    def __label(self, word):
        out = []
        if len(word) == 1:
            out = [self.S_TOKEN]
        else:
            out += [self.B_TOKEN
                    ] + [self.M_TOKEN] * (len(word) - 2) + [self.E_TOKEN]
        return out

    def train(self, dataset: list):
        if not dataset or len(dataset) == 0:
            print('数据为空')
            return

        line_nb = 0
        for line in tqdm(dataset):
            line = line.strip()
            if not line:
                continue
            line_nb += 1

            char_list = [c for c in line if c != ' ']
            word_list = line.split()
            # 获取 state list
            state_list = []
            for word in word_list:
                state_list.extend(self.__label(word))

            assert len(state_list) == len(char_list)

            # 统计更新转移和发射矩阵
            for index, state in enumerate(state_list):
                self.state_dict[state] += 1
                if index == 0:
                    self.start_p[state] += 1
                else:
                    self.trans_p[state_list[index - 1]][state] += 1
                self.emit_p[state_list[index]][char_list[index]] \
                    = self.emit_p[state_list[index]].get(char_list[index], 0) + 1

        self.start_p = {
            state: (num + self.epsilon) / line_nb
            for state, num in self.start_p.items()
        }
        self.trans_p = {
            pre_state: {
                cur_state:
                (cur_num + self.epsilon) / self.state_dict[pre_state]
                for cur_state, cur_num in value.items()
            }
            for pre_state, value in self.trans_p.items()
        }
        self.emit_p = {
            state: {
                char: (char_num + self.epsilon) / self.state_dict[state]
                for char, char_num in value.items()
            }
            for state, value in self.emit_p.items()
        }
        print('训练完成')

    def load_model(self, model_path: str):
        with open(model_path, 'rb') as f:
            self.start_p = pickle.load(f)
            self.trans_p = pickle.load(f)
            self.emit_p = pickle.load(f)
        print('模型加载完成')

    def save_model(self, model_path: str):
        with open(model_path, 'wb') as f:
            pickle.dump(self.start_p, f)
            pickle.dump(self.trans_p, f)
            pickle.dump(self.emit_p, f)
        print('模型保存 %s' % model_path)

    def __viterbi(self, sentence: str):
        dp = [{}]
        path = {}
        for state in self.state_list:
            dp[0][state] = self.start_p[state] * self.emit_p[state].get(
                sentence[0], self.epsilon)
            path[state] = [state]

        # 遍历句子每个字
        for index in range(1, len(sentence)):
            dp.append({})
            new_path = {}

            # 遍历 state, DP 算法更新，记录路径
            for cur_state in self.state_list:
                emitp = self.emit_p[cur_state].get(sentence[index],
                                                   self.epsilon)
                (prob, pre_state) = max([
                    (dp[index - 1][pre_state] *
                     self.trans_p[pre_state].get(cur_state, self.epsilon) *
                     emitp, pre_state) for pre_state in self.state_list
                    if dp[index - 1][pre_state] > 0
                ])
                dp[index][cur_state] = prob
                new_path[cur_state] = path[pre_state] + [cur_state]
            path = new_path

        # 非单字词
        if self.emit_p[self.M_TOKEN].get(sentence[-1], self.epsilon) > \
                self.emit_p[self.S_TOKEN].get(sentence[-1], self.epsilon):
            # 判别词中还是词尾
            (prob, state) = max([(dp[len(sentence) - 1][state], state)
                                 for state in (self.E_TOKEN, self.M_TOKEN)])
        else: # 单字词转移
            (prob, state) = max([(dp[len(sentence) - 1][state], state)
                                 for state in self.state_list])

        return prob, path[state]

    def __cut(self, sentence: str):
        if sentence is None or len(sentence) == 0:
            return []

        prob, pos_list = self.__viterbi(sentence)
        begin_, next_ = 0, 0

        for i, char in enumerate(sentence):
            pos = pos_list[i]
            if pos == self.B_TOKEN:
                begin_ = i
            elif pos == self.E_TOKEN:
                yield sentence[begin_:i + 1]
                next_ = i + 1
            elif pos == self.S_TOKEN:
                yield char
                next_ = i + 1
        if next_ < len(sentence):
            yield sentence[next_:]

    def cut(self, sentence: str):
        if sentence is None or len(sentence) == 0:
            return []

        re_han = re.compile("([\u4E00-\u9FD5a-zA-Z0-9+#&\._%\-]+)", re.U)
        blocks = re_han.split(sentence)
        for blk in blocks:
            if not blk:
                continue
            if re_han.match(blk):
                for word in self.__cut(blk):
                    yield word
            else:
                yield blk


if __name__ == '__main__':
    text = '南京市长江大桥上的汽车'
    train_file = 'data/icwb2-data/training/pku_training.utf8'
    segment = HMMSegment()
    segment.train([line for line in open(train_file, 'r', encoding='utf-8')])
    print(' '.join(segment.cut(text)))
