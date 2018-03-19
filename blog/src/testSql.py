import sqlite3


database_name = 'follows_db.db'
follows_db = sqlite3.connect(database_name, timeout=0, isolation_level=None)
follows_db_c = follows_db.cursor()
fdfd=1