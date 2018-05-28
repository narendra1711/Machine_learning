# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 14:54:54 2018

@author: Narendra_Mugada
"""

# import the dataset
from nltk.corpus import inaugural
from wordcloud import WordCloud
import matplotlib.pyplot as plt
# extract the datataset in raw format, you can also extract it in other formats as well
#text = inaugural.raw()
text="NEW DELHI:  A day after Delhi recorded the season's hottest day with the mercury settling at 42 degrees Celsius, people in city can look forward to a little respite. Light rains are expected at night.The sky will be general cloudy with the possibility of light rain at night, an India Meteorological Department official told IANS.0 COMMENTSIt was a warm morning in the national capital on Friday with the minimum temperature recorded at 26 degrees Celsius, two notches above the season's average, the weather office said. The maximum temperature was likely to hover around 43 degrees Celsius and the humidity at 8.30 a.m. was 57 per cent.hursday's maximum temperature settled at 42 degrees Celsius, three notches above the season's average and the minimum was recorded at 25.5 degrees Celsius, a notch above the season's average"
text=str(text)
wordcloud = WordCloud(max_font_size=30).generate(text)
plt.figure(figsize=(6,3))
# plot wordcloud in matplotlib
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()