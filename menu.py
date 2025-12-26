import sqlite3

conn = sqlite3.connect('restaurants.db')
cursor = conn.cursor()

cursor.execute('''
create table if not exists users (
               id integer primary key autoincrement,
               username text not null,
               password text not null,
               phone text unique not null,
               role text not null )
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