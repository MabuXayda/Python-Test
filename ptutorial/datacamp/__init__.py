#

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#%%
plt.style.use("ggplot")
age = [46,20,52,30,57,25,28,36,22,43,57,33,22,63,40,48,28,49]
bmi = [25.4,20.6,26.2,22.6,25.4,23.1,22.7,24.9,19.8,25.3,23.2,21.8,20.9,26.7,26.4,21.2,21.2,22.8]
chol = [3.5,1.9,4.0,2.6,4.5,3.0,2.9,3.8,2.1,3.8,4.1,3.0, 2.5,4.6,3.2,4.2,2.3,4.0]

data = pd.DataFrame([age,bmi,chol]).transpose()
data.columns = ["age","bmi","chol"]
data.sort(["age"],inplace=True)
print data.corr(method="pearson")

#%%
line, = plt.plot(data.age, data.chol, "m-", linewidth = 5.0)
#line.set_antialiased(False)
plt.setp(line)
plt.xlabel("age")
plt.ylabel("chol")
plt.show()

#ax = plt.subplot(111)
#t = np.arange(0.0, 5.0, 0.01)
#s = np.cos(2*np.pi*t)
#line, = plt.plot(t, s, lw=2)
#plt.annotate('local max', xy=(2, 1), xytext=(3, 1.5),
#            arrowprops=dict(facecolor='black', shrink=0.05),
#            )
#plt.ylim(-2,2)
#plt.show()
#print plt.style.available

#%% 
#data.plot(y = data.index)
from pandas.tools.plotting import andrews_curves
data = pd.read_csv("https://raw.githubusercontent.com/pydata/pandas/master/pandas/tests/data/iris.csv")

#%%
andrews_curves(data, "Name")