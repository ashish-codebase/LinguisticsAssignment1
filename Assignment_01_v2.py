#!/usr/bin/env python
# coding: utf-8

# In[26]:


import pandas as pd
import numpy as np


# In[ ]:


class Location:
    row:int
    col:int
    def __init__(self, row=9999, col=9999) -> None:
        self.row=row
        self.col=col
    def text(self):
        print(f"{self.row}, {self.col}")



def getMinLocation(distance_matrix_l1_init:pd.DataFrame):
    matrix2min = 9999
    matrix2RowColMin=Location(9999,9999)
    matrixsize = distance_matrix_l1_init.shape[0]
    for i in range(matrixsize):
        for j in range(matrixsize):
            if distance_matrix_l1_init.iloc[i,j]<matrix2min and distance_matrix_l1_init.iloc[i,j]>0:            
                matrix2min = distance_matrix_l1_init.iloc[i,j]
                matrix2RowColMin = Location(i,j)
    print("Min Location==>",matrix2RowColMin.text, "Min value==>", matrix2min)
    print("Row==>", distance_matrix_l1_init.columns[matrix2RowColMin.row], "Col==>",distance_matrix_l1_init.columns[matrix2RowColMin.col] )
    return matrix2RowColMin


def updateDistances (distanceMatrix:pd.DataFrame, minLocation:Location):
    distance_matrix_l1_init = distanceMatrix.copy()
    colNames = distance_matrix_l1_init.columns
#     lowerIndex, upperIndex
    comboCol1Name = f"S{minLocation.row+1}"
    comboCol2Name = f"S{minLocation.col+1}"
    for i in range(1, len(colNames),1):
        val1 = distance_matrix[comboCol1Name][colNames[i]]
        val2 = distance_matrix[colNames[i]][comboCol2Name]    
        distance_matrix_l1_init.iloc[0,i] = (val1 + val2)/2.0
        distance_matrix_l1_init.iloc[i,0] = (val1 + val2)/2.0
        print(f"{comboCol1Name}_{colNames[i]}({val1})".ljust(10, ' '),f"{comboCol2Name}_{colNames[i]}({val2})".ljust(10, ' '))
    return distance_matrix_l1_init


# In[4]:


def removeMinDistanceRowCol(distanceMatrix:pd.DataFrame, minValueLocaiton:Location):
    lowerIndex = minValueLocaiton.row
    upperIndex = minValueLocaiton.col
    colNames = distanceMatrix.columns
    rowcolString1 = colNames[lowerIndex]
    rowcolString2 = colNames[upperIndex]
    colName1 = colNames[lowerIndex].replace('S','')
    colName2 = colNames[upperIndex].replace('S','')
    newRowColName = f"S{colName1}{colName2}"
    
    # Remove columns
    distanceMatrix.drop(rowcolString1, axis=1, inplace=True)
    distanceMatrix.drop(rowcolString2, axis=1, inplace=True)
    # Remove rows
    distanceMatrix.drop(rowcolString1, inplace=True)
    distanceMatrix.drop(rowcolString2, inplace=True)


    # Filling row and col and index 0,0 with -9999
    rowCombo =distanceMatrix.iloc[0]
    newDF = pd.DataFrame(rowCombo, index=[0])
    distanceMatrix = pd.concat([newDF, distanceMatrix])
    rowArray  = np.zeros(distanceMatrix.shape[0])
    rowArray[:] = -9999
    distanceMatrix.insert(0, newRowColName, rowArray)
    distanceMatrix.iloc[0] = -9999
    distanceMatrix.index = distanceMatrix.columns
    
    # Setting diagonal = 0
    array = distanceMatrix.values
    np.fill_diagonal(array, 0)
    distanceMatrix_modified = pd.DataFrame(array, columns=distanceMatrix.columns, index=distanceMatrix.index)
    return distanceMatrix_modified


# In[5]:


# From XSLX file read specific sheet name.
df = pd.read_excel("Hw1-words.xlsx", sheet_name='Proto-words')
df


