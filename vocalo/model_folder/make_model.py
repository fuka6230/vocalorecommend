import pandas as pd
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
import csv
import numpy as np
import pickle

df1_1 = np.loadtxt('spotify_1.csv', dtype = 'str', delimiter=',')
df1_1 = pd.DataFrame(data=df1_1)
df2_1 = np.loadtxt('spotify_playlist_1.csv', dtype = 'str', delimiter=',')
df2_1 = pd.DataFrame(data=df2_1)
df_all = pd.concat([df1_1, df2_1])
df_all = df_all.assign(artist_num=1)
for n in [2, 4, 6, 7, 8, 9]:
  df2 = np.genfromtxt('spotify_' + str(n) + '.csv', dtype = 'str', delimiter=',')
  df2 = pd.DataFrame(data=df2)
  df2_2 = np.genfromtxt('spotify_playlist_' + str(n) + '.csv', dtype = 'str', delimiter=',')
  df2_2 = pd.DataFrame(data=df2_2)
  df = pd.concat([df2, df2_2])
  df = df.assign(artist_num=n)
  df_all = pd.concat([df_all, df])

df_all.reset_index(inplace=True, drop=True)
df_all = df_all[df_all[5] != 'length']
df_all.to_csv('tracks_with_data.csv')

x = df_all.loc[1:, 5:18]
y = df_all.loc[1:, 'artist_num']
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from sklearn import preprocessing

from sklearn.ensemble import RandomForestClassifier


from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(bootstrap=True, ccp_alpha=0.0, class_weight='balanced',
                       criterion='gini', max_depth=9, max_features='auto',
                       max_leaf_nodes=None, max_samples=None,
                       min_impurity_decrease=0.0,
                       min_samples_leaf=1, min_samples_split=2,
                       min_weight_fraction_leaf=0.0, n_estimators=141,
                       n_jobs=None, oob_score=False, random_state=0, verbose=0,
                       warm_start=False)
model.fit(x, y)

f = open('final_model','wb')
pickle.dump(model,f)
f.close


