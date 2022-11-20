set -ex

export CUDA_VISIBLE_DEVICES=0


cd cws/bilstm_crf
python run.py