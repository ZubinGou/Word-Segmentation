# Word-Segmentation
Chinese Word Segmentation with FMM, BMM, BiMM, MMSeg, HMM, BiLSTM-CRF and BERT-CRF.


## Corpus

[SIGHAN05](http://sighan.cs.uchicago.edu/bakeoff2005/): MSR & PKU


## Methods
- Rule based:
    - Forward Maximum Matching Method (FMM)
    - Backward Maximum Matching Method (BMM)
    - Bi-directction Matching Method (BiMM)
    - Maximum Matching Segment (MMSeg)
- ML based:
    - Hidden Markov Model (HMM)
- DL based:
    - BiLSTM-CRF
    - BERT-CRF
- Tools:
    - jieba
    - HanLP
    - thulac
    - LTP


## Results

|        Method         | PKU P        | PKU R        | PKU F1       | PKU Time(s)  | MSR P        | MSR R        | MSR F1       | MSR Time(s)  |
| :-------------------: | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ |
|          FMM          | 80.17        | 78.14        | 79.14        | 0.767        | 79.82        | 80.75        | 80.28        | 0.831        |
|          BMM          | 80.46        | 78.44        | 79.44        | <u>0.764</u> | 79.86        | 80.79        | 80.32        | <u>0.794</u> |
|         Bi-MM         | 80.59        | 78.49        | 79.53        | 1.537        | 80.08        | 80.94        | 80.51        | 1.626        |
|         MMSeg         | 80.57        | 78.47        | 79.51        | 23.108       | 80.01        | 80.87        | 80.44        | 10.818       |
|          HMM          | 79.22        | 77.22        | 78.21        | 1.258        | 75.69        | 77.79        | 76.73        | 1.308        |
|      BiLSTM-CRF*      | 92.92        | 92.24        | 92.58        | 11.651       | <u>96.74</u> | <u>96.47</u> | <u>96.61</u> | 10.630       |
| BERT-CRF $^{\dagger*}$| **97.10**    | **96.10**    | **96.60**    | 23.334       | **98.33**    | **98.10**    | **98.21**    | 20.495       |
|         jieba         | 85.26        | 78.66        | 81.83        | **0.490**    | 81.51        | 80.92        | 81.22        | **0.541**    |
|         HanLP         | 86.82        | 81.20        | 83.92        | 1.747        | 82.72        | 80.81        | 81.75        | 1.635        |
|        thulac         | 92.24        | 92.33        | 92.28        | 3.533        | 83.28        | 87.75        | 85.45        | 3.853        |
|         LTP*          | <u>95.55</u> | <u>93.83</u> | <u>94.68</u> | 16.040       | 86.63        | 89.66        | 88.12        | 31.100       |

> *Indicates that the model uses RTX 3090 GPU to accelerate inference;
>
> $^\dagger$ BERT-CRF has only trained 20 epochs, and the performance can be improved by further training;
>
> See the `models` directory for logs.


## Requirements

- python==3.7
- torch==1.12
- transformers=4.24
- see `requirements.txt`.


## Run

### Prepare data
```sh
cd data
wget http://sighan.cs.uchicago.edu/bakeoff2005/data/icwb2-data.zip
unzip icwb2-data.zip

cd icwb2-data
mkdir msr_processed & pku_processed
cp training/msr_training.utf8 msr_processed/training.utf8
cp gold/msr_test_gold.utf8 msr_processed/test.utf8

cp training/pku_training.utf8 pku_processed/training.utf8
cp gold/pku_test_gold.utf8 pku_processed/test.utf8
```

### Word dict
```sh
cd data
wget https://raw.githubusercontent.com/fxsjy/jieba/master/jieba/dict.txt
```

### Run model

Evaluate `fmm`, `bmm`, `bimm`, `mmseg`, `hmm`, and `jieba`, `thulac`, `ltp`, `hanlp`:
```sh
bash scripts/eval.sh
```

Train and Evaluate `BiLSTM-CRF`:
```sh
bash scripts/train_bilstm_crf.sh
```

Train and Evaluate `BERT-CRF`:
```sh
bash scripts/train_bert_crf.sh
```


## Web UI

![](/assets/ui.png)

### Back-end

based on `Flask`:
```sh
CUDA_VISIBLE_DEVICES=0 FLASK_APP=app.py flask run
```

### Front-end

based on `create-react-app`:
```sh
npm install
npm install react-scripts
NODE_OPTIONS=--openssl-legacy-provider npm start
```

## Cases

| Methods    | Sentence1                                                    | Sentence2                                      |
| :--------- | :----------------------------------------------------------- | :--------------------------------------------- |
| FMM        | **玲/英**/思前想后/，/对/哥哥/说/：/“/我/**不忍心**/扔下/穆/大爷/不管/啊/！/”/ | 我/也/想/过过/过儿/过过/的/生活                |
| BMM        | **玲/英**/思前想后/，/对/哥哥/说/：/“/我/**不忍心**/扔下/穆/大爷/不管/啊/！/”/ | 我/也/想/过过/过儿/过过/的/生活                |
| Bi-MM      | **玲/英**/思前想后/，/对/哥哥/说/：/“/我/**不忍心**/扔下/穆/大爷/不管/啊/！/”/ | 我/也/想/过过/过儿/过过/的/生活                |
| MMSeg      | **玲/英**/思前想后/，/对/哥哥/说/：/“/我/**不忍心**/扔下/穆/大爷/不管/啊/！/”/ | 我/也/想/过过/过儿/过过/的/生活                |
| HMM        | **玲/英思前/想/后**/，/对/哥哥/说/：“/我/不/忍心/**扔/下穆大爷**/不管/啊/！” | 我/也/想/过过/过儿/过过/的/生活                |
| BiLSTM-CRF | **玲/英思/前/想/后**/，/对/哥哥/说/：/“/我/**不忍/心**/**扔/下**/穆/大爷/不管/啊/！/” | 我/也/想/**过/过**/过儿/**过/过**/的/生活      |
| BERT-CRF   | 玲英/思前想后/，/对/哥哥/说/：/“/我/不/忍心/扔下/穆/大爷/不管/啊/！/” | 我/也/想/**过/过/过/儿/过/过**/的/生活         |
| jieba      | 玲英/思前想后/，/对/哥哥/说/：/“/我/**不忍心**/扔下/穆/大爷/不管/啊/！/”/ | 我/也/想/**过/过**/过儿/过过/的/生活           |
| thulac     | **玲/英思/前想后**/，/对/哥哥/说/：/“/我/不/忍心/扔下/穆/大爷/**不/管**/啊/！/” | 我/也/想/**过/过**/过儿/**过/过**/的/生活      |
| LTP        | 玲英思前想后/，/对/哥哥/说/：/“/我/不/忍心/扔下/穆/大爷/**不/管**/啊/！/” | 我/也/想/**过/过**/**过/儿**/**过/过**/的/生活 |
| HanLP      | **玲/英**/思前想后/，/对/哥哥/说/：/“/我/**不忍心**/扔下/**穆大爷**/不管/啊/！/”/ | 我/也/想/过过/**过/儿**/过过/的/生活           |
| Gold       | 玲英/思前想后/，/对/哥哥/说/：/“/我/不/忍心/扔下/穆/大爷/不管/啊/！/” | 我/也/想/过过/过儿/过过/的/生活                |




## References
- https://github.com/hemingkx/WordSeg
- https://github.com/hiyoung123/ChineseSegmentation
- https://github.com/ownthink/evaluation
- https://github.com/kb22/ML-React-App-Template