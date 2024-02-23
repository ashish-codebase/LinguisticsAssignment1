import pandas as pd
import numpy as np


df = pd.read_excel("Hw1-words.xlsx", sheet_name='Proto-words')  # Replace 'Sheet1' with the name of the sheet you want to read
df

df.columns

word_list = []
for i, column in enumerate(df.columns):
    # print(i, column)
    word_list.append(df[column].tolist())
# word_list = word_list.tolist()
word_list

values_list_flat = [val for sublist in df.values.tolist() for val in sublist]
uniques = np.unique(values_list_flat)
print(uniques)
print (len(uniques))

keys = list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklm')
len(keys)


proto_dict = dict(zip(uniques, keys))

df.replace(proto_dict, inplace=True)


matrix_size = df.shape[0]
NameIndexed = []
for i in range(matrix_size):
    NameIndexed.append("S"+str(i+1))
print(NameIndexed)


distance_matrix = pd.DataFrame(index=range(df.shape[0]), columns=range(df.shape[0]))
distance_matrix = pd.DataFrame(distance_matrix, index=NameIndexed)

min_value_location = []
min_value = 999999
for i in range (matrix_size):
    for j in range (matrix_size-i,0,-1):
        col=matrix_size-j
        row =i
        row1 = df.iloc[row]
        row2 = df.iloc[col]
        distance = (row1 != row2).sum()
        if min_value>distance and distance!=0:
            min_value = distance
            min_value_location = (row,col)        
        print(f"Distance between row {row} and {col}", "Distance =", distance)
        distance_matrix.iloc[row,col]=distance
distance_matrix

distance_matrix.columns = NameIndexed

distance_matrix.shape

min_value_location

lowerIndex, upperIndex = min_value_location

distance_matrix_l1 = distance_matrix.copy()

distance_matrix_l1.drop(distance_matrix_l1.columns[upperIndex], axis=1, inplace=True)
distance_matrix_l1.drop(distance_matrix_l1.columns[lowerIndex], axis=1, inplace=True)

distance_matrix_l1.drop(distance_matrix_l1.index[upperIndex], inplace=True)
distance_matrix_l1.drop(distance_matrix_l1.index[lowerIndex], inplace=True)

# # Rename column 'B' to 'New_B' at index 1
# distance_matrix_l1.rename(columns={distance_matrix_l1.columns[1]: f"S{lowerIndex}{upperIndex}"}, inplace=True)
# distance_matrix_l1.rename(columns={distance_matrix_l1.columns[1]: f"S{lowerIndex}{upperIndex}"}, inplace=True)

# # Rename the row at index 1 to 'Row_1'
# distance_matrix_l1.rename(index={distance_matrix_l1.index[1]: f"S{lowerIndex}{upperIndex}"}, inplace=True)
# distance_matrix_l1.rename(index={distance_matrix_l1.index[1]: f"S{lowerIndex}{upperIndex}"}, inplace=True)

distance_matrix_l1

rowCombo  = distance_matrix_l1.iloc[0]
rowCombo.iloc[:] = np.nan


# distance_matrix_l1.iloc[:, :] = np.nan


distance_matrix_l1.insert(0, f"S{lowerIndex+1}{upperIndex+1}", rowCombo)

distance_matrix_l1.rename(index={distance_matrix_l1.index[0]: f"S{lowerIndex+1}{upperIndex+1}"}, inplace=True)
# distance_matrix_l1.index[0] = f"S{lowerIndex}{upperIndex}"

distance_matrix_l1

dfnew = pd.DataFrame(distance_matrix_l1.iloc[2], index=[0])

dfnew

distance_matrix_l1.shape

new_distance_matrix = pd.DataFrame()
drop_index = max(min_value_location)
minIndex = min(min_value_location)

drop_index

distance_matrix_l1 = distance_matrix.copy()


distance_matrix_l1.drop(distance_matrix_l1.columns[min_value_location], axis=1, inplace=True)

distance_matrix_l1.drop(distance_matrix_l1.index[drop_index], inplace=True)



distance_matrix_l1

distance_matrix_drop1 = distance_matrix.drop(distance_matrix.columns[drop_index], axis=1)

NameIndexed

distance_matrix.columns = NameIndexed
distance_matrix = pd.DataFrame(distance_matrix, index=NameIndexed)
