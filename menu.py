import sqlite3
from tabulate import tabulate

conn = sqlite3.connect('restaurants.db')
cursor = conn.cursor()


#user table
cursor.execute('''
create table if not exists users (
               id integer primary key autoincrement,
               username text not null,
               password text not null,
               phone text unique not null,
               role text not null,
               points integer default 0)
               ''')

#order table
cursor.execute('''
               create table if not exists orders (
               id integer primary key autoincrement,
               customer_id integer not null,
               menu_item_id integer not null,
               quantity integer not null,
               table_number integer not null,
               foreign key (customer_id) references users(id),
               foreign key (menu_item_id) references menu(id))  
               ''')

#menu table
cursor.execute('''
create table if not exists menu (
               id integer primary key autoincrement,
               item_name text not null,
               category text not null,
               price real not null,
               availability integer default 1)
               ''')


# manager insertion
cursor.execute('''
INSERT OR IGNORE INTO users (username, password, phone, role)
values ('manager1', 'man123', '1111111111', 'manager')
''')

# login function
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
            manager()
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


# manager function
def manager():
        while True:
            print("\nManager Menu\n")
            print("1. View Menu")
            print("2. View Orders")
            print("3.add staff")
            print("4.view staff")
            print("0. Logout")

            choice = input("\nenter your choice: ")
            if choice == "1":
                view_menu()
            elif choice == "2":
                view_orders()
            elif choice == "3":
                add_staff()
            elif choice == "4":
                view_staff()
            elif choice == "0":
                break
            else:
                print("invalid choice, please try again.")


# add staff function
def add_staff():
    try:
        username = input("enter staff username: ").strip()
        password = input("enter staff password: ").strip()
        phone = input("enter staff phone number: ").strip()
        role = input("enter staff role (cheif/waiter): ").strip().lower()
 
        if role not in ['cheif', 'waiter']:
            print("invalid role, must be 'cheif' or 'waiter'")
            return
        if not username or not password or not phone:
            print("all fields are required")
            return
        
        cursor.execute('''
        insert into users (username, password, phone, role)
        values (?, ?, ?, ?)''', (username, password, phone, role))
        conn.commit()
        print("\nstaff added successfully")
    except:
        print("failed to add staff, phone number may already exist")

#view staff function
def view_staff():
    cursor.execute('''
    select id, username, phone, role from users where role in ('cheif', 'waiter')
    ''')
    staff_members = cursor.fetchall()

    print("\nStaff Members:")
    headers = ["id", "username", "phone", "role"]
    print(tabulate(staff_members, headers, tablefmt="grid"))


#-----------------------------------------------------------------------------------------------   

# chef function
def cheif():
    while True:
        print("\nCheif Menu")
        print("1.add menu item")
        print("2.view menu")
        print("3.view orders")
        print("4.update menu")
        print("0.logout")

        choice = input("enter your choice: ")
        if choice == "1":
            add_menu()
        elif choice == "2":
            view_menu_available()
        elif choice == "3":
            view_orders()
        elif choice == "4":
            update_menu_item_availbility()
        elif choice == "0":
            break
        else:
            print("invalid choice, please try again.")

# menu adding function
def add_menu():
    while True:
        item_name = input("enter item name: ")
        category = input("enter category: ")
        price = float(input("enter price: "))
        availability = int(input("enter availability (1 for available, 0 for not available): "))
        cursor.execute('''
        insert into menu (item_name, category, price, availability)
        values (?, ?, ?, ?)''', (item_name, category, price, availability))
        conn.commit()
        print("menu item added successfully")

        choice = input("do you want to add another item? (y/n): ").lower()
        if choice != 'y':
            break

def view_menu_available():
    cursor.execute('''
    select id, item_name, category, price, availability from menu''')
    menu_items = cursor.fetchall()

    formatted_items = []
    for item in menu_items:
        availability_status = 'Available' if item[4] == 1 else 'Not Available'
        formatted_items.append((item[0], item[1], item[2], item[3], availability_status))

    print("\nMenu Items:")
    headers = ["id", "item_name", "category", "price", "availability"]
    print(tabulate(formatted_items, headers, tablefmt="grid"))

#update_menu_item_availbility
def update_menu_item_availbility():
    try:
        item_id = int(input("enter item id : "))
        availability = int(input("enter new availability (1 for available, 0 for not available): "))
        cursor.execute('''
        update menu set availability = ? where id = ?''', (availability, item_id))
        conn.commit()
        print("menu item availability updated successfully")
    except :
        print("failed to update menu item availability: ")

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
    headers = ["id", "username", "item_name", "quantity", "table_number"]
    print(tabulate(orders, headers, tablefmt="grid"))

#-----------------------------------------------------------------------------------------------

# customer function
def customer(customer_id):
    while True:
        print("\nCustomer Menu\n")
        print("1. View Menu")
        print("2. Place Order")
        print("3. View Points")
        print("4. View order")
        print("0. Logout")

        choice = input("\nenter your choice: ")

        if choice == "1":
            view_menu()
        elif choice == "2":
            place_order(customer_id)
        elif choice == "3":
            view_points(customer_id)
        elif choice == "4":
            view_order(customer_id)
        elif choice == "0":
            break
        else:
            print("invalid choice")

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

# view menu 
def view_menu():
    cursor.execute('''
    select id, item_name, category, price from menu''')
    menu_items = cursor.fetchall()

    print("\nMenu Items:")
    headers = ["id", "item_name", "category", "price"]
    print(tabulate(menu_items, headers, tablefmt="grid"))

# order placeing
def place_order(customer_id):

    table_number = int(input("\nEnter table number: "))
    try:
        menu_item_id = int(input("Enter menu item id: "))
        quantity = int(input("Enter quantity: "))
        cursor.execute('''
        insert into orders (customer_id, menu_item_id, quantity, table_number)
        values (?, ?, ?, ?)
        ''', (customer_id, menu_item_id, quantity, table_number))
        cursor.execute('''
        UPDATE users SET points = points + 10 WHERE id = ?
        ''', (customer_id,))
        conn.commit()
        print("\nitem added successfully")

        choice = input("do you want to place another order? (y/n): ").lower()
        if choice == 'y':
            place_order(customer_id)
        else:
            return
            
    except:
        print("invalid menu item id")

#view order
def view_order(customer_id):
    cursor.execute('''
    select o.id, m.item_name, o.quantity, o.table_number
    from orders o
    join menu m on o.menu_item_id = m.id
    where o.customer_id = ?
    ''', (customer_id,))
    orders = cursor.fetchall()

    print("\nYour Orders:")
    headers = ["id", "item_name", "quantity", "table_number"]
    print(tabulate(orders, headers, tablefmt="grid"))
    
#customer points view
def view_points(customer_id):
    cursor.execute('''
    SELECT points FROM users WHERE id = ?
    ''', (customer_id,))
    
    result = cursor.fetchone()
    
    if result:
        print(f"Your total points: {result[0]}")
    else:
        print("Unable to fetch points")

#----------main--------------------------------------------------------------
# main
while True:
    print("\nWelcome to the Restaurant Menu Management System\n")
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