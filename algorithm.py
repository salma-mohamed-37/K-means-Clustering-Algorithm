import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import copy

k=0


def preprocessInputs(filePath, kin, percentage):
    global k
    k = kin
    df = pd.read_csv(filePath)
    df = df[['Movie Name', 'IMDB Rating']]
    num_desired_records = int(len(df) * float(percentage) / 100)
    sample = df.sample(n=num_desired_records)
    return sample

def clustering(sample, centroids):
    global k
    if(centroids is None):
        random_rows = sample.sample(n=k)
        values = random_rows['IMDB Rating'].values
        centroids = pd.DataFrame({'value': values, 'Cluster Number': range(0, k)})

    print(centroids)
    
    clusters =[[] for _ in range(0,k)]
    for _,row in sample.iterrows():
        minimum = math.inf
        distance = math.inf
        cluster = None
        for _ ,c in centroids.iterrows():
            distance = math.sqrt(math.pow(row['IMDB Rating'] - c['value'],2))

            if distance < minimum :
                minimum = distance
                cluster = int(c['Cluster Number'])
        clusters[cluster].append(list([row['Movie Name'],row['IMDB Rating'], minimum]))        

    for i in range (0,k):
        new_centroid = 0
        sum =0
        for m in clusters[i]:
            sum+=m[1]
        new_centroid = sum/len(clusters[i])
        centroids.loc[i,'value']= new_centroid
    
    return clusters, centroids


def prepareResults(clusters):
    plottingData = [[] for _ in range(0,k)]
    result = ""
    for i in range (k):
        size = len(clusters[i])
        result += "\nCluster"+str(i+1)+": "+str(size)+" records"
        result += "\n"
        for m in clusters[i]:
            result += m[0]+" , "
            plottingData[i].append(m[1])
        result += "\n"    
    return result, plottingData


def plot(plottingData, centroids):
    plt.ion()  
    plt.figure()
    
    cmap = plt.cm.get_cmap('viridis', k) 
    colors = cmap(range(k))

    for i in range(k):
        offset = 0.2*np.random.rand(len(plottingData[i]))
        y = [point + offset[i] for point in plottingData[i]]
        plt.scatter(plottingData[i], y, color=colors[i], label=f"Cluster {i+1}")

    offset2 = 0.2
    yc = [point + offset2 for point in centroids['value']]
    plt.scatter(centroids['value'], yc, color ='red')    
    plt.xlabel("Ratings")
    plt.ylabel("Offset")
    plt.title("Clusters")
    plt.legend() 
    plt.xlim(0, 10)
    plt.show()

def removeOutliers(clusters, sample, distance_threshold=1):
    outlier_values = []  
    finalOutliers = "Outliers : "
    outliers = ""
    for i in range(k):
        cluster_data = copy.deepcopy(clusters[i])  
        for m in cluster_data: 
            if m[2] > distance_threshold:
                outlier_values.append(m[0]) 
                outliers += m[0]+": "+str(m[1])+", "
    finalOutliers += str(len(outlier_values))+" records \n"+outliers+"\n"            

    filtered_sample = sample[~sample['Movie Name'].isin(outlier_values)]

    return filtered_sample, finalOutliers  

def kmeans (filePa, k, percentage):
    sample = preprocessInputs(filePa, k, percentage)
    currentCentroids = None
    futureCentroids = None
    oldClusters = []
    newClusters = None
    final = True

    while True:
        final = True
        #print(currentCentroids)
        # print(futureCentroids)
        #print("**********************")
        #if (newClusters is not None):
            # for c in newClusters:
            #     print(c)
            #     print("*****************************")
        newClusters, futureCentroids= clustering (sample, currentCentroids)
        # print(futureCentroids)
        # print(currentCentroids)
        # print("f")
        

        for i in range(0,k):
            if len(oldClusters)  == 0 :
                final = False
                break
            if(len(newClusters[i]) != len(oldClusters[i])):
                final = False
                break
            for j in range(len(newClusters[i])): 
                m = newClusters[i][j]
                n = oldClusters[i][j]
                if not m[0] == n[0] :
                    final = False
                    break
            if not final :
                break
            
        if final :
            result, plottingData = prepareResults(newClusters)
            plot(plottingData, currentCentroids)
            newSample, result2,  = removeOutliers(newClusters, sample)
            currentCentroids = futureCentroids
            newClusters, futureCentroids = clustering (newSample, currentCentroids)
            result, plottingData = prepareResults(newClusters)
            plot(plottingData, currentCentroids)
            return result, result2
        else :
            print(newClusters)
            print("***********************************")
            oldClusters = newClusters
            currentCentroids = copy.deepcopy(futureCentroids)