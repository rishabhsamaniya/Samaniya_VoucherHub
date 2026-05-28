# 🎫 Samaniya VoucherHub

> India's premier, high-performance digital voucher and e-commerce platform. Built with a robust **Django + DRF** backend and a stunning **Glassmorphism Vanilla CSS & JavaScript** frontend.

---

## ✨ Features

- 🌟 **Premium 3D Flipped Auth:** Sleek and fluid 3D card rotation between sign-in and sign-up with real-time feedback.
- 🛒 **Instant Cart & Dynamic Badges:** Interactive cart state management synced across all pages with custom quantity controls.
- 💳 **Secure Checkout Flow:** Supports UPI, cards, Net Banking, and automatically triggers unique secure voucher code generation.
- 🗺️ **State-of-the-Art State & Pincode Lookup:** Fast lookup APIs using local Indian geographic datasets.
- 🚀 **WhiteNoise Integration:** High-performance static files serving with gzip/brotli compression ready for cloud deployment.
- 🛡️ **JWT-like Token Auth:** Robust Bearer-token authentication for stateful APIs.

---

## 🛠️ Technical Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Backend Framework** | Django 4.2.x | Secure, fast, and structured relational server. |
| **API Architecture** | Django REST Framework (DRF) | Stateless serializer-based JSON API endpoints. |
| **Database** | PostgreSQL (Production) / SQLite (Local) | Seamless transition using `dj-database-url`. |
| **Frontend UI** | HTML5, CSS3, ES6+ JS | Glassmorphic aesthetics, custom 3D animations, zero third-party framework weight. |
| **Static Server** | WhiteNoise | Optimized static file compressing/caching engine. |

---

## 💻 Local Setup & Installation

### 1. Prerequisite
Ensure you have **Python 3.9+** installed.

### 2. Setup the Environment
From the project root:

```bash
# 1. Activate the Python virtual environment
source .venv/bin/activate

# 2. Go to the backend directory
cd backend

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply database migrations
python manage.py migrate

# 5. Run the server
python manage.py runserver
```

### 3. Open the App
* Visit **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in your web browser.
* *Note:* Use development OTP **`123456`** for registration and forgot-password flows.

---

## 🚀 Free Deployment Guide (Render + Neon PostgreSQL)

This project is pre-configured to be deployed on **Render** (Free Web Service) linked to **Neon.tech** or **Supabase** (Free PostgreSQL).

### Step 1: Create a PostgreSQL Database
1. Go to [Neon.tech](https://neon.tech/) and create a free project.
2. Copy the **Connection String** (looks like: `postgres://user:password@host/dbname`).

### Step 2: Set up Render Web Service
1. Create a free account on [Render.com](https://render.com/) and connect your GitHub account.
2. Click **New +** -> **Web Service** and connect this repository.
3. Configure the following parameters:
   - **Environment:** `Python`
   - **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate`
   - **Start Command:** `gunicorn config.wsgi:application`
4. Add the following **Environment Variables** in the **Environment** tab:
   - `DATABASE_URL`: `[Your Neon database connection string]`
   - `PYTHON_VERSION`: `3.9.18` (or your Python version)

Click **Deploy Web Service** and Render will compile, migrate, compress static files, and serve **Samaniya VoucherHub** live!
