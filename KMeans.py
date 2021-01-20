# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 21:38:50 2021

@author: Alessandro
"""
from tslearn.metrics import dtw


import random
import numpy as np

class KMeansClusterizer:
    
    def getClusters(self):
        """
        getClusters(self):
        Metodo getter che ritorna i clusters.
        """
        return self.clusters
    
    def getCentroids(self):
        """
        getCentroids(self):
        Metodo getter che ritorna i centroidi.
        """
        return self.centroids
    
    def __init__(self,anomalies,n,ITMAX,distance_metric):
        """
        __init__(self,anomalies,n,ITMAX,distance_metric):
        Costruttore della classe, prende in ingresso:
            anomalies: dataset labeled.
            n: numero di clusters.
            ITMAX: max iterazioni.
            distance_metric: metrica di distanza.
        """  
        self.anomalies = anomalies
        #Inizializzo clusters e centroidi
        clusters = [[]]
        centroids = [[]]
        for i in range(0,n):
            clusters.append([])
            centroids.append(anomalies.iloc[random.randint(0,200)].values)
        clusters.pop(0)
        centroids.pop(0)
        self.clusters = clusters
        self.centroids = centroids
        self.ITMAX = ITMAX
        self.distance_metric = distance_metric
        
    def k_means_assign_points(self):
        """
        k_means_assign_points(self):
        Metodo che assegna tutti i punti (sensori) al relativo cluster
        best fitting.
        """
        for i in range(0,self.anomalies.shape[0]):
            riga = self.anomalies.iloc[i]
            #Inizializzo il best fit
            best_fit = 0    
            #Inizializzo un valore di distanza
            distance = 10
            #step 1: assegno ognuno al suo cluster
            for j in range(0,len(self.centroids)):              
                if self.distance_metric=="euclid":
                    distanza_calcolata = np.linalg.norm(riga - self.centroids[j])
                if self.distance_metric == "dtw":
                    distanza_calcolata = dtw(riga,self.centroids[j])   
                if(distanza_calcolata<distance):
                    #Assegno best fit
                    best_fit = j  
                    #Aggiorno la distanza
                    distance = distanza_calcolata      
            #Aggiungo il punto al cluster best fit.
            self.clusters[best_fit-1].append(i)
            
    def k_means_recalc_centroid(self):  
        """
        k_means_recalc_centroid(self):  
        Metodo che ricalcola il centroide sulla base del concetto
        di centro di massa.
        """
        #per ogni cluster
        for i in range(0,len(self.clusters)):
            #prendo la casa contenuta nel cluster
            for j in range(0,len(self.clusters[i])):
                #ricostruisco l'indice del dataset originale
                indice = self.clusters[i][j]
                #prendo il valore dal datset della casa j-esima nel cluster i-esimo
                riga = self.anomalies.iloc[indice]                
                #accumulo i valori su ogni campo
                self.centroids[i] = np.add(self.centroids[i],riga)        
        #adesso divido ogni cluster per la sua size (secondo formula)
        for k in range(0,len(self.centroids)):
            #size
            size = len(self.clusters[k])
            #se un cluster è vuoto imposto size=1
            if(size==0):
                size=1            
            #divisione
            self.centroids[k] = np.divide(self.centroids[k],size)
            
    def clear_clusters(self):
        """
        clear_clusters(self): 
        Metodo che toglie tutti i sensori di un cluster
        """
        for cluster in self.clusters:
            cluster.clear()

    def fit(self):
        """
        fit(self):
        Metodo che esegue il fitting.
        """
        for i in range(0,self.ITMAX):
           print("[KMEANS]: Iterazione num. ",i)
           self.clear_clusters()
           self.k_means_assign_points()
           self.k_means_recalc_centroid()
           

  

        



