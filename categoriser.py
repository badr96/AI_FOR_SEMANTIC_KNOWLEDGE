#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer
from nltk.corpus import stopwords 


# In[2]:


df = pd.read_csv('Dataset/poi.csv')
df.head()


# In[3]:


data = df[{"name","description_fr"}]
data.shape


# In[4]:


import re

for index in range(0, len(data)):  
    # Remove all the special characters
    data["description_fr"][index] = re.sub(r'\W', ' ', str(data["description_fr"][index]))
 
    # remove all single characters
    data["description_fr"][index] = re.sub(r'\s+[a-zA-Z]\s+', ' ', data["description_fr"][index])

    data["description_fr"][index] = re.sub(r'\W*\b\w{1,3}\b', ' ', data["description_fr"][index])
  
    # Remove single characters from the start
    data["description_fr"][index] = re.sub(r'\^[a-zA-Z]\s+', ' ', data["description_fr"][index]) 
 
    # Substituting multiple spaces with single space
    data["description_fr"][index] = re.sub(r'\s+', ' ', data["description_fr"][index], flags=re.I)
 
    # Removing prefixed 'b'
    data["description_fr"][index] = re.sub(r'^b\s+', '', data["description_fr"][index])
 
    # Converting to Lowercase
    data["description_fr"][index] = data["description_fr"][index].lower()


# In[11]:


tfidfconverter = TfidfVectorizer(max_features=1000, min_df=5, max_df=0.7, stop_words=stopwords.words('french'))  
X = tfidfconverter.fit_transform(data.description_fr.values).toarray()


# In[12]:


Sum_of_squared_distances = []
K = range(1,25)
for k in K:
    km = KMeans(n_clusters=k)
    km = km.fit(X)
    Sum_of_squared_distances.append(km.inertia_)


# In[13]:


plt.plot(K, Sum_of_squared_distances, 'bx-')
plt.xlabel('k')
plt.ylabel('Sum_of_squared_distances')
plt.title('Elbow Method For Optimal k')
plt.show()


# In[14]:


for i in range(5):
    km = KMeans(n_clusters=14)
    km.fit(X)
#Plusieurs executions pour l'initialisation 


# In[23]:


data["cluster"] = km.labels_


# In[16]:


order_centroids = km.cluster_centers_.argsort()[:, ::-1]
terms = tfidfconverter.get_feature_names()


# In[18]:


i = 0
data['cluster_name'] = 'lourd'
cluster_center =[]
cluster_index = data['cluster'].to_list()
for index in cluster_index:
    cluster_center.append(int(order_centroids[index,:1]))

for center in cluster_center:
    data['cluster_name'][i] = terms[center]
    i +=1


# In[22]:


data.to_csv('Dataset/predicted_data.csv')


# In[27]:


data


# In[ ]:




