# Samaniya VoucherHub Backend API (Django + DRF)

This backend is now implemented using:
- **Django**
- **Django REST Framework**
- **Serializer-based APIs**
- **SQLite** (default, easy local setup)

It matches your frontend needs:
- OTP login
- voucher listing/filtering
- cart operations
- checkout/order
- FAQ/testimonials/contact

## Project structure

```txt
backend/
  manage.py
  db.sqlite3
  requirements.txt
  config/
    settings.py
    urls.py
  apps/
    api/
      models.py
      serializers.py
      views.py
      urls.py
      management/commands/seed_data.py
```

## Start server

From project root:

1. Activate virtual env
```bash
source .venv/bin/activate
```

2. Go to backend
```bash
cd backend
```

3. Install requirements
```bash
pip install -r requirements.txt
```

4. Run migrations
```bash
python manage.py migrate
```

5. Seed sample data
```bash
python manage.py seed_data
```

6. Start server
```bash
python manage.py runserver
```

Open the **full website** (HTML + CSS + JS + API same origin — recommended):

- **Site:** `http://127.0.0.1:8000/`
- **API health:** `http://127.0.0.1:8000/api/health`

Django serves files from the `frontend/` folder automatically, so **do not open HTML with `file://`** — that breaks API calls.

Optional: run `python3 -m http.server` inside `frontend/` only if you set `localStorage.vh_api_base` to `http://127.0.0.1:8000/api`.

## API Endpoints

### Auth
- `POST /api/v1/auth/request-otp`
- `POST /api/v1/auth/verify-otp`

Compatibility endpoints:
- `POST /api/auth/request-otp`
- `POST /api/auth/verify-otp`

### Vouchers
- `GET /api/v1/vouchers?category=shopping&search=amazon`
- `GET /api/v1/vouchers/<voucher_id>`

### Cart
- `GET /api/v1/cart/<user_id>`
- `POST /api/v1/cart/<user_id>/items`
- `PATCH /api/v1/cart/<user_id>/items/<voucher_id>`
- `DELETE /api/v1/cart/<user_id>/remove/<voucher_id>`
- `DELETE /api/v1/cart/<user_id>/clear`

### Orders
- `POST /api/v1/orders/checkout`
- `GET /api/v1/orders/<order_id>`
- `GET /api/v1/orders/user/<user_id>`

### Content
- `GET /api/v1/content/faq`
- `GET /api/v1/content/testimonials`
- `POST /api/v1/content/contact`

## OTP for local development

- Development OTP is `123456`.
- For production, integrate an SMS provider (Twilio/Fast2SMS/etc) in `api/views.py`.
