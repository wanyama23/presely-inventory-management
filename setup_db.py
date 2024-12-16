import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('inventory.db')

# Create a cursor object
cursor = conn.cursor()

# Create the inventory table
cursor.execute('''
CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
