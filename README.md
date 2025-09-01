# 👟 Walksy Shoe Store

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Backend-black?logo=flask)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange?logo=mysql&logoColor=white)
![Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-black?logo=vercel)
![License](https://img.shields.io/badge/License-MIT-green)

Walksy is a **Flask + MySQL powered e-commerce web application** for browsing, filtering, and purchasing shoes.  
It features authentication, admin management, a shopping cart, and order tracking — all deployed on **Vercel**.  

🔗 **Live Demo:** [Walksy Shoe Store](https://walksy-shoe-store.vercel.app/)

---

## ✨ Features

### 👤 User Features
- Browse shoes by **men’s / women’s categories**
- Filter products by **brand and category**
- View detailed product pages
- Add/remove items from **shopping cart**
- Update quantities in cart
- Place **orders** with address and payment method
- View **past orders**

### 🔐 Authentication
- User **signup / login / logout**
- Passwords hashed with **Flask-Bcrypt**
- Session-based authentication using **Flask-Login**

### 🛠️ Admin Features
- Add, edit, and delete products
- Manage users
- Manage orders
- View contact messages

---

## 🏗️ Tech Stack

- **Backend:** [Flask](https://flask.palletsprojects.com/) (Python)
- **Frontend:** Jinja2 Templates, HTML5, CSS3, Bootstrap
- **Database:** MySQL with SQLAlchemy ORM
- **Auth:** Flask-Login, Flask-Bcrypt
- **Deployment:** [Vercel](https://vercel.com/)
- **Environment Config:** `python-dotenv`

---

## 📂 Project Structure
walksy/ <br>
├── app.py      # Main Flask app <br>
├── models.py       # Database models <br>
├── requirements.txt      # Dependencies <br>
├── vercel.json        # Vercel config <br>
├── .env        # Local environment variables (ignored in Git) <br>
├── static/     # CSS, images, uploads <br>
│ └── style.css <br>
├── templates/      # HTML templates <br>
│ ├── base.html  <br>
│ ├── index.html <br>
│ ├── men.html <br>
│ ├── women.html <br>
│ ├── login.html <br>
│ ├── signup.html <br>
│ ├── cart.html <br>
│ ├── orders.html <br>
│ ├── shoe_details.html <br>
│ └── admin/ # Admin panel pages <br>


---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/walksy-shoe-store.git
cd walksy-shoe-store

python -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows

pip install -r requirements.txt

python app.py
```
Open http://localhost:5000

🚀 Deployment on Vercel
---
Push your project to GitHub

Import into Vercel

Add environment variables (SECRET_KEY, DB_USER, DB_PASS, DB_HOST, DB_NAME) in
Vercel → Project → Settings → Environment Variables

Deploy! 🎉

🧑‍💻 Author
---
Shivam Vadhiya – Full Stack Developer
---
