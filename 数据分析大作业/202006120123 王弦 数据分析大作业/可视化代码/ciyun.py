import jieba
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def trans_ch(txt):
  words = jieba.lcut(txt)
  newtxt = ''.join(words)
  return newtxt


f = open('gjc.txt','r',encoding = 'ANSI')
txt = f.read()
f.close
txt = trans_ch(txt)
mask = np.array(Image.open("tp.png"))
wordcloud = WordCloud(background_color="white",\
                      width = 800,\
                      height = 600,\
                      max_words = 200,\
                      max_font_size = 80,\
                      mask = mask,\
                      contour_width = 4,\
                      contour_color = 'steelblue',\
                        font_path =  "msyh.ttc"
                      ).generate(txt)
wordcloud.to_file('房子关键词_词云图2.png')

