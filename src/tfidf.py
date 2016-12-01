# -*- coding: utf-8 -*-
import sys
import jieba
import re
from itertools import islice
from collections import Counter
import math

pattern = '[\s+\.\!\/\_\,\$\?\!\@\#\$\%\^\&\*\(\)\_\+\=\-\%\^\*\:(+\"\']+' \
          '|[+——！：“”；，。？、~《》【】@#￥%……&*（）]+'

def read_file(path):
  try:
    fp = open(path, 'r')
    words = ''
    while True:
      lines = fp.readlines(100)
      if not lines: break
      for line in lines:
          words += line
    fp.close()
    return words
  except:
    print '_BUG at function read_file.'
    return ''

def get_IDF(path):
  fp = open(path, 'r')
  IDF = []
  while True:
    lines = fp.readlines(100)
    if not lines: break
    for line in lines:
      line = line.split(' ')
      IDF.append((line[1], float(line[0])))
  return IDF

def get_TF(content):
  # 归一化后求词频
  size = len(content)
  content = map(lambda x:(x[0],float(x[1])/float(size)),
                Counter(filter(lambda x: x != '', content)).items())
  content = sorted(content, key=lambda x:x[1], reverse=True)
  return content

def get_TFIDF(TF, IDF):
  TFIDF = []
  IDF = dict(IDF)
  for it in TF:
    key = it[0]
    if key in IDF:
      value = IDF.get(key)
      TFIDF.append((key, (value+1.0)*it[1]))
    else:
      TFIDF.append((key, math.log(17910.0/1.0+0.01)*it[1]))
  return TFIDF

def main(argv):
  content = read_file(argv[1])
  content = re.sub(pattern.decode('UTF-8'), ' '.decode('UTF-8'), content.decode('UTF-8'))
  content = list(islice(jieba.cut(content), 100000))
  TF = get_TF(content)
  IDF = map(lambda x:(x[0][:-1],x[1]), get_IDF(argv[2]))
  TFIDF = get_TFIDF(TF, IDF)
  TFIDF = sorted(TFIDF, key=lambda x:x[1], reverse=False)
  TFIDF = filter(lambda x:x[0]!='　'.decode('UTF8') and x[0]!=' ', TFIDF)
  for i in TFIDF:
    print i[0], i[1]

if __name__ == '__main__':
    sys.argv.append('F:/proj/IDF.txt')
    sys.argv.append('F:/proj/case/test000001.txt')
    jieba.
    main(sys.argv)
