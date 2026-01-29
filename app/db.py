import sqlite3

con = sqlite3.connect("notes.db")

cur = con.cursor()

#cur.execute("CREATE TABLE Users( id INTEGER PRIMARY KEY AUTOINCREMENT," \
#"username TEXT NOT NULL UNIQUE," \
#"email TEXT UNIQUE," \
#"password_hash TEXT NOT NULL," \
#"created_at DATETIME DEFAULT CURRENT_TIMESTAMP)")

cur.execute("CREATE TABLE notes ( id INTEGER PRIMARY KEY AUTOINCREMENT, " \
"user_id INTEGER NOT NULL," \
"title TEXT NOT NULL," \
"context TEXT," \
"created_at DATETIME DEFAULT CURRENT_TIMESTAMP," \
"updated_at DATETIME DEFAULT CURRENT_TIMESTAMP," \
"is_archived BOOLEAN DEFAULT 0," \
"FOREIGN KEY (user_id) REFERENCES users(id))")

res = cur.execute("SELECT name FROM sqlite_master")

print(res.fetchone())
