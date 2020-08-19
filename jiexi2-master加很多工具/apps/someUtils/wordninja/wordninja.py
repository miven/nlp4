import gzip, os, re
from math import log


__version__ = '2.0.0'


# I did not author this code, only tweaked it from:
# http://stackoverflow.com/a/11642687/2449774
# Thanks Generic Human!


# Modifications by Scott Randal (Genesys)
#
# 1. Preserve original character case after splitting
# 2. Avoid splitting every post-digit character in a mixed string (e.g. 'win32intel')
# 3. Avoid splitting digit sequences
# 4. Handle input containing apostrophes (for possessives and contractions)
#
# Wordlist changes:
# Change 2 required adding single digits to the wordlist
# Change 4 required the following wordlist additions:
#   's
#   '
#   <list of contractions>

'''
看看英文分词怎么做的
'''



class LanguageModel(object):
  def __init__(self, word_file):
    # Build a cost dictionary, assuming Zipf's law and cost = -math.log(probability).
    with gzip.open(word_file) as f:
      words = f.read().decode().split()


    self._wordcost = dict((k, log((i+1)*log(len(words)))) for i,k in enumerate(words))
    #生成了一个wordcost字典.key是单词,value是罕见度.单词越长越罕见,单词越靠后越罕见.
    #所以我们切词要按照cost最低的切.
    self._maxword = max(len(x) for x in words)#词表里面最大长度的单词的长度
   

  def split(self, s):
    """Uses dynamic programming to infer the location of spaces in a string without spaces."""
    l = [self._split(x) for x in _SPLIT_RE.split(s)]
    return [item for sublist in l for item in sublist]
  #双重for循环也可以写一行.


  def _split(self, s):
    # Find the best match for the i first characters, assuming cost has
    # been built for the i-1 first characters.
    # Returns a pair (match_cost, match_length).
    def best_match(i):
      candidates = enumerate(reversed(cost[max(0, i-self._maxword):i]))
      return min(   (c + self._wordcost.get(s[i-k-1:i].lower(), 9e999), k+1) for k,c in candidates)
      #candidates是一个词表.如果字典中没有这个值,那么就让他cost无限大,这里就是9e999
    #如何避免切分的组合爆炸问题?这个算法怎么加速的?好像还是用了贪婪,只是每一次考虑前self._maxword
    #个单词做重新排序得到cost即可.类似动态规划.
    #确实是最优解,不是贪婪.可以证明这个就是最优解.所以最后的时间复杂度是O(N).
    #tuple排序会先按照第一个,相同时候再按照第二个
    # Build the cost array.
    cost = [0]
    for i in range(1,len(s)+1):
      c,k = best_match(i)
      cost.append(c)

    # Backtrack to recover the minimal-cost string.
    #根据k的值,切回去.
    out = []
    i = len(s)
    while i>0:

      c,k = best_match(i)
      assert c == cost[i]
      # Apostrophe and digit handling (added by Genesys)
      newToken = True
      if not s[i-k:i] == "'": # ignore a lone apostrophe
        if len(out) > 0:
          # re-attach split 's and split digits
          if out[-1] == "'s" or (s[i-1].isdigit() and out[-1][0].isdigit()): # digit followed by digit
            out[-1] = s[i-k:i] + out[-1] # combine current token with previous token
            newToken = False
      # (End of Genesys addition)

      if newToken:
        out.append(s[i-k:i])

      i -= k

    return reversed(out)

DEFAULT_LANGUAGE_MODEL = LanguageModel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'wordninja','wordninja_words.txt.gz'))
_SPLIT_RE = re.compile("[^a-zA-Z0-9']+")

def split(s):
  return DEFAULT_LANGUAGE_MODEL.split(s)




'''
测试
'''

lm = LanguageModel('wordninja/wordninja_words.txt.gz')
tmp=lm.split("that'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadgethat'sthesheriff'sbadge")


'''
解压之后看这个模型就会发现他是一个12万词组成的txt文档.
这个还是可以考虑dat树加速.类似的加速还有dfa算法.
这个算法貌似nlp里面的万能加速算法.
'''