# In[6]:


maxRowsCount = df.shape[0]
maxRowsCount
keys = (list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'))[:maxRowsCount]
keys


# In[7]:


dfKeyed = df.copy()
for col in df.columns:
    selectedCol = df[col]
    unique_values = selectedCol.unique()
    word2key = dict(zip(unique_values, keys))
    dfKeyed[col].replace(word2key, inplace=True)


# In[8]:


dfKeyed


# In[9]:


matrix_size = dfKeyed.shape[0]
NameIndexed = []
for i in range(matrix_size):
    NameIndexed.append("S"+str(i+1))
print("Column and Row names",NameIndexed)


# ### Setting row/col names

# In[10]:


distance_matrix = pd.DataFrame(index=range(df.shape[0]), columns=range(df.shape[0]))
distance_matrix = pd.DataFrame(distance_matrix, index=NameIndexed)
distance_matrix.columns = NameIndexed


# In[11]:


min_value_location = Location()
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
            min_value_location = Location(row,col)        
        distance_matrix.iloc[row,col]=distance


# ### <u>**Distance matrix from Proto words**</u>

# In[12]:


distance_matrix


# ### Renaming columns as S1..Sn & finding the row/col index of the minimum distance

# In[13]:


distance_matrix.columns = NameIndexed
distance_matrix.shape
lowerIndex, upperIndex = (min_value_location.row, min_value_location.col)
print(f"Minimum distance row/col index==> {min_value_location.text()}")
print("Row==>", distance_matrix.columns[min_value_location.row], "Col==>",distance_matrix.columns[min_value_location.col] )


# In[14]:


newRowColName = f"S{lowerIndex+1}{upperIndex+1}"


# ### Creating a copy of distance matrix for calculation of 2nd step and removing the rows and column associated with minimum row/col distance.

# In[15]:


distance_matrix_l1 = distance_matrix.copy()
distance_matrix_l1.drop(distance_matrix_l1.columns[upperIndex], axis=1, inplace=True)
distance_matrix_l1.drop(distance_matrix_l1.columns[lowerIndex], axis=1, inplace=True)

distance_matrix_l1.drop(distance_matrix_l1.index[upperIndex], inplace=True)
distance_matrix_l1.drop(distance_matrix_l1.index[lowerIndex], inplace=True)
print("Distance matrix after removing min value rows and columns")
distance_matrix_l1


# ### Adding row and col at index 0,0 with with the row/col name.

# In[16]:


rowCombo =distance_matrix_l1.iloc[0]
newDF = pd.DataFrame(rowCombo, index=[0])
distance_matrix_l1 = pd.concat([newDF, distance_matrix_l1])
# rowCombo  = distance_matrix_l1[0]
rowArray  = np.zeros(distance_matrix_l1.shape[0])
rowArray[:] = np.nan
distance_matrix_l1.insert(0, f"S{lowerIndex+1}{upperIndex+1}", rowArray)


# In[17]:


indexNames = distance_matrix_l1.index.tolist()
indexNames[0]= f"S{lowerIndex+1}{upperIndex+1}"
distance_matrix_l1.index= indexNames


# #### Constructed a matrix with new colum/row name corresponding to min distance combo
# e.g. If min distance value is at S3 & S5; new col name will be S35

# In[18]:


distance_matrix_l1


# In[19]:


distance_matrix_l1_init = updateDistances(distance_matrix_l1, min_value_location)
distance_matrix_l1_init


# In[20]:


matrix2RowColMin = getMinLocation(distance_matrix_l1_init)


# ### Creating matrix and filling row=0; col=0 with dummy values -9999

# In[22]:


updatedMatrix = removeMinDistanceRowCol(distance_matrix_l1_init, matrix2RowColMin)
updatedMatrix


# In[24]:


updatedMatrix2 = updateDistances(updatedMatrix, matrix2RowColMin)
updatedMatrix2


# In[ ]:


distance_matrix_l1_init


# In[ ]:




