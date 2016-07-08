#
dir = "/home/tunn/data/digit-recognizer/"

import pandas as pd
import math
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

df = pd.read_csv(dir + "train.csv")
df_test = pd.read_csv(dir + "testNew.csv")
cl = df.columns.values
x_cl = cl[1:]
y_cl = cl[0]


print math.sqrt(800)

def knn():
    knn = KNeighborsClassifier(n_neighbors=5)
    
    print "training knn ..."
    knn.fit(df[x_cl],df[y_cl])
    print "testing knn ..."

    df_test[y_cl] = knn.predict(df_test[x_cl])
    print "done"
    print df_test[y_cl]
    
def rf():
    rf = RandomForestClassifier(n_estimators=1000, max_features = 30)

    print "training rf ..."
    rf.fit(df[x_cl],df[y_cl])
    print "testing knn ..."
    df_test[y_cl] = rf.predict(df_test[x_cl])    
    print "done"
    print df_test[y_cl]

def svm():
    svm = SVC()
    
    print "training svm ..."
    svm.fit(df[x_cl],df[y_cl])
    print "testing svm ..."
    df_test[y_cl] = svm.predict(df_test[x_cl])
    print "done"
    print df_test[y_cl]
    
    
def main():
    svm()
    
if __name__ =="__main__":
    main()
    