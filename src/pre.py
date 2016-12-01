# -*- coding: utf-8 -*-
import sys
import jieba
import re
from collections import Counter
from itertools import islice

'''
预处理语料库，获取词语的IDF。
复杂度太高了，单机跑起来很吃力。
'''

# 继承list，解决链式extend的问题。
class ListWithLinkExtend(list):
  def extend(self, value):
    super(ListWithLinkExtend, self).extend(value)
    return self

# 生成累加器，map处理保证不冲突
def generate_counter():
  counter = [0]
  def adder():
    counter[0] += 1
    return counter[0]
  return adder
#  path累加器
path_counter = generate_counter()

# 处理掉各种标点符号（不全）
pattern = '[\s+\.\!\/\_\,\$\?\!\@\#\$\%\^\&\*\(\)\_\+\=\-\%\^\*\:(+\"\']+' \
          '|[+——！：“”；，。？、~《》【】@#￥%……&*（）]+'

# 获取路径
def get_path_name(root_directory):
  if root_directory[-1] != '/':
    root_directory += '/'
  return map(lambda path:path+str(path_counter()).zfill(6)+'/',
             [root_directory+'C' for _ in range(9)])

# 合并文件名和路径，获取完整文件路径
def get_file_name(path):
  # full path: [10, 2000)
  return [d+i for d in get_path_name(path)
          for i in [str(_)+'.txt'
                    for _ in range(10, 2000)] ]

# 获取文件内容的辅助程序，直接对文件操作。数据集中文件编码不一
# 这里我的处理是只处理GBK文件。
# 集群的话应该修改成读取数据库
def _get_file_content(path):
  try:
    content = ''
    fp = open(path, 'r')
    while True:
      lines = fp.readlines(100)
      if not lines: break
      for line in lines:
        content += line
    fp.close()
    return content.decode('GBK').encode('UTF-8')
  except:
    return ''

# 获取文件的内容，发现会有空白转义符&nbsp;，这里顺便处理了
def get_file_content(file_name):
  return map(lambda content:re.sub(pattern.decode('UTF-8'), ' '.decode('UTF-8'), content.decode('UTF-8')),
             map(lambda content:content.replace('&nbsp;', ' '),
                 map(_get_file_content, file_name)))

# 给每个文件分词，去重成集合
def get_file_dictionary(files):
  return map(lambda x: set(x),
             map(lambda x: list(islice(x, 1000000)),
                 map(jieba.cut, files)))

def save_files(files, path):
  file_name = 'words.txt'
  print len(files)
  if path[-1] != '/':
    path += '/'
  fp = open(path+file_name, 'w')
  for article in files:
    for word in article:
      fp.write(word+'\n')
    fp.write('--end_of_file--'+'\n')
  fp.close()

def main(argv):
  # 更新编码，保证是UTF8
  default_encoding = 'UTF-8'
  if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
  assert len(argv) >= 3
  # 预处理文件名
  file_name = get_file_name(argv[1])
  # 读文件
  files = get_file_content(file_name)
  # 分词，展开generator，list存的元素是set
  files = get_file_dictionary(files)
  # 存盘
  save_files(files, argv[2])

if __name__ == '__main__':
  if len(sys.argv) == 1:
    # path = raw_input()
    path1 = 'F:/proj/Reduced/'
    path2 = 'F:/proj/'
    sys.argv.append(path1)
    sys.argv.append(path2)
    main(sys.argv)
  else:
    main(sys.argv)
