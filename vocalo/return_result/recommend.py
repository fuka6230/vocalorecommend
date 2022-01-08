import pandas as pd
import spotipy as sp
from spotipy.oauth2 import SpotifyClientCredentials
import time
import json
from sklearn import preprocessing
import tensorflow as tf
import pickle
import numpy as np
import pandas.io.sql as psql
import os
import psycopg2

client_id = '18c6546b047443ce9e724ec60d89356b'
client_secret = '6107b869cacd421bb4db8762c51d19c6'
client_credentials_manager = sp.oauth2.SpotifyClientCredentials(client_id, client_secret)
sp = sp.Spotify(client_credentials_manager=client_credentials_manager)


def GetTrackIdsFromAlbum(album_ids):
  """
  アルバムのidからトラックのidを取得
  """
  track_ids = []
  for album_id in album_ids:
    album_tracks = sp.album_tracks(album_id, limit=50, offset=0, market=None)
    track_id = album_tracks['items'][0]['id']
    track_ids.append(track_id)

  return track_ids


def GetTrackFeatures(track_id):
  """
  トラックのidからメタデータを取得
  """
  meta = sp.track(track_id)
  features = sp.audio_features(track_id)

  name = meta['name']
  album = meta['album']['name']
  artist = meta['album']['artists'][0]['name']
  release_date = meta['album']['release_date']
  length = meta['duration_ms']
  popularity = meta['popularity']
  key = features[0]['key']
  mode = features[0]['mode']
  danceability = features[0]['danceability']
  acousticness = features[0]['acousticness']
  energy = features[0]['energy']
  instrumentalness = features[0]['instrumentalness']
  liveness = features[0]['liveness']
  loudness = features[0]['loudness']
  speechiness = features[0]['speechiness']
  tempo = features[0]['tempo']
  time_signature = features[0]['time_signature']
  valence = features[0]['valence']

  track = [name, album, artist, release_date, length, popularity, key, mode, danceability, acousticness, energy, instrumentalness, liveness, loudness, speechiness, tempo, time_signature, valence]
  return track

artists_dic = {1: 'ピノキオピー', 2: 'DECO*27', 4: '鬱P',6: 'おてつ！', 7: 'みきとP', 8: '40mP', 9: 'ナユタン星人'}

def GetAlbumIds(artist_id):
  """
  アーティストのidからアルバムのidを取得
  """
  results = sp.artist_albums(artist_id, album_type=None, country=None, limit=20, offset=0)
  albums = results['items']
  while results['next']:
    results = sp.next(results)
    albums.extend(results['items'])

  album_ids = []

  for album in albums:
    album_ids.append(album['id'])

  return album_ids


def title_to_artist(track_name):
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')  

    try:
      sr = psql.read_sql("SELECT * FROM items where track_name =%(track_name)s ;", conn, params={'track_name': track_name})
      sr = sr.loc[0, :]
    except KeyError:
      conn.close()
      error = 'error'
      return error
    else:
      conn.close()
      track_id = sr[1]
      track = GetTrackFeatures(track_id)
      df = pd.DataFrame(track, index = ['name', 'album', 'artist', 'release_date', 'length', 'popularity', 'key', 'mode', 'danceability', 'acousticness', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'time_signature', 'valence'])
      df = df.T
      df = df.drop(['name', 'album', 'artist', 'release_date'], axis=1)
      x = df.loc[:, 'length': 'valence']
      with open('final_model.pickle', mode='rb') as f:  
        model = pickle.load(f)  
      result = model.predict(x)
      result_artist = result[0]
      return artists_dic[result_artist]





