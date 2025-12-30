import sqlite3
from tabulate import tabulate
from datetime import datetime

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
               billed integer default 0,
               status text default 'pending',
               chef_id integer,
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

#customer feedback
cursor.execute('''
CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    comments TEXT,
    created_at TEXT,
    FOREIGN KEY (customer_id) REFERENCES users(id)
)
''')
conn.commit()



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
        elif role == 'chef':
            print(f"\nwelcome chef {username}")
            chef(id)
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
            print("2. Add staff")
            print("3. View staff")
            print("4. View customers")
            print("5. View feedback")
            print("0. Logout")

            choice = input("\nenter your choice: ")
            if choice == "1":
                view_menu()
            elif choice == "2":
                add_staff()
            elif choice == "3":
                view_staff()
            elif choice == "4":
                view_customers()
            elif choice == "5":
                view_feedback()
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
        role = input("enter staff role (chef/waiter): ").strip().lower()

        if role not in ['chef', 'waiter']:
            print("invalid role, must be 'chef' or 'waiter'")
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
    select id, username, phone, role from users where role in ('chef', 'waiter')
    ''' )
    staff_members = cursor.fetchall()

    print("\nStaff Members:")
    headers = ["id", "username", "phone", "role"]
    print(tabulate(staff_members, headers, tablefmt="grid"))

#view customers function
def view_customers():
    cursor.execute('''
    select id, username, phone, points from users where role = 'customer'
    ''')
    customers = cursor.fetchall()

    print("\nCustomers:")
    headers = ["id", "username", "phone", "points"]
    print(tabulate(customers, headers, tablefmt="grid"))

#view feedback function
def view_feedback():
    cursor.execute('''
    SELECT u.username, u.phone, f.rating, f.comments, f.created_at
    FROM feedback f
    JOIN users u ON f.customer_id = u.id
    ORDER BY f.created_at DESC
    ''')
    
    feedbacks = cursor.fetchall()

    if not feedbacks:
        print("No feedback available.")
        return

    headers = ["Customer Name", "Phone", "Rating", "Feedback", "Date"]
    print("\nCustomer Feedback:")
    print(tabulate(feedbacks, headers, tablefmt="grid"))





# chef function
def chef(chef_id):
    while True:
        print("\nChef Menu")
        print("1.add menu item")
        print("2.view menu")
        print("3.view orders")
        print("4.accept order")
        print("5.mark order as ready")
        print("6.update menu")
        print("0.logout")

        choice = input("\nenter your choice: ")
        if choice == "1":
            add_menu()
        elif choice == "2":
            view_menu_available()
        elif choice == "3":
            view_orders()
        elif choice == "4":
            chef_accepts_order(chef_id)
        elif choice == "5":
            chef_marks_order_ready(chef_id)
        elif choice == "6":
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

#view menu function
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
    join users u ON o.customer_id = u.id
    join menu m ON o.menu_item_id = m.id
    where o.status = 'pending' AND o.chef_id IS NULL and o.billed = 0
    ''')
    orders = cursor.fetchall()

    if not orders:
        print("No pending orders available.")
        return
    
    headers = ["Order ID", "Customer Name", "Item Name", "Quantity", "Table Number"]
    print(tabulate(orders, headers, tablefmt="grid"))


# chef accepts
def chef_accepts_order(chef_id):
    try:
        order_id = int(input("enter order id to accept: "))
        cursor.execute('''
        update orders set chef_id = ?, status = 'cooking' where id = ? and chef_id IS NULL
        ''', (chef_id, order_id))
        if cursor.rowcount == 0:
            print("order not found or already accepted by another chef.")
        else:
            conn.commit()
            print("order accepted successfully")
    except:
        print("failed to accept order")

#chef marks order as ready
def chef_marks_order_ready(chef_id):
    try:
        order_id = int(input("enter order id to mark as ready: "))
        cursor.execute('''
        update orders set status = 'cooked' where id = ? and chef_id = ?
        ''', (order_id, chef_id))
        if cursor.rowcount == 0:
            print("order not found or not assigned to you.")
        else:
            conn.commit()
            print("order marked as ready successfully")
    except:
        print("failed to mark order as ready")




# customer function
def customer(customer_id):
    while True:
        print("\nCustomer Menu\n")
        print("1. View Menu")
        print("2. Place Order")
        print("3. View Points")
        print("4. View order")
        print("5. view Bill")
        print("6. Pay Bill")
        print("7. Add Feedback")
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
        elif choice == "5":
            generate_bill(customer_id)
        elif choice == "6":
            pay_bill(customer_id)
        elif choice == "7":
            add_feedback(customer_id)
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
    select o.id, m.item_name, o.quantity, o.table_number, o.status
    from orders o
    join menu m on o.menu_item_id = m.id
    where o.customer_id = ?
    ''', (customer_id,))
    orders = cursor.fetchall()

    print("\nYour Orders:")
    headers = ["id", "item_name", "quantity", "table_number","status"]
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

#genarte bill
def generate_bill(customer_id):
    cursor.execute('''
    SELECT o.id, m.item_name, o.quantity, m.price,
           (o.quantity * m.price) as total_price
    FROM orders o
    JOIN menu m ON o.menu_item_id = m.id
    WHERE o.customer_id = ? AND o.billed = 0
    ''', (customer_id,))
    
    orders = cursor.fetchall()
    
    if not orders:
        print("No unbilled orders found for this customer.")
        return None, None
    
    print("\n----- Bill Details -----")
    headers = ["Order ID", "Item Name", "Quantity", "Unit Price", "Total Price"]
    print(tabulate(orders, headers, tablefmt="grid"))
    
    total_amount = sum(order[4] for order in orders)
    print(f"\nTotal Amount Due: ₹{total_amount:.2f}")
    
    order_ids = [order[0] for order in orders]
    return total_amount, order_ids

# pay bill function
def pay_bill(customer_id):
    total_amount, order_ids = generate_bill(customer_id)

    if not order_ids:
        return

    choice = input("\nDo you want to pay the bill? (y/n): ").lower()
    if choice != 'y':
        print("Payment not completed.")
        return

    payment_mode = input("Enter payment mode (Cash / Card / UPI): ").strip().lower()

    if payment_mode not in ["cash", "card", "upi"]:
        print("Invalid payment mode.")
        return

    cursor.execute(f'''
    UPDATE orders
    SET billed = 1
    WHERE id IN ({','.join('?' for _ in order_ids)})
    ''', order_ids)

    conn.commit()
    print(f"Payment successful via {payment_mode}.")
    print("Orders marked as billed.")

# feedback function
def add_feedback(customer_id):
    try:
        rating = int(input("Rate our service (1 to 5): "))
        if rating < 1 or rating > 5:
            print("Rating must be between 1 and 5")
            return

        comments = input("Enter your feedback: ").strip()
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute('''
        INSERT INTO feedback (customer_id, rating, comments, created_at)
        VALUES (?, ?, ?, ?)
        ''', (customer_id, rating, comments, created_at))

        conn.commit()
        print("Thank you for your feedback!")

    except ValueError:
        print("Invalid input")





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