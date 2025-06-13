import sqlite3

conn = sqlite3.connect('users.db')
conn.execute('CREATE TABLE IF NOT EXISTS logins (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
conn.commit()
conn.close()
