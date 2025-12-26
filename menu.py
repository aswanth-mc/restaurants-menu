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

def login():
    phone = input ("enter phone number: ")
    password = input("enter password: ")
    cursor.execute('''
    select username,role from users where phone = ? and password = ?''', (phone, password))

    user = cursor.fetchone()

    if user:
        username,role = user
        if role == 'manager':
            print(f"\nwelcome manager {username}")
        elif role == 'cheif':
            print(f"welcome cheif {username}")
            chef()
        elif role == 'waiter':
            print(f"welcome waiter {username}")
        else:
            print(f"welcome {username}")
    else:
        print("invalid phone number or password")

#menu table
cursor.execute('''
               create table if not exists menu (
               id integer primary key autoincrement,
                item_name text not null,
               category text not null,
               price real not null ,
                availability integer not null default 1)
                ''')

# menu adding function
def add_menu():
    item_name = input("enter item name: ")
    category = input("enter category: ")
    price = float(input("enter price: "))
    availability = int(input("enter availability (1 for available, 0 for not available): "))

    cursor.execute('''
    insert into menu (item_name, category, price, availability)
    values (?, ?, ?, ?)''', (item_name, category, price, availability))
    conn.commit()
    print("menu item added successfully")



# chef fuction
def chef():
    while True:
        print("1.add menu item")
        print("0.logout")

        choice = input("enter your choice: ")
        if choice == "1":
            add_menu()
        elif choice == "0":
            break
        else:
            print("invalid choice, please try again.")


while True:
    print("\nWelcome to the Restaurant Menu Management System")
    print("1. user registration")
    print("2. login")
    print("0. Exit")

    choice = input("enter your choice: ")

    if choice == "1":
        print("user registration")
    elif choice == "2":
        login()
    elif choice == "0":
        break
    else:
        print("invalid choice, please try again.")
conn.close()