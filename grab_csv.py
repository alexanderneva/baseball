from pybaseball import batting_stats, pitching_stats
import pandas as pd
import numpy as np


data_p = pd.read_csv("my_data.csv")
print(data_p.columns.values)
print(data_p.head())
print(data_p.shape)
# with open('pitching.txt','w') as file:
#    for i in data_p.columns.values:
#        file.write(i+'\n')
