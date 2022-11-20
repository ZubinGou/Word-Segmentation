import os
import sys
import jieba
from ltp import LTP
import thulac
import pyhanlp
import torch

from cws.fmm import FMMSegment
from cws.bmm import BMMSegment
from cws.bimm import BIMMSegment
from cws.mmseg import MMSegment
from cws.hmm import HMMSegment


class Segmentor:

    def __init__(self, methods, corpus='pku'):
        """
        基于词表的方法: FMM / BMM / BiMM / MMSeg
        """
        if 'fmm' in methods:
            self.model_fmm = FMMSegment()
            self.model_bmm = BMMSegment()
            self.model_bimm = BIMMSegment()
            self.model_mmseg = MMSegment()
        """
        基于机器学习的方法: HMM
        """
        # load hmm
        if 'hmm' in methods:
            self.model_hmm = HMMSegment()
            hmm_path = "models/hmm/{}.pickle".format(corpus)
            if os.path.exists(hmm_path):
                self.model_hmm.load_model(hmm_path)
            else:
                print("Training HMM...")
                train_file = 'data/icwb2-data/training/{}_training.utf8'.format(
                    corpus)
                self.model_hmm.train(
                    [line for line in open(train_file, 'r', encoding='utf-8')])
                self.model_hmm.save_model(hmm_path)
        """
        基于神经网络：BiLSTM-CRF
        基于预训练模型：BERT-CRF
        """
        """
        现有分词工具包含 jieba/thulac/LTP/Hanlp
        """
        # load jiba
        if 'jieba' in methods:
            jieba.initialize()

        # load ltp
        if 'ltp' in methods:
            print("Loading LTP")
            self.model_ltp = LTP("LTP/small")  # 默认加载 Small 模型
            if torch.cuda.is_available():  # 将模型移动到 GPU 上
                self.model_ltp.to("cuda")

        # load thulac
        if 'thulac' in methods:
            self.model_thulac = thulac.thulac(seg_only=True)

    def fmm(self, text):
        return [word for word in self.model_fmm.cut(text)]

    def bmm(self, text):
        return [word for word in self.model_bmm.cut(text)]

    def bimm(self, text):
        return [word for word in self.model_bimm.cut(text)]

    def mmseg(self, text):
        return [word for word in self.model_mmseg.cut(text)]

    def hmm(self, text):
        return [word for word in self.model_hmm.cut(text)]

    def bi_lstm_crf(self, text):
        _, sequences = self.model_bi_lstm_crf([text])
        return sequences[0]

    def jieba(self, text):
        # 结巴分词
        return list(jieba.cut(text))

    def thulac(self, text):
        # 清华分词
        return self.model_thulac.cut(text, text=True).split()

    def ltp(self, text):
        # 哈工大LTP
        return self.model_ltp.pipeline([text], tasks=["cws"]).cws[0]

    def hanlp(self, text):
        # HanLP
        res = []
        for term in pyhanlp.HanLP.segment(text):
            res.append(term.word)
        return res


def _test_segment():
    # https://www.zhihu.com/question/19578687/answer/15607602
    sentences = [
        "柳奶奶和牛奶奶泼牛奶吓坏了刘奶奶，大骂再也不买柳奶奶和牛奶奶的牛奶。",
        "工信处女干事每月经过下属科室都要亲口交代24口交换机等技术性器件的安装工作",
        "工信處女幹事每月經過下屬科室都要親口交代24口交換機等技術性器件的安裝工作"
    ]
    methods = ['jieba', 'thulac', 'ltp', 'hanlp']
    segmentor = Segmentor(methods)
    for sent in sentences:
        print("\n" + "-" * 20)
        print("Sentence: {}".format(sent))
        for method in methods:
            words = getattr(segmentor, method)(sent)
            print("{}: {}".format(method, words))


if __name__ == '__main__':
    _test_segment()
