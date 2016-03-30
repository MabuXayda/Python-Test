'''
Created on Nov 20, 2015

@author: tunn8
'''
from os import path
from imread import imread
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

d = path.dirname(__file__)
text = open(path.join(d, 'alice.txt')).read()
alice_mask = imread(path.join(d, "alice_mask.jpg"))
wc = WordCloud(background_color="white", max_words=2000, mask=alice_mask, stopwords=STOPWORDS.add("said"))
wc.generate(text)
wc.to_file(path.join(d, "alice.jpg"))

plt.imshow(wc)
plt.axis("off")
plt.figure()
plt.imshow(alice_mask, cmap=plt.autumn())
plt.axis("off")
plt.show()
