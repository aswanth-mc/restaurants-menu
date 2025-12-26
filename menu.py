import sqlite3

conn = sqlite3.connect('restaurants.db')
cursor = conn.cursor()

#user table
cursor.execute('''
create table if not exists users (
               id integer primary key autoincrement,
               username text not null,
               password text not null,
               phone text unique not null,
               role text not null )
               ''')

# manager insertion
cursor.execute('''
insert into users (username, password, phone, role)
values ('manager1', 'man123', '1234567890', 'manager')
''')

#cheif insertion
cursor.execute('''
insert into users (username, password, phone, role)
values ('cheif1', 'cheif123', '0987654321', 'cheif')
''')

#waiter insertion
cursor.execute('''
insert into users (username, password, phone, role)
values ('waiter1', 'waiter123', '1122334455', 'waiter')
''')

while True:
    print("\nWelcome to the Restaurant Menu Management System")
    print("1. user registration")
    print("0. Exit")

    choice = input("enter your choice: ")

    if choice == "1":
        print("user registration")
    elif choice == "0":
        break
    else:
        print("invalid choice, please try again.")
conn.close()