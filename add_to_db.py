import sqlite3
import pandas as pd
import pandas.io.sql as psql
import sqlite3
 
# sqlite3に接続
con = sqlite3.connect('Tracks.db')
cur = con.cursor()
 
df = pd.read_csv('tracks_db.csv')
df = df.loc[:, 'artist_name':]
df.to_sql('vocalo_tracks', con, if_exists='append', index=None)