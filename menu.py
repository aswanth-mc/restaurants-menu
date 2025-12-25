import sqlite3

conn = sqlite3.connect("restaurant.db")
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

#users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
)
''')

#default admin user
cursor.execute('''
INSERT OR IGNORE INTO users (username, password, role)
VALUES ('admin', 'admin123', 'admin')
''')
conn.commit()

#function to register a new user
def register_user():
    username = input("Enter username: ")
    password = input("Enter password: ")
    cursor.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, 'user')",
        (username, password)
    )
    conn.commit()
    print("User registered successfully")


#menu table
cursor.execute('''
CREATE TABLE IF NOT EXISTS menu (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT,
    price REAL
)
''')
#orders table
cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    item_id INTEGER,
    quantity INTEGER,
    total_price REAL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (item_id) REFERENCES menu(item_id)
)
''')
conn.commit()





while True:
    print("\nRestaurant Management System")
    print("1. Register (User)")


    choice = input("Choice: ")

    if choice == "1":
        register_user()
    else:
        print("Invalid choice. Please try again.")

conn.close()