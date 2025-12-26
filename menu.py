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
INSERT OR IGNORE INTO users (username, password, phone, role)
values ('manager1', 'man123', '1111111111', 'manager')
''')

#cheif insertion
cursor.execute('''
INSERT OR IGNORE INTO users (username, password, phone, role)
values ('cheif1', 'cheif123', '2222222222', 'cheif')
''')

#waiter insertion
cursor.execute('''
INSERT OR IGNORE INTO users (username, password, phone, role)
values ('waiter1', 'waiter123', '3333333333', 'waiter')
''')

def login():
    phone = input ("enter phone number: ")
    password = input("enter password: ")
    cursor.execute('''
    select id,username,role from users where phone = ? and password = ?''', (phone, password))

    user = cursor.fetchone()

    if user:
        id,username,role = user
        if role == 'manager':
            print(f"\nwelcome manager {username}")
        elif role == 'cheif':
            print(f"\nwelcome cheif {username}")
            cheif()
        elif role == 'waiter':
            print(f"\nwelcome waiter {username}")
        else:
            print(f"\nwelcome {username}")
            customer(id)
    else:
        print("invalid phone number or password")

# customer registration
def customer_registration():
    try:
        username = input("enter username: ")
        password = input("enter password: ")
        phone = input("enter phone number: ")

        cursor.execute('''
        insert into users (username, password, phone, role)
        values (?, ?, ?, 'customer')''', (username, password, phone))
        conn.commit()
        print("registration successful")
    
    except:
        print("registration failed, phone number may already exist")

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

# view menu function
def view_menu():
    cursor.execute('''
    select id, item_name, category, price, availability from menu''')
    menu_items = cursor.fetchall()

    print("\nMenu Items:")
    for item in menu_items:
        id, item_name, category, price, availability = item
        availability_status = "Available" if availability == 1 else "Not Available"
        print(f"ID: {id}, Name: {item_name}, Category: {category}, Price: {price}, Availability: {availability_status}")

#order table
cursor.execute('''
               create table if not exists orders (
               id integer primary key autoincrement,
               customer_id integer not null,
               menu_item_id integer not null,
               quantity integer not null,
               table_number integer not null,
               foreign key (customer_id) references users(id),
               foreign key (menu_item_id) references menu(id))  ''')
# order placeing
def place_order(customer_id):
    menu_item_id = int(input("Enter menu item id: "))
    quantity = int(input("Enter quantity: "))
    table_number = int(input("Enter table number: "))

    cursor.execute('''
    insert into orders (customer_id, menu_item_id, quantity, table_number)
    values (?, ?, ?, ?)
    ''', (customer_id, menu_item_id, quantity, table_number))

    conn.commit()
    print("Order placed successfully")

#view order
def view_orders():
    cursor.execute('''
    select o.id, u.username, m.item_name, o.quantity, o.table_number
    from orders o
    join users u on o.customer_id = u.id
    join menu m on o.menu_item_id = m.id
    ''')
    orders = cursor.fetchall()

    print("\nOrders:")
    for order in orders:
        id, username, item_name, quantity, table_number = order
        print(f" Item: {item_name}, Quantity: {quantity}, Table Number: {table_number}")

# chef function
def cheif():
    while True:
        print("\n1.add menu item")
        print("2.view menu")
        print("3.view orders")
        print("0.logout")

        choice = input("enter your choice: ")
        if choice == "1":
            add_menu()
        elif choice == "2":
            view_menu()
        elif choice == "3":
            view_orders()
        elif choice == "0":
            break
        else:
            print("invalid choice, please try again.")

# customer function
def customer(customer_id):
    while True:
        print("\n1. View Menu")
        print("2. Place Order")
        print("0. Logout")

        choice = input("enter your choice: ")

        if choice == "1":
            view_menu()
        elif choice == "2":
            place_order(customer_id)
        elif choice == "0":
            break
        else:
            print("invalid choice")


# main
while True:
    print("\nWelcome to the Restaurant Menu Management System")
    print("1. user registration")
    print("2. login")
    print("0. Exit")

    choice = input("enter your choice: ")

    if choice == "1":
        customer_registration()
    elif choice == "2":
        login()
    elif choice == "0":
        break
    else:
        print("invalid choice, please try again.")
conn.close()