# -*- coding: utf-8 -*-
import sys
import jieba
import re
from collections import Counter
from itertools import islice

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
                    for _ in range(10, 100)] ]

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

# 获取词典，这里会使用了刚才继承的list
# 解决链式extend的问题
# 用结巴分词来将每一个文件的词语切片
def get_dictionary(files):
  return list(reduce(lambda a, b: ListWithLinkExtend(a).extend(ListWithLinkExtend(b)),
                         map(lambda x: map(lambda y: y[0], x),
                             map(lambda content: Counter(jieba.cut(content)).items(), files))))

# 给每个文件分词，去重成集合
def get_file_dictionary(files):
  return map(lambda x: set(x),
             map(lambda x: list(islice(x, 1000000)),
                 map(jieba.cut, files)))

# 辅助函数，用于merge key相同的value(相加)
# 前提是 file 和 IDF 处理成了dict

# 获取每个词语的IDF
def get_IDF(dictionary, files):
  # 把files中的每一个file经分词处理成一个单词的集合
  # 将files中的每一个文章中的单词搞成(k,v)形式，类型是set，k是单词，v是1。
  # reduce的时候强转成dict，用Counter的功能，就可以按k合并掉v，并且v的操作是相加。
  # 完事转回set，求一波Dw返回就行了
  D = len(dictionary)
  files = reduce(lambda x, y: Counter(dict(x))+Counter(dict(y)),
                 map(lambda filex:map(lambda x:(x,1), filex), files))
  IDF = files.items()
  IDF = map(lambda x:(x[0],float(x[1]/float(D))), IDF)
  IDF = sorted(IDF, key=lambda x:x[1], reverse=True)
  for i in IDF:
    print i[0], i[1]
  return IDF

def main(argv):
  # 更新编码，保证是UTF8
  default_encoding = 'UTF-8'
  if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
  assert len(argv) >= 2
  # 预处理文件名
  file_name = get_file_name(argv[1])
  # 读文件
  files = get_file_content(file_name)
  # 拆出词典，存成set
  dictionary = set(get_dictionary(files))
  # 分词，展开generator，list存的元素是set
  files = get_file_dictionary(files)
  # 获取IDF
  IDF = get_IDF(dictionary, files)
  # 存盘

if __name__ == '__main__':
  if len(sys.argv) == 1:
    # path = raw_input()
    path = 'F:/proj/Reduced/'
    sys.argv.append(path)
    main(sys.argv)
  else:
    main(sys.argv)
