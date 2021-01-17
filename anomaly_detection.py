# | Author: Alessandro Mini 
# | Assignment for D.D.M Lab @ University of Florence.


import seaborn as sns
import matplotlib.pyplot as plt                   
import pandas as pd
import random
from tslearn.metrics import dtw
import numpy as np   

    

def mark_and_extend_anomalies(df_base,look_ahead):                  
    """
    mark_and_extend_anomalies(df_base,look_ahead):   
    This method find and extends the anomalies given a lookahead.
    it returns a new dataset in order to use multiple versions.
    """
    df = df_base.copy(deep=True)
    for index, row in df.iterrows():
        mean = row.mean()
        std = row.std()
        for idx, item in enumerate(row):
            if(item>=(mean+3*std)):
                row[idx] = 1
            else:
                row[idx]= 0  
   
    for row in df.iterrows():        
        i = 0    
        riga = row[1]
        while(i<len(riga)-1):        
            if(riga[i]==1):
                for i in range(i,i+look_ahead):
                    try:
                        riga[i] = 1
                    except:
                        pass
            i = i + 1
            
    return df

def sort_dataset_by_date(df):
    """
    sort_dataset_by_date(df):
    This method sorts a dataset by the "Time" field
    """
    df.reset_index(inplace=True)
    df['Time']=pd.to_datetime(df['Time'])
    df = df.sort_values(by="Time")
    df = df.set_index("Time")
    return df
    
def import_normalize_dataset(path):    
    """
    import_normalize_dataset(path)
    This method import and normalize the base dataset.
    """
    df = pd.read_csv(path,sep=";")    
    df["Time"] = pd.to_datetime(df["Time"])
    df['Time'] = df['Time'].dt.strftime('%d/%m/%Y')    
    aggregated_df =  df.groupby('Time')[list(df.columns)[1:]].sum()
    aggregated_df.sort_values(by="Time")    
    aggregated_df = (aggregated_df-aggregated_df.min())/(aggregated_df.max()-aggregated_df.min())
    for col in aggregated_df:
        df[col] = df[col]/df[col].max()         
    return aggregated_df

def plot_anomalies_heatmap(anomalies,look_ahead):
    """
    plot_anomalies_heatmap(anomalies,look_ahead)
    This method plots an heatmap using seaborn.
    """
    ax = plt.axes()
    sns.heatmap(anomalies.T, ax = ax ,cmap="Oranges")   
    title = "Look ahead " + str(look_ahead)
    ax.set_title(title)
    ax.xlabel = "Sensore"
    ax.ylabel = "Data"
    plt.show()  



    
def k_means_assign_points(clusters,centroids):
    for i in range(0,anomalies.shape[0]):
        riga = anomalies.iloc[i]
        best_fit = 0
        distance = 10
        #step 1: assegno ognuno al suo cluster
        for j in range(0,len(centroids)):
            if(dtw(riga,centroids[j])<distance):
                best_fit = j
                distance = (dtw(riga,centroids[j]))        
        clusters[best_fit-1].append(i)
    return clusters,centroids


def k_means_recalc_centroid(anomalies,centroids):  
    for i in range(0,len(clusters)):
        for j in range(0,len(clusters[i])):
            indice = clusters[i][j]
            riga = anomalies.iloc[indice]
            centroids[i] = centroids[i] + riga
    
    for k in range(0,len(centroids)):
        centroids[k] = np.divide(centroids[k],len(clusters[k]))
    return centroids


def hasAnomaly(serie):
    for item in serie:
        if item == 1:
            return True
    return False
df = import_normalize_dataset("G:\\GitHubRepo\\AnomalyDet\\Anomaly-Detection\\dataset\\originalcsv.csv")
df = sort_dataset_by_date(df)
df = df.T

look_ahead = 1
anomalies = mark_and_extend_anomalies(df,look_ahead)
#plot_anomalies_heatmap(anomalies,look_ahead)

clusters = [[]]
clusters.append([])
centroids= [[]]
centroids.append(anomalies.iloc[random.randint(0,200)].values)
centroids.append(anomalies.iloc[random.randint(0,200)].values)
centroids.pop(0)


for i in range(1,3):
    print("Iterazione ",i)
    clusters[0].clear()
    clusters[1].clear()
    clusters,centroids = k_means_assign_points(clusters,centroids)
    centroids = k_means_recalc_centroid(anomalies,centroids)
    
for i in range(0,len(clusters)):
    a = 0
    for j in range(0,len(clusters[i])):
        casa = anomalies.iloc[clusters[i][j]]
        if hasAnomaly(casa):
            a = a + 1
    print("Cluster ", i ," ha ", a ," anomalie")


    

            
            
        
    
        
    




        
    