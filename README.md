# 🍽️ Restaurant Management System (CLI)

A **terminal-based Restaurant Management System** built using **Python** and **SQLite**, designed to manage restaurant operations such as menu handling, order processing, staff management, billing, and customer feedback.

---

## 📌 Features

### 👨‍💼 Manager
- View full menu
- Add staff (Chef / Waiter)
- View staff details
- View customers
- View customer feedback

### 👨‍🍳 Chef
- Add menu items
- View menu
- View incoming orders
- Accept orders
- Mark orders as cooked
- Update menu availability
- Add categories

### 🧑‍🍽️ Waiter
- View ready (cooked) orders
- Serve orders

### 👤 Customer
- Register & login
- View categorized menu
- Place orders
- Track order status
- View and redeem points
- Generate and pay bills
- Provide feedback

---

## 🛠️ Tech Stack

- **Language:** Python  
- **Database:** SQLite3  
- **Libraries Used:**
  - `sqlite3` – database management  
  - `tabulate` – formatted table display  
  - `datetime` – timestamp handling  

---

## 🗂️ Database Schema

### Tables:
- **users** → stores all users (manager, chef, waiter, customer)  
- **menu** → food items  
- **categories** → food categories  
- **orders** → customer orders  
- **feedback** → customer reviews  

---

## 🚀 How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/restaurant-management.git
   cd restaurant-management
