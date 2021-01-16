import seaborn as sns
import matplotlib.pyplot as plt                   # For data visualization
import pandas as pd

         
def mark_and_extend_anomalies(df,look_ahead):
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
    df.reset_index(inplace=True)
    df['Time']=pd.to_datetime(df['Time'])
    df = df.sort_values(by="Time")
    df = df.set_index("Time")
    return df
    
def import_normalize_dataset(path):    
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
    ax = plt.axes()
    sns.heatmap(anomalies.T, ax = ax ,cmap="Oranges")   
    title = "Look ahead " + str(look_ahead)
    ax.set_title(title)
    ax.xlabel = "Sensore"
    ax.ylabel = "Data"
    plt.figure()  


df = import_normalize_dataset("G:\\GitHubRepo\\AnomalyDet\\Anomaly-Detection\\dataset\\originalcsv.csv")
df = sort_dataset_by_date(df)
df = df.T

look_ahead = 7
anomalies = mark_and_extend_anomalies(df,look_ahead)
plot_anomalies_heatmap(anomalies,look_ahead)


        
    