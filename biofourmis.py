
# coding: utf-8

# # HEALTH MONITORING SIMULATOR

# In[1]:

import pandas as pd


# In[2]:

import time


# # Randomly generating data for 2000 epochs

# In[12]:

import random
import time
import json

start = time.time()
print(start)
with open('result1.json', 'w') as fp:
    json.dump([], fp)
while start + 10 > time.time():
    h_rate = random.randint(10,160)
    r_rate = random.randint(0,100)
    activity = random.randint(0,100)
    data=dict()
    data["userId"]="abc"
    data["timestamp"]=time.time()
    data["heart_rate"]=h_rate
    data["respiration_rate"]=r_rate
    data["activity"]=activity
    print(data)
    with open('result1.json', 'r') as fp:
        feeds = json.load(fp)
    with open('result1.json', 'w') as fp:
        feeds.append(data)
        json.dump(feeds, fp)
    time.sleep(1)


# In[13]:

df = pd.read_json('result1.json')


# In[15]:

df


# In[16]:

print(sum(df['heart_rate']))


# ## Changing timestamp format from nanosec to sec

# In[17]:

df['timestamp']=df.timestamp.values.astype('datetime64[s]')


# In[18]:

from datetime import timedelta


# In[19]:

for ind in df.index: 
     print(df['timestamp'][ind]-timedelta(seconds=900))


# # Creating another dataframe containing Timestamp(every 15min), total heart rate, minimum, maximum, average heart rate during every interval of 15 minutes

# In[34]:

dfObj = pd.DataFrame(columns=['timestamp','Total_Sum','MIN','MAX','AVG','COUNT'])


# In[35]:

dfObj.head()


# ## Initial Start and End time of 15 minutes (900 seconds)

# In[36]:

start_obj = df['timestamp'][0]
print(start_obj)
end_obj=start_obj+timedelta(seconds=3)
print(end_obj)


# # Calculation of min, max and average heart_rate

# In[37]:

avg_sum=0

for ind in df.index: 
    val=df['timestamp'][ind]
    heart_rate=df['heart_rate'][ind]
    if val==end_obj:
        start_obj=end_obj
        end_obj=start_obj+timedelta(seconds=3)
    if df.timestamp[df.timestamp == val].count() and val>=start_obj and val<end_obj:
        print(val)
        if dfObj.timestamp[dfObj.timestamp == end_obj].count():
            for index in dfObj.index:
                if dfObj['timestamp'][index] == end_obj:
                    dfObj['Total_Sum'][index] = dfObj['Total_Sum'][index] + heart_rate
                    if heart_rate<dfObj['MIN'][index]:
                        dfObj['MIN'][index]=heart_rate
                    if heart_rate>dfObj['MAX'][index]:
                        dfObj['MAX'][index]=heart_rate
                    avg_sum=dfObj['Total_Sum'][index]/dfObj['COUNT'][index]
                    dfObj['AVG'][index]=avg_sum
                    dfObj['COUNT'][index]=dfObj['COUNT'][index]+1
        else:
            tempdf = pd.DataFrame({'timestamp':end_obj, 'Total_Sum':heart_rate,
                                   'MIN':heart_rate, 'MAX': heart_rate, 'AVG': heart_rate,'COUNT': [1]})
            dfObj = dfObj.append(tempdf, ignore_index=True)


# In[38]:

dfObj


# In[39]:

start_obj


# In[40]:

import numpy as np


# In[41]:

if val!=end_obj:
    dfObj=dfObj[:-1]


# In[42]:

dfObj


# # Writing the calculations along with the timestamp to csv

# In[43]:

dfObj.to_csv('tracker_res.csv',columns=['timestamp', 'MIN', 'MAX', 'AVG'],index=False)


# In[44]:

csv_file=pd.read_csv('tracker_res.csv')


# In[45]:

csv_file


# In[ ]:



