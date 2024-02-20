#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import math


# In[98]:


def getMinLocation(distance_matrix_l1_init:pd.DataFrame):
    matrix2min = 9999
    matrix2RowColMin=(9999,9999)
    matrixsize = distance_matrix_l1_init.shape[0]
    for i in range(matrixsize):
        for j in range(matrixsize):
            if distance_matrix_l1_init.iloc[i,j]<matrix2min and distance_matrix_l1_init.iloc[i,j]>0:            
                matrix2min = distance_matrix_l1_init.iloc[i,j]
                matrix2RowColMin = (i,j)
    print("Min Location==>",matrix2RowColMin, "Min value==>", matrix2min)
    print("Row==>", distance_matrix_l1_init.columns[matrix2RowColMin[0]], "Col==>",distance_matrix_l1_init.columns[matrix2RowColMin[1]] )
    return matrix2RowColMin


# In[81]:


def updateDistances (distanceMatrix:pd.DataFrame, minLocation):
    distance_matrix_l1_init = distanceMatrix.copy()
    colNames = distance_matrix_l1_init.columns
#     lowerIndex, upperIndex
    comboCol1Name = f"S{minLocation[0]+1}"
    comboCol2Name = f"S{minLocation[1]+1}"
    for i in range(1, len(colNames),1):
        val1 = distance_matrix[comboCol1Name][colNames[i]]
        val2 = distance_matrix[colNames[i]][comboCol2Name]    
        distance_matrix_l1_init.iloc[0,i] = (val1 + val2)/2.0
        distance_matrix_l1_init.iloc[i,0] = (val1 + val2)/2.0
        print(f"{comboCol1Name}_{colNames[i]}({val1})".ljust(10, ' '),f"{comboCol2Name}_{colNames[i]}({val2})".ljust(10, ' '))
    return distance_matrix_l1_init


# In[109]:


def removeMinDistanceRowCol(distanceMatrix:pd.DataFrame, minValueLocaiton):
    distance_matrix_l1 = distanceMatrix.copy()
    lowerIndex = minValueLocaiton[0]
    upperIndex = minValueLocaiton[1]
    colNames = distance_matrix_l1.columns
    rowcolString1 = colNames[lowerIndex]
    rowcolString2 = colNames[upperIndex]
    colName1 = colNames[lowerIndex].replace('S','')
    colName2 = colNames[upperIndex].replace('S','')
    newRowColName = f"S{colName1}{colName2}"
    # Remove columns
    distance_matrix_l1.drop(rowcolString1, axis=1, inplace=True)
    distance_matrix_l1.drop(rowcolString2, axis=1, inplace=True)
    # Remove rows
    distance_matrix_l1.drop(rowcolString1, inplace=True)
    distance_matrix_l1.drop(rowcolString2, inplace=True)

    rowCombo =distance_matrix_l1.iloc[0]
    newDF = pd.DataFrame(rowCombo, index=[0])
    distance_matrix_l1 = pd.concat([newDF, distance_matrix_l1])
    rowArray  = np.zeros(distance_matrix_l1.shape[0])
    rowArray[:] = np.nan
    distance_matrix_l1.insert(0, newRowColName, rowArray)
    distance_matrix_l1.index = distance_matrix_l1.columns
    return distance_matrix_l1
    


# In[58]:


# From XSLX file read specific sheet name.
df = pd.read_excel("Hw1-words.xlsx", sheet_name='Proto-words')
df


# In[59]:


maxRowsCount = df.shape[0]
maxRowsCount
keys = (list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'))[:maxRowsCount]
keys


# In[60]:


dfKeyed = df.copy()
for col in df.columns:
    selectedCol = df[col]
    unique_values = selectedCol.unique()
    word2key = dict(zip(unique_values, keys))
    dfKeyed[col].replace(word2key, inplace=True)


# In[61]:


dfKeyed


# In[62]:


matrix_size = dfKeyed.shape[0]
NameIndexed = []
for i in range(matrix_size):
    NameIndexed.append("S"+str(i+1))
print("Column and Row names",NameIndexed)


# ### Setting row/col names

# In[83]:


distance_matrix = pd.DataFrame(index=range(df.shape[0]), columns=range(df.shape[0]))
distance_matrix = pd.DataFrame(distance_matrix, index=NameIndexed)
distance_matrix.columns = NameIndexed


# In[85]:


min_value_location = []
min_value = 999999
for i in range (matrix_size):
    for j in range (matrix_size):
        col=j
        row =i
        row1 = df.iloc[row]
        row2 = df.iloc[col]
        distance = (row1 != row2).sum()
        if min_value>distance and distance!=0:
            min_value = distance
            min_value_location = (row,col)        
        distance_matrix.iloc[row,col]=distance


# ### <u>**Distance matrix from Proto words**</u>

# In[96]:


distance_matrix


# ### Renaming columns as S1..Sn & finding the row/col index of the minimum distance

# In[87]:


distance_matrix.columns = NameIndexed
distance_matrix.shape
lowerIndex, upperIndex = min_value_location
print(f"Minimum distance row/col index==> {min_value_location}")
print("Row==>", distance_matrix.columns[min_value_location[0]], "Col==>",distance_matrix.columns[min_value_location[1]] )


# In[88]:


newRowColName = f"S{lowerIndex+1}{upperIndex+1}"


# ### Creating a copy of distance matrix for calculation of 2nd step and removing the rows and column associated with minimum row/col distance.

# In[89]:


distance_matrix_l1 = distance_matrix.copy()
distance_matrix_l1.drop(distance_matrix_l1.columns[upperIndex], axis=1, inplace=True)
distance_matrix_l1.drop(distance_matrix_l1.columns[lowerIndex], axis=1, inplace=True)

distance_matrix_l1.drop(distance_matrix_l1.index[upperIndex], inplace=True)
distance_matrix_l1.drop(distance_matrix_l1.index[lowerIndex], inplace=True)
distance_matrix_l1


# ### Adding row and col at index 0,0 with with the row/col name.

# In[90]:


rowCombo =distance_matrix_l1.iloc[0]
newDF = pd.DataFrame(rowCombo, index=[0])
distance_matrix_l1 = pd.concat([newDF, distance_matrix_l1])
# rowCombo  = distance_matrix_l1[0]
rowArray  = np.zeros(distance_matrix_l1.shape[0])
rowArray[:] = np.nan
distance_matrix_l1.insert(0, f"S{lowerIndex+1}{upperIndex+1}", rowArray)


# In[91]:


distance_matrix_l1


# In[ ]:





# In[92]:


indexNames = distance_matrix_l1.index.tolist()
indexNames[0]= f"S{lowerIndex+1}{upperIndex+1}"
distance_matrix_l1.index= indexNames


# #### Constructed a matrix with new colum/row name corresponding to min distance combo
# e.g. If min distance value is at S3 & S5; new col name will be S35

# In[93]:


distance_matrix_l1


# In[94]:


distance_matrix_l1_init = updateDistances(distance_matrix_l1, min_value_location)
distance_matrix_l1_init


# In[99]:


matrix2RowColMin = getMinLocation(distance_matrix_l1_init)


# In[100]:


distance_matrix_l1_init2 = updateDistances(distance_matrix_l1_init, matrix2RowColMin)
distance_matrix_l1_init2


# In[110]:


updatedMatrix = removeMinDistanceRowCol(distance_matrix_l1_init2, matrix2RowColMin)
updatedMatrix


# In[ ]:




