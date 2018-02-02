# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 16:30:42 2017

@author: SRINIVAS RAO
"""
import pandas as pd
def decision_tree_algo(filename):
    '''Input a file and outputs the first left node and right node of a decision tree, 
     the code is written for only splitting on numerical veriables'''
     
    df = pd.read_csv(filename, sep =',') # change this method according to file format
    dict_goodnes = {} # for storing the values of goodness of nodes for their respective rows and columns
    for col in df.columns: # iterating on columns
        if ((df[col].dtype == 'int64') or (df[col].dtype == 'float64')) and col != df.columns[-1]: # checking if the column is of data type integer or float and excludes the predicted column
            for row_index in range(0, len(df)): #iterating on each row of every column and splitting on each row
                left_node = df[df[col] <= df.loc[row_index, col]]
                right_node = df[df[col] > df.loc[row_index, col]]
                if len(left_node) !=0  and len(right_node) !=0: #checking if the length of nodes is greater tna zero

                    #calucalting the Goodness of parent node
                    score_of_left_node = float(sum(map(lambda x: x**2, list(left_node[df.columns[-1]].value_counts()))))/float((len(left_node)**2)) #caluculating score of left node
                    #print('score_of_left_node', score_of_left_node)
                    score_of_right_node =float(sum(map(lambda x: x**2, list(right_node[df.columns[-1]].value_counts()))))/float((len(right_node)**2)) #caluculating the score of right node
                    #print('score_of_right_node', score_of_right_node)
                    Goodness_of_node = ((float(len(left_node))/float(len(df)))*score_of_left_node) + ((float(len(right_node))/float(len(df)))*score_of_right_node) #caluculating the Goodness of parent node
                    #print('Goodness_of_node', Goodness_of_node)
                    dict_goodnes[(row_index, df.loc[row_index, col], col)] = Goodness_of_node # finally storing the Goodness of all nodes in a dictionary
        else:
            break;
    key_max_goodness_node = max(dict_goodnes, key= dict_goodnes.get) #a tuping with best split row index, row value and column name
    final_left_node = df[df[key_max_goodness_node[2]] <= df.loc[key_max_goodness_node[0], key_max_goodness_node[2]]]
    final_left_node = final_left_node.sort_values(by = key_max_goodness_node[2]) #sorting the final left node
    final_right_node = df[df[key_max_goodness_node[2]] > df.loc[key_max_goodness_node[0], key_max_goodness_node[2]]]
    final_right_node = final_right_node.sort_values(by = key_max_goodness_node[2]) #sorting the final right node
    split_value = (final_left_node.tail(1)[key_max_goodness_node[2]].values[0] + final_right_node.head(1)[key_max_goodness_node[2]].values[0])/2
    print('split on column {0} with split value as {1} and on row with row-index {2}\n'.format(key_max_goodness_node[2], split_value, key_max_goodness_node[0]))
    print('first_left_node\n')
    print(final_left_node)
    print("")
    print('first_right_node\n')
    print(final_right_node)
    return final_left_node, final_right_node