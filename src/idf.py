# -*- coding: utf-8 -*-
import sys
from collections import Counter
import math

def read_file(path):
  try:
    fp = open(path, 'r')
    words = []
    while True:
      lines = fp.readlines(100)
      if not lines: break
      for line in lines:
          words.append(line)
    fp.close()
    return words
  except:
    print '_BUG at line 6'
    return []
    
def read_file_size(path):
  fp = open(path, 'r')
  size = fp.readline(100)
  return int(size)

def save_file(path, IDF):
  fp = open(path, 'w')
  for idf in IDF:
    fp.write(str(idf[1])+' '+idf[0])
  fp.close()

def get_IDF(words, D):
  words = read_file(path1)
  words = Counter(filter(lambda x: x != '', words)).items()
  words = sorted(words, key=lambda x:x[1], reverse=True)
  IDF = map(lambda Dw:(Dw[0],math.log(float(D)/float(Dw[1])+0.01)), words)
  return IDF

def main(path1, path2, path3):
  words = read_file(path1)
  size = read_file_size(path2)
  IDF = get_IDF(words, size)
  save_file(path3, IDF)

if __name__ == '__main__':
  if len(sys.argv) == 1:
    # path = raw_input()
    path1 = 'F:/proj/words.txt'
    path2 = 'F:/proj/file_number.txt'
    path3 = 'F:/proj/IDF.txt'
    sys.argv.append(path1)
    sys.argv.append(path2)
    sys.argv.append(path3)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
  else:
    main(sys.argv[1], sys.argv[2], sys.argv[3])
