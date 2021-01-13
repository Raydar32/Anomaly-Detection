# -*- coding: utf-8 -*-

"""
Created on Wed Dec 30 17:17:20 2020

'--------------------------------------------------------------------------------------------
' File      : dataset_processing.py
' Author    : Alessandro Mini (7060381)
' Date      : 31/12/2020
' Purpose   : Questo programma esegue il preprocessing dei dati come viene descritto 
'             nel paper, applicando i 5 step descritti:
'                 - Accumulazione dei dati (per il momento uso una pivoting table su excel)
'                 - Normalizzazione (non viene specficato il tipo, uso il massimo)
'                 - Anomaly detection empirica con regola (anomaly se  valore >mean + 3 std)
'                 - Labeling 0/1 e creazione di label set
'                 - Espansione dei giorni (TODO)
'--------------------------------------------------------------------------------------------

"""

#Import.. 

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

#Colori per format output.
W  = '\033[0m'  
R  = '\033[31m'
G  = '\033[32m'
O  = '\033[33m' 
B  = '\033[34m' 
P  = '\033[35m' 


def labelDataset(df):
    column_names_to_not_normalize = ['Data']
    column_names_to_normalize = [x for x in list(df) if x not in column_names_to_not_normalize ]
    
    #normalizzo i dati del dataset, ogni colonna con il massimo.
    for col in column_names_to_normalize:
        df[col] = df[col]/df[col].max()
    
    #inizio il labeling delle anomalie, uso un nuovo dataset  "labeled_df"
    labeled_df = df.copy()
    for i in range(1,df.shape[1]):
        colonna = df[df.columns[i]]
        #print("Colonna in esame : ", i )
        col_mean = colonna.mean()
        col_std = colonna.std()
        treshold = col_mean + 3*col_std     #Legge empirica per anomaly detection
        for j in range(0,colonna.size):     #Ogni elemento della colonna setto 1 se anomalo, 0 altrimenti
            item = colonna[j]
            if item >= treshold:
                colonna[j] = 1
            else:
                colonna[j] = 0  
        labeled_df.iloc[:,i] = colonna      #sostituisco la colonna nel nuovo dataset.   
    return labeled_df

def hasAnomaly(row):
    for item in row:
        if item==1:
            return True    
    return False

def askInput(question):
    while "the answer is invalid":
        reply = str(input(question+' (y/n): ')).lower().strip()
        if reply[0] == 'y':
            return True
        if reply[0] == 'n':
            return False
        
def spyder_cls():
    try:
        from IPython import get_ipython
        get_ipython().magic('clear')
        get_ipython().magic('reset -f')
    except:
        pass

#leggo il dataset csv (in cui è stata eseguita una pivoting table)
path = "G:\\GitHubRepo\\AnomalyDet\\Anomaly-Detection\\dataset\\test2.csv"
df = pd.read_csv(path,sep=';')
#Escludo la data dalla normalizzazione
column_names_to_not_normalize = ['Data']
column_names_to_normalize = [x for x in list(df) if x not in column_names_to_not_normalize ]

labeled_df = labelDataset(df)

#spyder_cls()
#Generazione heatmap 
chHeatmap = askInput("Generare la heatmap? ")
#chHeatmap = False #debug
if chHeatmap:
    print("--------- Heatmap & Labeling anomalie ---------")
    la = input("Inserire lookahead (in giorni) : ")
    #Genero la heatmap
    ax = plt.axes()
    sns.heatmap(labeled_df[column_names_to_normalize], ax = ax ,cmap="Blues")   #
    ax.set_title('Heatmap no look Ahead')
    ax.xlabel = "Sensore"
    ax.ylabel = "Giorno"
    plt.figure()
    
        
    #Avvio la procedura di lookup 
    print("Avvio procedura lookup")
    la_days = int(la)                            #Parametro di look-ahead possible modificarlo
    for j in range(1,df.shape[1]):
        colonna = labeled_df[labeled_df.columns[j]]
        i = 1
        while(i<len(colonna)):       
            if colonna[i] == 1:             #Condizione se anomalia
                #estendo l'anomalia
                for i in range(i,i+la_days):
                    colonna[i] = 1               
            i = i + 1  
        labeled_df.iloc[:,j] = colonna      #sostituisco la colonna con l'originale.  
    
    #Genero la heatmap 2 (con look-ahead)
    ax = plt.axes()
    sns.heatmap(labeled_df[column_names_to_normalize], ax = ax ,cmap="Oranges")   
    title = "Look ahead " + str(la_days)
    ax.set_title(title)
    ax.xlabel = "Sensore"
    ax.ylabel = "Giorno"
    plt.figure()
    
    


print("Avvio procedura di clustering")
clusters = int(input("Inserire num clusters > "))


anomaly_df = labeled_df[column_names_to_normalize].T
kmeans_model = KMeans(n_clusters = clusters,random_state=2,n_init=10,algorithm="auto")
label = kmeans_model.fit_predict(anomaly_df) #Stampo le labels
silhouetteScore = silhouette_score(anomaly_df, label)
centroids = kmeans_model.cluster_centers_
u_labels = np.unique(label)

table = [[]]


for item in u_labels:
   filtered = anomaly_df[label==item]    
   row = []
   for i in range(0,len(filtered)):
       row.append(filtered.index[i])
   table.append(row)
table.remove(table[0])


i = 0
for row in table:
    print(G+"Cluster ", i, " ", W)
    print("Sensori :")
    print(row)
    i = i + 1
#Calcolo il numero di anomalie per cluster

print("\n\n-------------------- Summary ---------------------")
print("Silhouette score: ", str(silhouetteScore))
i = 0
for row in table:
    anomCounter = 0
    for item in row:
        if hasAnomaly(labeled_df[item]):
            anomCounter = anomCounter + 1
    print("Cluster ", i , "Lunghezza ",str(len(row)),  "n. Anomalie: ", anomCounter, " percent. ", str(round(anomCounter/len(row),2)))
    i = i + 1


   
   










