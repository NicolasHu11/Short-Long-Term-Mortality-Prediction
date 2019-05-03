#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sqlite3
import pandas as pd
import math


# ### table names

# In[2]:


conn = sqlite3.connect('MERGE.sqlite')
#pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'; ", conn)


# ### Column names in admissions table

# cursor = conn.execute('select * from admissions')
# names = [description[0] for description in cursor.description]
# names

# In[37]:


admissions = pd.read_sql("""SELECT *
                FROM admissions
                """,conn)
len(admissions)


# In[4]:


patients = pd.read_csv("PATIENTS.csv")


# ### SUBJECT_ID: Cannot merge 'int64' with 'object' dtype.

# In[5]:


#patients.dtypes
#admissions.dtypes


# ### Convert the dtype of SUBJECT_ID in patient from int64 to object.

# In[6]:


patients['SUBJECT_ID'] = patients['SUBJECT_ID'].apply(lambda x: str(x))


# In[7]:


patients.dtypes


# ### Merge admission and patient on SUBJECT_ID

# In[8]:


merge_df = pd.merge(admissions, patients, left_on = ['SUBJECT_ID'], right_on = ['SUBJECT_ID'], how = 'left')


# ### Convert the datetime to age.    type(age): list

# In[34]:


day = (pd.to_datetime(merge_df['ADMITTIME']) - pd.to_datetime(merge_df['DOB']))
year = day.dt.days/365
#https://github.com/YaronBlinder/MIMIC-III_readmission/blob/master/Report.pdf
#Patients older than 89 yrs old, set the age to 100.
def older_89(x):
    if x < 0:
        x = 100
    return x
year = year.apply(older_89)
age = []
for i in year:
    age.append(math.floor(i))
merge_df['Age'] = age


# In[39]:


Age_csv = merge_df.drop(columns = ['ROW_ID_x', 'ADMITTIME', 'DISCHTIME',
       'DEATHTIME', 'ADMISSION_TYPE', 'ADMISSION_LOCATION',
       'DISCHARGE_LOCATION', 'INSURANCE', 'LANGUAGE', 'RELIGION',
       'MARITAL_STATUS', 'ETHNICITY', 'EDREGTIME', 'EDOUTTIME', 'DIAGNOSIS',
       'HOSPITAL_EXPIRE_FLAG', 'HAS_CHARTEVENTS_DATA', 'AGE', 'ROW_ID_y',
       'GENDER', 'DOB', 'DOD', 'DOD_HOSP', 'DOD_SSN', 'EXPIRE_FLAG'])


# In[40]:


Age_csv.to_csv('Age.csv')

