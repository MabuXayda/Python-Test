'''
Created on Nov 20, 2015

@author: tunn8
'''
from scipy.misc import imread
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import numpy as np
from PIL import Image
import random

d = "/home/tunn/workspace/Project-Python/Python-Test/AliceWordCloud/"
def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(%d, 75%%, %d%%)" % (random.randint(0, 100), random.randint(30, 70))

#%%
text = open(d + "hippo.txt").read().upper()

mask = np.array(Image.open(d + "hippo.jpg"))
#mask_coloring = imread(d + "hippo_violet.jpg")
#coloring =  ImageColorGenerator(mask_coloring)

stopwords = set(STOPWORDS)
stopwords.add("use")
stopwords.add("more")
stopwords.add("edit")
stopwords.add("such")
stopwords.add("need")
stopwords.add("set")
stopwords.add("general")
stopwords.add("provide")
stopwords.add("base")
stopwords.add("government")
stopwords.add("per")
stopwords.add("day")
stopwords.add("handle")
stopwords.add("term")
stopwords.add("applicable")
stopwords.add("include")
stopwords.add("one")
stopwords.add("parallel")
stopwords.add("year")
stopwords.add("institute")
stopwords.add("within")
stopwords.add("unit")
stopwords.add("citation")
stopwords.add("user")
stopwords.add("require")
stopwords.add("authors")
stopwords.add("through")
stopwords.add("between")
stopwords.add("help")
stopwords.add("allows")
stopwords.add("well")
stopwords.add("department")
stopwords.add("over")
stopwords.add("may")
stopwords.add("using")
stopwords.add("per")
stopwords.add("used")
stopwords.add("also")
stopwords.add("sets")
stopwords.add("based")
stopwords.add("every")
stopwords.add("from")
stopwords.add("manufacturing")
stopwords.add("information")
stopwords.add("time")
stopwords.add("system")


wc = WordCloud(background_color="black", max_words=2000, mask=mask, margin=7, font_path="/home/tunn/londrina/LondrinaSketche-Regular.otf", 
               stopwords=stopwords, max_font_size=350).generate(text)

#plt.imshow(wc.recolor(color_func=color_func))
#plt.imshow(wc.recolor(color_func=coloring))
#plt.imshow(wc)


wc.to_file(d + "hippo_25.png")

