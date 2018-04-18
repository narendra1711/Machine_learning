# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 20:46:27 2018
http://pythonforengineers.com/create-a-word-counter-in-python/
@author: narendra
"""

import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("hubble_data.csv")
data.head()

headers = ["dist","rec_vel"]
 
data_no_headers = pd.read_csv("hubble_data_no_headers.csv", names = headers)
data_no_headers.head()

data_no_headers["dist"]

#If we replace the index with distance, then plotting becomes easy, as distance becomes the x axis, while velocity becomes the y axis.
data.set_index("distance", inplace= True)
data.head()

data.plot()
plt.show()

"""--------------------------------------------------------------------------"""
import pandas as pd
import matplotlib.pyplot as plt
 
data = pd.read_csv("wages_hours.csv")
data.head()

data = pd.read_csv("wages_hours.csv", sep = "\t")
data.head()

data2 = data[["AGE", "RATE"]]
data2.head()

#We’ll go for ascending (which is the default behaviour of the sort() function).
data_sorted = data2.sort(["AGE"])
data_sorted.head()

data_sorted.set_index("AGE", inplace=True)
data_sorted.head()

data_sorted.plot()
plt.show()

"""--------------------------------------------------------------------------"""
import pandas as pd
import matplotlib.pyplot as plt

headers = ["date", "visitors"]
data = pd.read_csv("visitors.csv", skiprows=4, names = headers)
data.head()

headers = ["date", "visitors_new"]
data_new = pd.read_csv("visitors-new.csv", skiprows=4, names = headers)
data_new.head()

#pd.merge() function merged the two dataframes.
data_combined = pd.merge(data, data_new)
data_combined.head()

	
data_combined.sort(["date"], inplace=True)

data_combined.set_index("date", inplace=True)
data_combined.head()

data_combined.plot()
plt.show()

"""--------------------------------------------------------------------------"""
data = pd.read_csv("operating-systems.csv")
data.head()

data.columns

data["Value"]

data["Item"]
