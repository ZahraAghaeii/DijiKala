﻿# 🛍️ Mini DijiKala 

A simple **multi-vendor marketplace** developed using **Django** as the final project for the **Daneshkar Django Bootcamp (Level 5)**.

The platform allows sellers to create and manage their own stores and products, while customers can browse stores, add products to their shopping cart, manage their wallet balance, and complete purchases through a simulated checkout process.

---

# ✨ Features

### 👤 Authentication & Authorization
* User registration and role selection (Customer / Seller)
* Secure login and logout system
* Role-based access control (Decorator-protected views)
* Full integration with Django Admin Panel

### 🏪 Store Management
* Sellers can create personal stores with custom names and descriptions
* Dedicated store detail pages showcasing specific products
* Seller dashboard for managing store inventories

### 📦 Product Management
* Sellers can add products with custom images, names, and pricing
* Product images dynamically handled via media configurations
* Store-isolated product display and custom access checks

### 🛍️ Shopping Experience
* Browse all available stores and overall products from the home page
* Interactive shopping cart system
* Add and remove items from the cart dynamically

### 💳 Demo Payment System
* Simulated customer wallet balance
* Balance top-up and instant synchronization
* Checkout validation checking customer assets against order pricing
* Automated fund deductions from customer wallet and dynamic transfer to store accounts

### 📜 Order History
* Post-checkout order item tracking
* Complete historical database record of consumer invoice entities
---

## 🏗️ System Architecture

### User Roles

#### Administrator
* Full data access through the Django Admin Panel
* Manage database entities including users, profiles, stores, products, and invoices

#### Seller
* Establish and operate custom stores
* List and manage unique inventory items
* Access the specialized seller panel

#### Customer
* Explore marketplace stores and product catalogs
* Populate and manage shopping cart items
* Top up wallet balance and execute secure checkouts
* Review personal order history logs

---

# 📂 Project Structure

```text
DijiKala/
│
├── DijiKala/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── marketplace/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
│
├── static/
│   └── css/
│       └── style.css
│
├── templates/
│   ├── registration/
│   │   ├── logged_out.html
│   │   ├── login.html
│   │   └── signup.html
│   ├── base.html
│   ├── cart.html
│   ├── customer_panel.html
│   ├── home.html
│   ├── order_history.html
│   ├── payment.html
│   ├── seller_panel.html
│   ├── store_detail.html
│   └── stores.html
│
├── manage.py
├── requirements.txt
└── README.md
```

---

# 🛠️ Database Models

| Model | Description |
|--------|-------------|
| **User** | Django built-in authentication model |
| **CustomerProfile** | Stores customer information and wallet balance |
| **SellerProfile** | Profile associated with seller accounts |
| **Store** | Marketplace stores owned by sellers |
| **Product** | Products belonging to each store |
| **CartItem** | Shopping cart items |
| **Order** | Completed purchase records |
| **OrderItem** | Individual products within an order |

---

## 📄 Pages

| URL | Description | VIEW / METHOD |
| :--- | :--- | :--- |
| `/` | Landing page with latest stores/products | `home` -> GET |
| `/stores/` | List of all registered stores | `stores_list` -> GET |
| `/stores/<id>/` | Store catalog, product overview | `store_detail` -> GET |
| `/seller/` | Seller administration panel | `seller_panel` -> GET |
| `/seller/create-store/` | Create a new merchant store | `create_store_view` -> POST |
| `/seller/add-product/<store_id>/` | Append products to owned store | `add_product_view` -> POST |
| `/customer/` | Customer details and overview panel | `customer_panel` -> GET |
| `/customer/orders/` | Historical purchase log archive | `order_history_view` -> GET |
| `/cart/` | Core user shopping cart page | `cart` -> GET |
| `/payment/` | Top-up and fund processing screen | `payment` -> GET |
| `/deposit-wallet/` | Add cash and increase wallet balance | `deposit_wallet_view` -> POST |
| `/checkout/` | Order verification and fund settlement | `checkout_view` -> GET/POST |
| `/accounts/login/` | User authentication entrance | `login` -> GET, POST |
| `/accounts/signup/` | Registration view and role assignment | `signup_view` -> GET, POST |

---

# 🚀 Installation

## 1. Clone the repository

```bash
git clone https://github.com/ZahraAghaeii/DijiKala.git
cd DijiKala
```

---

## 2. Create a virtual environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Apply database migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 5. Create an administrator account

```bash
python manage.py createsuperuser
```

---

## 6. Run the development server

```bash
python manage.py runserver
```

Open your browser and visit:

```
http://127.0.0.1:8000/
```

---

# 💻 Technologies Used

- Python
- Django
- SQLite3
- HTML5
- CSS3

---
# 📷 Screenshots

* Home Page
  <img width="1500" height="937" alt="Screenshot (15) png" src="https://github.com/user-attachments/assets/f17c95fd-2592-4fae-8b3f-a4ab62f67e5a" />

* Sign up Page
  <img width="1500" height="937" alt="Screenshot (16) png" src="https://github.com/user-attachments/assets/b7f262f4-030c-45ca-9108-dd884ab00f09" />

* Login page
  <img width="1500" height="937" alt="Screenshot (17) png" src="https://github.com/user-attachments/assets/0f757829-c103-4778-95f4-df1aabe75e1f" />

* Order history
  <img width="1500" height="937" alt="Screenshot (20) png" src="https://github.com/user-attachments/assets/24002cc8-15ed-4cdc-a4da-679961491967" />

* Cart Page
  <img width="1500" height="937" alt="Screenshot (18) png" src="https://github.com/user-attachments/assets/5ac52efb-6353-497d-bee8-bb1dcf117cbc" />

* Customer panel
  <img width="1500" height="937" alt="Screenshot (19) png" src="https://github.com/user-attachments/assets/bbecc435-f25d-4712-8e32-3988577391e8" />


---
# 📌 Main Functionalities

- Multi-vendor marketplace
- Authentication system
- Role-based authorization
- Seller dashboard
- Customer dashboard
- Shopping cart
- Wallet payment system
- Order history
- Django Admin Panel
- Responsive user interface

---

# 👩‍💻 Developers

### Zahra Aghaei
GitHub: https://github.com/ZahraAghaeii

### Ghazal Taherkhani
GitHub: https://github.com/ghazaltaherkhani82

---

# 📚 Course

This project was developed as the final project of the **Daneshkar Django Bootcamp (Django Track)**.

---

# 📄 License

This project was developed for educational purposes as part of the Daneshkar Django Bootcamp.
