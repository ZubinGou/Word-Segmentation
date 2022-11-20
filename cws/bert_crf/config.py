import os
import torch

bert_model = "bert-base-chinese"

# pku
# data_dir = os.getcwd() + '/../../data/icwb2-data/pku_processed/'
# exp_dir = os.getcwd() + '/../../models/bert_crf-pku_bs32/'

# msr
data_dir = os.getcwd() + '/../../data/icwb2-data/msr_processed/'
exp_dir = os.getcwd() + '/../../models/bert_crf-msr_bs32/'

# data
train_dir = data_dir + 'training.npz'
test_dir = data_dir + 'test.npz'
files = ['training', 'test']
vocab_path = data_dir + 'vocab.npz'

# exp
os.makedirs(exp_dir, exist_ok=True)
model_dir = exp_dir
log_dir = exp_dir + 'train.log'
case_dir = exp_dir + 'bad_case.txt'
output_dir = data_dir + 'output.txt'
res_dir = data_dir + 'res_bert_crf.txt'
test_ans = data_dir + 'test.txt'

max_vocab_size = 1000000
max_len = 500
sep_word = '@'  # 拆分句子的文本分隔符
sep_label = 'S'  # 拆分句子的标签分隔符

# 训练集、验证集划分比例
dev_split_size = 0.1

# 是否加载训练好的Seg模型
load_before = False

# 是否对整个BERT进行fine tuning
full_fine_tuning = True

# hyper-parameter
learning_rate = 6e-5
weight_decay = 0.01
clip_grad = 5

batch_size = 32
epoch_num = 20
min_epoch_num = 5
patience = 0.0002
patience_num = 5

gpu = '0'

local_rank = 0
device = torch.device("cuda", local_rank)

# if gpu != '':
#     torch.distributed.init_process_group(backend='nccl')
#     local_rank = torch.distributed.get_rank()
#     torch.cuda.set_device(local_rank)
# else:
#     device = torch.device("cpu")

# B：分词头部 M：分词词中 E：分词词尾 S：独立成词
label2id = {'B': 0, 'M': 1, 'E': 2, 'S': 3}

id2label = {_id: _label for _label, _id in list(label2id.items())}
