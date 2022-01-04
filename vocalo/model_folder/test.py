import psycopg2


# connect postgreSQL
users = 'jlsxzrphwsccaj'
dbnames = 'vocalorecomm'
conn = psycopg2.connect(" user=" + users +" dbname=" + dbnames)

# excexute sql
cur = conn.cursor()
cur.execute('SELECT * FROM items;')
results = cur.fetchall()

#output result
print(results)

cur.close()
conn.close()