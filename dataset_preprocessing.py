# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 17:17:20 2020

@author: Alessandro
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



#leggo il dataset
path = "G:\\GitHubRepo\\AnomalyDet\\Anomaly-Detection\\dataset\\test2.csv"
df = pd.read_csv(path,sep=';')
column_names_to_not_normalize = ['Data']
column_names_to_normalize = [x for x in list(df) if x not in column_names_to_not_normalize ]

#normalizzo
for col in column_names_to_normalize:
    df[col] = df[col]/df[col].max()


#inizio il labeling delle anomalie
labeled_df = df.copy()

for i in range(1,df.shape[1]):
    colonna = df[df.columns[i]]
    print("Colonna in esame : ", i )
    col_mean = colonna.mean()
    col_std = colonna.std()
    treshold = col_mean + 3*col_std
    for j in range(0,colonna.size):
        item = colonna[j]
        if item >= treshold:
            colonna[j] = 1
        else:
            colonna[j] = 0  
    labeled_df.iloc[:,i] = colonna
    
#Genero la heatmap
ax = plt.axes()
sns.heatmap(labeled_df[column_names_to_normalize], ax = ax ,cmap="Blues")
ax.set_title('Heatmap 1')
ax.xlabel = "Sensore"
plt.show()


