# Milk Cart

An online milk shopping cart web app built with Django. Customers can browse dairy products, add them to a cart, checkout with delivery details, and view their order history with live status tracking.

## Features

- Product catalog with images
- Shopping cart (add / remove / quantity)
- Checkout with delivery address form
- **Order history page with status tracking** (Pending → Packed → On The Way → Delivered)
- Wishlist
- User signup / login / logout
- Admin panel for managing products, orders, customers, payments
- Bootstrap-based responsive UI

## Tech Stack

- **Backend:** Django 6.1, Python 3.13
- **Database:** SQLite (dev)
- **Frontend:** HTML, Bootstrap 5
- **Version control:** Git + GitHub

## Installation

```bash
git clone https://github.com/Pratikpatil456/milkcart.git
cd milkcart
pip install django pillow
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
