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
        return self.clusters
    def getCentroids(self):
        return self.centroids
    
    def __init__(self,anomalies,n,ITMAX,distance_metric):
        self.anomalies = anomalies
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
        for i in range(0,self.anomalies.shape[0]):
            riga = self.anomalies.iloc[i]
            best_fit = 0
            distance = 10
            #step 1: assegno ognuno al suo cluster
            for j in range(0,len(self.centroids)):
                #distanza_calcolata = dtw(riga,self.centroids[j])
                if self.distance_metric=="euclid":
                    distanza_calcolata = np.linalg.norm(riga - self.centroids[j])
                if self.distance_metric == "dtw":
                    distanza_calcolata = dtw(riga,self.centroids[j])                    
                if(distanza_calcolata<distance):
                    best_fit = j
                    distance = distanza_calcolata        
            self.clusters[best_fit-1].append(i)
            
    def k_means_recalc_centroid(self):  
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
        for cluster in self.clusters:
            cluster.clear()

    def fit(self):
        for i in range(0,self.ITMAX):
           print("[KMEANS]: Iterazione num. ",i)
           self.clear_clusters()
           self.k_means_assign_points()
           self.k_means_recalc_centroid()
           

  

        



