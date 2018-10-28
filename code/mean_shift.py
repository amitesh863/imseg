# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 18:52:37 2018

@author: durgesh singh
"""

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist


input_dir = '../data/'
output_dir = '../result/'





def assign_cluster(data_arr,means):
    #mediods = data_arr[med_indx]
    dists = np.zeros((data_arr.shape[0],len(means)))
    
    for i in range(means.shape[0]):
        diff = data_arr - means[i]
        dists[:,i] = np.linalg.norm(diff,axis=1)
    cluster_nos= np.argmin(dists,axis=1).reshape(data_arr.shape[0],1)
    #print(cluster_nos)
    data_arr = np.concatenate([data_arr,cluster_nos],axis=1)
    return data_arr


#gaussian mean for calculating density in epsilon negihobour
def calc_density_mean(neig,seed,rad):
    weights = np.exp(-1*np.linalg.norm((neig-seed)/rad,axis=1))
    mean = np.array(np.sum(weights[:,None]*neig,axis=0)/np.sum(weights),dtype=np.int64)
    return mean
    
def coalesce_means(means,bandwidth):
    flags = [1 for me in means]
    for i in range(len(means)):
        if flags[i] == 1:
            w = 1.0
            j = i + 1
            while j < len(means):
                dsm = np.linalg.norm(means[i] - means[j])
                if dsm < bandwidth:
                    means[i] = means[i] + means[j]
                    w = w + 1.0
                    flags[j] = 0
                j = j + 1
            means[i] = means[i]/w
    converged_means = []
    for i in range(len(means)):
        if flags[i] == 1:
            converged_means.append(means[i])
    converged_means = np.array(converged_means)
    return converged_means


#function of kernel density estimation
def kde(data_arr,mean_indx,rad):
    means = data_arr[mean_indx]
    
    iters=0
    while(True):
        new_means =[]
        for indx in range(means.shape[0]):
            mean =means[indx]
            dist = np.linalg.norm(data_arr - mean,axis=1)
            neig = data_arr[np.where(dist < rad)]
            new_mean = calc_density_mean(neig,mean,rad)
            new_means.append(new_mean)
        new_means = np.array(new_means)
        if np.array_equal(new_mean,mean):
            break
        means = new_means
        iters+=1
    return means


#reading the image in RGB format

arr_img= np.array(Image.open(input_dir+'input2.jpg').resize((256,256)))

'''
plt.figure()
plt.imshow(arr_img)
plt.show()
'''
rad = 7
#handling grayscale vs color case
if (len(arr_img.shape) == 2):
    w,h = arr_img.shape
    data_arr = arr_img.reshape((w*h,1))
elif(len(arr_img.shape) == 3):
    w,h,d = arr_img.shape
    data_arr = arr_img.reshape((w*h,d))    
no_probes = 50


#selecting random means given by k
mean_indx = np.random.choice(data_arr.shape[0],no_probes,replace=True)
#performing kde for each mean
kde_means = kde(data_arr,mean_indx,rad)
#assigning the clusters
clus_data_arr = assign_cluster(data_arr,kde_means)
final_means = coalesce_means(kde_means,rad)
clus_data_arr = assign_cluster(data_arr,final_means)


#for each mean and its corresponding cluster
for k in range(final_means.shape[0]):
    idx = np.where(clus_data_arr[:,-1] == k)
    clus_data_arr[idx,:-1]=final_means[k]
    

#showing the final clustered image
data_arr = clus_data_arr[:,:-1]
data_arr= data_arr.reshape(arr_img.shape)
plt.figure()
plt.imshow(data_arr)
plt.show()



