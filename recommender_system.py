#!/usr/bin/env python
# coding: utf-8

# ## Section 1: Dataset preparation

# In[2]:
import warnings
warnings.filterwarnings("ignore")

#importing the packages needed
import pandas as pd
import re
import nltk


# In[3]:


#reading the 12 dataset scraped from different websites
df1=pd.read_csv("d1.csv")
df2=pd.read_csv("d2.csv")
df3=pd.read_csv("d3.csv")
df4=pd.read_csv("d4.csv")
df5=pd.read_csv("d5.csv")
df6=pd.read_csv("d6.csv")
df7=pd.read_csv("d7.csv")
df8=pd.read_csv("d8.csv")
df9=pd.read_csv("d9.csv")
df10=pd.read_csv("d10.csv")
df11=pd.read_csv("d11.csv")
df12=pd.read_csv("d12.csv")


# In[4]:


#concatenating all the dataframes to a single one
frames = [df1,df2,df3,df4,df5,df6,df7,df8,df9,df10,df11,df12]
df = pd.concat(frames)


# various dataframe functions for analysing the data
# 
# 1) df.describe ----describing the dataset
# 
# 2) df.shape  ------shape of the dataframe
# 
# 3) df.info() ------number of nonempty cells

# In[5]:


#dropping all the row where the about section is empty
#This is imp as we are analysing the cosine similarity of this section
data=df.dropna(axis = 0, how ='any')


# ## Section 2 -- Preprocessing of data

# In[6]:


#Joining the columns to make a unique text column which defines a package
features = ['place','package_name','about_trip']
def combine_features(row):
 return row['place']+" "+row['package_name']+" "+row['about_trip']
for feature in features:
    data[feature] = data[feature].fillna('') #filling all NaNs with blank string
data["combined_features"] = data.apply(combine_features,axis=1) #applying combined_features() method over each rows of dataframe and storing the combined string in “combined_features” column
#data.head(50) ---seeing the data


# In[7]:


#downloading stopwords to remove the common words
nltk.download('stopwords')
from nltk.corpus import stopwords


# In[8]:


#Function to do basiic 
def clean(text):
           
    # Urls
    text = re.sub(r"https?:\/\/t.co\/[A-Za-z0-9]+", "", text)
        
    # Words with punctuations and special characters
    punctuations =['@','#','!','?','+','&','*','[',']','-','%','.',':','/','(',')',';','$','=','>','<','|','{','}','^']
    for p in punctuations:
        text = text.replace(p, f' {p} ')

    return text


# In[9]:


data.iloc[6] = data.iloc[6].apply(lambda s : clean(s)) #cleaning the text using above function


# In[10]:


#removing stopwords 
from nltk.corpus import stopwords
data["combined_features"] = data["combined_features"].str.lower().str.split()
stop = stopwords.words('english')
data['combined_features']=data['combined_features'].apply(lambda x: [item for item in x if item not in stop])
data["combined_features"]= data["combined_features"].str.join(" ") #rejoining the words to text


# In[11]:


# defining a new column with no's and setting it as index
ind=[]
for i in range(1609):
     ind.append(i)

data.insert (0,"index",ind)
data.set_index(['index'])


# This marks the end of our preprocessing of data.

# ## Section 3: Applying Cosine Similarity

# In[13]:


#import modules
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# In[16]:


#data.replace('', np.nan, inplace=True)
cv = CountVectorizer() #creating new CountVectorizer() object
count_matrix = cv.fit_transform(data['combined_features'].values.astype('U'))  #fitting cv object to combine features column
cosine_sim = cosine_similarity(count_matrix) #calculating cosine similarity


# ## Section 4: Recommending places

# In[17]:


#creating new column to merge place and package_name which serves as user input identifier
data.head()
features2 = ['place','package_name']
def combine_features2(row):
 return row['place']+" "+row['package_name']
for feature in features2:
    data[feature] = data[feature].fillna('') #filling all NaNs with blank string
data["place_names"] = data.apply(combine_features,axis=1)
data["place_names"] = data["place_names"].str.lower()


# In[18]:


#function to search user input on the newly created column and return the index
import re
def get_index_from_title(place):
    for ind in data.index:
        mond=data.iloc[ind]['place_names']
        if re.search(place,mond):
            return(ind)


# In[21]:


#finding similar places using cosine similarity
print('\n\n')
place_selec = input("Please say a place where you have gone to or love to go \n")
print('\n\n')
place_index = get_index_from_title(place_selec)
#print(place_index)

similar_places = list(enumerate(cosine_sim[place_index])) #accessing the row corresponding to given place name to find all the similarity scores for that place name and then enumerating over it


# In[22]:


#sorting those packages in descending order 
sorted_similar_places = sorted(similar_places,key=lambda x:x[1],reverse=True)[1:]
#print(sorted_similar_places)


# In[26]:


#printing the top 5 recommendations
i=0
print("Top 5 similar travel packages like going to "+place_selec+" are:\n")
for element in sorted_similar_places:
    print("Package name: {}".format(data.loc[data['index'] == element[0], 'package_name'].values[0]))
    print("Place: {}".format(data.loc[data['index'] == element[0], 'place'].values[0]))
    dur=data.loc[data['index'] == element[0], 'time'].values[0]
    print("Duration:{}".format(" ".join(dur.split())))
    print("Amount: Rs {} .".format(data.loc[data['index'] == element[0], 'price'].values[0]))
    print('Emi amount: Rs {}'.format(data.loc[data['index'] == element[0], 'emi'].values[0]))
    i=i+1
    if i>5:
        break


# In[ ]:





# In[ ]:





# In[ ]:




