set -ex

export CUDA_VISIBLE_DEVICES=0


cd cws/bert_crf
python run.py
