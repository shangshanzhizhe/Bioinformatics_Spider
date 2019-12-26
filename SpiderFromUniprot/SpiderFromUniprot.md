# [SpiderFromUniprot.py](https://github.com/shangshanzhizhe/Bioinformatics_Spider/blob/master/SipderFromUniport/SpiderFromUniprot.py)

根据比对到Uniprot库或模式生物的比对结果，从uniprot数据库爬取自己的基因的名称和功能的爬虫脚本

## 依赖环境

**python3**\
bs4\
requests\
lxml\
argparse

```sh
pip3 install bs4 requests lxml argparse
```

## 使用方法

```txt
python3 SpiderFromUniprot.py --help

usage: SpiderFromUniprot.py [-h] [-b BLAST] [-t TYPE]

This script is to convert your gene name to the orthologous human gene name,
which based on the blastp result

optional arguments:
  -h, --help            show this help message and exit
  -b BLAST, --blast BLAST
                        Your blast result file
  -t TYPE, --type TYPE  The blast agsinst type: Homolog Gene (gene) /
                        Swissprot Qurey (swiss), default:gene
```

## 输入文件

输入文件为两列，第一列为自己的基因名称，第二列为模式生物基因名称或Swissprot query，制表符分隔.

### 模式生物基因名称

```txt
ENSP00000301093-D94	ENSP00000334164
ENSP00000301093-D94	ENSP00000334164
ENSP00000301093-D94	ENSP00000334164
ENSP00000284073-D1	ENSP00000392607
ENSP00000299415-D1	ENSP00000299415
```

### Swissprot Query

```txt
evm.model.01.1109	Q8BG84
evm.model.01.1110	F4I037
evm.model.01.1187	F4HW79
evm.model.01.1325	Q94HW2
evm.model.01.1367	Q9H972
```

## 输出文件

输出为标准输出，输出文件后加上两列：基因名称和功能

## 示例

```sh
python3 SpiderFromUniprot.py -b Sample/ATH.test.input.txt -t swiss > Sample/ATH.test.output.txt
```

> 占用情况：9.41s user 1.02s system 7% cpu 2:28.56 total

```sh
python3 SpiderFromUniprot.py -b Sample/Human.test.input.txt -t gene > Sample/Human.test.output.txt
```

> 占用情况：13.98s user 1.32s system 19% cpu 1:20.48 total