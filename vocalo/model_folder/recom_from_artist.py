from vocalo.model_folder import recommend
import sqlite3
import pandas.io.sql as psql
import pandas as pd
import spotipy as sp
from spotipy.oauth2 import SpotifyClientCredentials
import time
import json
from sklearn import preprocessing
import tensorflow as tf
import pickle
from vocalo.model_folder import make_model
import numpy as np


with open('final_model.pickle', mode='rb') as f:
    model = pickle.load(f)

artists_dic = {1: 'ピノキオピー', 2: 'DECO*27', 4: '鬱P',6: 'おてつ！', 7: 'みきとP', 8: '40mP', 9: 'ナユタン星人'}

def artist_to_artist(artist):
    con = sqlite3.connect('Tracks.db')     
    cur = con.cursor()
    cur.execute('drop table items;')
    cur.execute(
      'CREATE TABLE items(artist_name text,track_id text,track_name text)'
    )
    df = pd.read_csv('all_tracks.csv')
    df = df.loc[:, 'artist_name':]
    df = df.drop_duplicates(subset='track_name')
    df.to_sql('vocalo_tracks', con, if_exists='replace', index=None)
    try:
      start_time2 = time.perf_counter()
      sr = psql.read_sql("SELECT * FROM vocalo_tracks where artist_name =:artist ;", con, params={'artist': artist})
      sr = sr.loc[:, 'track_id':'track_name']
    except KeyError:
      error = 'error'
      return error
    else:
        result_artists = {'ピノキオピー': 0, 'DECO*27': 0, '鬱P': 0 , 'おてつ！': 0, 'みきとP': 0, '40mP': 0, 'ナユタン星人': 0}
        for track_id in sr['track_id']:
            start_time3 = time.perf_counter()
            track = recommend.GetTrackFeatures(track_id)
            df = pd.DataFrame(track, index = ['name', 'album', 'artist', 'release_date', 'length', 'popularity', 'key', 'mode', 'danceability', 'acousticness', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'time_signature', 'valence'])
            df = df.T
            df = df.drop(['name', 'album', 'artist', 'release_date'], axis=1)
            x = df.loc[:, 'length': 'valence']  
            result = model.predict(x)
            result_artist = result[0]
            result_artist_name = artists_dic[result_artist]
            for k, v in result_artists.items():
                if k == result_artist_name:
                    result_artists[k] += 1
        max_k = max(result_artists.items(), key = lambda x:x[1])[0]
        return max_k



