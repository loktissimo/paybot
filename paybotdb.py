# -*- coding: utf-8 -*-
import sqlite3

conn = sqlite3.connect('paybot.db')

c = conn.cursor()

c.execute('SELECT * FROM users')
print(c.fetchall())
c.execute('SELECT * FROM posts')
print(c.fetchall())

conn.close()