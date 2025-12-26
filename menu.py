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
    role TEXT,
    phone TEXT
)
''')

#cursor.execute('alter table users add column phone text')

#default admin user
cursor.execute('''
INSERT OR IGNORE INTO users (username, password, role)
VALUES ('admin', 'admin123', 'admin')
''')
conn.commit()

# register a new user
def register_user():
    username = input("Enter username: ")
    password = input("Enter password: ")
    phone = input("Enter phone number: ")

    try:
        cursor.execute('''
        INSERT INTO users (username, password, role, phone)
        VALUES (?, ?, 'customer', ?)
        ''', (username, password, phone))
        conn.commit()
        print("User registered successfully.")
    except:
        print("username already exists")
        return register_user()

# login 
def login():
    phno = input ("enter phone number: ")
    password = input ("enter password: ")

    cursor.execute('''
                   select * from users
                   where phone = ? and password = ?
                     ''', (phno, password))
    user = cursor.fetchone()
    if user:
        print("Login successful.")
        return user


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

#place order





while True:
    print("\nRestaurant Management System")
    print("1. Register (User)")
    print("2. Login")


    choice = input("Choice: ")

    if choice == "1":
        register_user()
    elif choice == "2":
        user = login()
        if user:
            user_id, username, password, role, phone = user
            if role == "admin":
                print("Admin functionalities can be implemented here.")
            else:
                print(f"Customer functionalities can be implemented here {username}.")
    else:
        print("Invalid choice. Please try again.")

conn.close()