import pypyodbc

db_file = r'D:\acdb.accdb'
user = ''
password = ''
con_str = 'DRIVER={Microsoft Access Driver (*.accdb)};'+'DBQ={};UID={};PWD={};'.format(db_file,user,password)
conn = pypyodbc.win_connect_mdb(con_str)
sql = 'select * from acdb;'
cur = conn.cursor()
cur.execute(sql)
print(cur.fetchall())
print([column[0] for column in cur.description])
