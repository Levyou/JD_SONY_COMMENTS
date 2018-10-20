#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/21 0021 19:41
# @Author  : y
from snownlp import SnowNLP
import pandas as pd
from matplotlib import pylab as pl
import re
import json
# txt = open(r'C:\Users\Mr.You\Desktop\y\jd\mydata1.json', 'rb')
# a = json.load(txt)
# print(a)

texts = open(r'C:\Users\Mr.You\Desktop\y\jd\jdsony.txt').readlines()

score_set = []
senti_score = []

for i in texts:
    content = re.search(r'"content": "(.*?)}', i)
    score = re.search(r'"score": "(.*?)",', i)
    a1 = SnowNLP(content.group(0))
    a2 = a1.sentiments
    score_set.append(score)
    senti_score.append(a2)
#     print('doing')

name_list = score_set
num_list = senti_score
pl.bar(range(len(num_list)), num_list, color='rgb', tick_label=name_list)
pl.show()
# table = pd.DataFrame(sentences, senti_score)
# # table.to_excel('F:/_analyse_Emotion.xlsx', sheet_name='Sheet1')
# # ts = pd.Series(sentences, senti_score)
# # ts = ts.cumsum()
# # print(table)
# x = [1, 2, 3, 4, 5, 6, 7, 8]
# pl.mpl.rcParams['font.sans-serif'] = ['SimHei']
# pl.plot(x, senti_score)
# pl.title(u'京东索尼手机')
# pl.xlabel(u'评 论 用 户')
# pl.ylabel(u'情 感 程 度')
# pl.show()