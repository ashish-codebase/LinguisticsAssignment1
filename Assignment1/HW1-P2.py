import pandas as pd

class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []
        self.parent = None

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def get_parent(self):
        return self.parent

    def get_children(self):
        return self.children
    
    def __repr__(self, level=0):
        ret = "\t" * level + repr(self.data) + "\n"
        for child in self.children:
            ret += child.__repr__(level+1)
        return ret
    
def node_exists(root, node):
    children = root.get_children()
    while len(children) != 0: 
        if node in children:
            return node
        for child in children:
            return node_exists(child, node)
    return None

    
def find_longest(column):
    max_len = 0
    for word in column:
        if len(word) > max_len:
            max_len = len(word)
    return max_len

def find_consensus_sequence(column):
    all_chars_count = []
    for i in range(0, find_longest(column)):
        chars_count = {}
        for word in column:
            char = word[i]
            if char in chars_count:
                chars_count[char] += 1
            else:
                chars_count[char] = 1
        all_chars_count.append(chars_count)
    keys_with_largest_values = [max(d, key=d.get) for d in all_chars_count]
    return ''.join(keys_with_largest_values)

def find_mutations_set(column, consensus_sequence):
    mutations_set = []
    for word in column:
        word_mutations = []
        for index, char in enumerate(consensus_sequence):
            if char != word[index]:
                word_mutations.append({word[index]: index})
        mutations_set.append(word_mutations)
    return mutations_set

def find_initial_cm_matrix(mutations_set):
    inital_common_mutation_matrix = [[None for _ in range(len(mutations_set))] for _ in range(len(mutations_set))]

    for row_index, row in enumerate(inital_common_mutation_matrix):
        for column_index, column in enumerate(inital_common_mutation_matrix):
            if row_index == column_index:
                inital_common_mutation_matrix[row_index][column_index] = mutations_set[row_index]

    for row_index, row in enumerate(inital_common_mutation_matrix):
        for column_index, column in enumerate(row):
            if row_index > column_index:
                inital_common_mutation_matrix[row_index][column_index] = None
                continue
            inital_common_mutation_matrix[row_index][column_index] = find_dictionaries_common_items(inital_common_mutation_matrix[row_index][row_index], inital_common_mutation_matrix[column_index][column_index])

    return inital_common_mutation_matrix

def find_dictionaries_common_items(dict1, dict2):
    if dict1 == None or dict2 == None:
        return None
    if len(dict1) == 0 or len(dict2) == 0:
        return []
    common_dicts = [d1 for d1 in dict1 for d2 in dict2 if d1 == d2]
    return common_dicts

def find_cmm(common_mutation_matrix, language_family_tree_root, titles):
    row, column = find_biggest_mutation(common_mutation_matrix)
    if row == -1:
        return common_mutation_matrix
    parent = TreeNode(f"S{titles[row][1:]}{titles[column][1:]}")
    node1 = node_exists(language_family_tree_root, titles[row])
    node2 = node_exists(language_family_tree_root, titles[column])

    ch1_has_parent = False
    ch2_has_parent = False
    if node1 != None:
        ch1_has_parent = True 
    if node2 != None:
        ch2_has_parent = True

    if not ch1_has_parent and not ch2_has_parent:

        child1 = TreeNode(f"S{titles[row][1:]}")
        child2 = TreeNode(f"S{titles[column][1:]}")
        parent.add_child(child1)
        parent.add_child(child2)
        language_family_tree_root.add_child(parent)

    else:

        if ch1_has_parent:
            child1.parent.add_child(parent)
            child1.parent = parent
        else:
            child1 = TreeNode(f"S{titles[row][1:]}")
            parent.add_child(child1)

        if ch2_has_parent:
            child2.parent.add_child(parent)
            child2.parent = parent
        else:
            child2 = TreeNode(f"S{titles[column][1:]}")
            parent.add_child(child2)

    if column > row:
        titles[row] = f"S{titles[row][1:]}{titles[column][1:]}"
        titles.pop(column)
        for i in range(len(common_mutation_matrix[0])):
                common_mutation_matrix[i][row] = find_dictionaries_common_items(common_mutation_matrix[i][column], common_mutation_matrix[i][row])
        common_mutation_matrix = drop_column(common_mutation_matrix, column)
        common_mutation_matrix = drop_row(common_mutation_matrix, column)
    else:
        titles[column] = f"S{titles[column][1:]}{titles[row][1:]}"
        titles[row] = titles[column]
        common_mutation_matrix = drop_row(common_mutation_matrix, row)
    return find_cmm(common_mutation_matrix, language_family_tree_root, titles)

def find_biggest_mutation(common_mutation_matrix):
    max_len = 0
    row = None
    column = None
    for i in range(len(common_mutation_matrix[0])):
        for j in range(i+1, len(common_mutation_matrix[0])):
            if len(common_mutation_matrix[i][j]) > max_len:
                row = i
                column = j
                max_len = len(common_mutation_matrix[i][j])
    if max_len == 0:
        return -1, -1
    return row, column

def drop_column(data, column_index):
    return [row[:column_index] + row[column_index+1:] for row in data]

def drop_row(data, row_index):
    return data[:row_index] + data[row_index+1:]

def main():
    file_path = 'Hw1-words.xlsx'

    # df = pd.read_excel("Hw1-words.xlsx", sheet_name='Proto-words')
    df = pd.read_excel(file_path, header=None, skiprows=4, usecols='C:R')
    maxRowsCount = df.shape[0]
    keys = (list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'))[:maxRowsCount]
    dfKeyed = df.copy()
    for col in df.columns:
        selectedCol = df[col]
        unique_values = selectedCol.unique()
        word2key = dict(zip(unique_values, keys))
        dfKeyed[col].replace(word2key, inplace=True)
    all_rows = []
    for index, row in dfKeyed.iterrows():
        words = []
        for value in row.values:
            words.append(value)
        all_rows.append(words)
    # mother = []
    # for row in all_rows:
    #     mother.append(row[1])
    consensus_sequence = find_consensus_sequence(all_rows)
    mutations_set = find_mutations_set(all_rows, consensus_sequence)
    common_mutation_matrix = find_initial_cm_matrix(mutations_set)
    # print("common_mutation_matrix")
    # print(common_mutation_matrix)
    language_family_tree_root = TreeNode('Root')
    titles = [f"S{i}" for i, t in enumerate(common_mutation_matrix[0])]
    common_mutation_matrix = find_cmm(common_mutation_matrix, language_family_tree_root, titles)
    print("common_mutation_matrix")
    print(common_mutation_matrix)
    print(language_family_tree_root)
if __name__ == "__main__":
    main()
