## 👇👇👇👇👇 Project link 👇👇👇👇👇

https://kitchen-service-m5u6.onrender.com/


## To login as admin user use:
  Login: Max
  
  Password: 2001november24



# Restaurant Kitchen Service 🍽️

A web application for managing dishes, ingredients, dish types, and cooks. Built with Django.

## 👥 Functionality Overview

### 🔓 Guest (Unauthenticated User)

- Can view the login/register page .
- Can't view the homepage.
- Cannot access dish, ingredient, dish type, or cook lists.

---

### 👤 Authenticated User (Regular User (Cook))

- Can:
  - View a list of dishes and search by name.
  - View detailed pages for each dish.
  - Assign or unassign themselves to/from a dish (become a cook of the dish).
  - View a list of cooks.
  - View cook profiles and edit their own.
- Cannot:
  - View, create, update, or delete ingredients, dish types, or other cooks.
  - Create, update, or delete dishes.

---

### 👑 Administrator (Superuser)

Has full access to all features, including:

- Managing all dishes:
  - Create, update, delete.
  - Assign multiple cooks to a dish.
- Managing ingredients:
  - View, create, update, delete.
- Managing dish types:
  - View, create, update, delete.
- Managing cooks:
  - View, create, update, delete.
  - View detailed cook profiles and unassign them from dishes.


## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- SQlite3
- Python-dotenv (for dependency management)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/Odin-max/kitchen_service.git
cd restaurant_kitchen_service
```

2. **Configure environment variables**

Create a `.env` file in the root folder:

```env
SECRET_KEY=your-secret-key
DEBUG=True
```

3. **Install dependencies**

```bash
poetry install
```

4. **Apply migrations**

```bash
poetry run python manage.py migrate
```

5. **Create superuser**

```bash
poetry run python manage.py createsuperuser
```

6. **Run the development server**

```bash
poetry run python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to start using the app.

## ✅ Running Tests

```bash
poetry run python manage.py test
```

---
