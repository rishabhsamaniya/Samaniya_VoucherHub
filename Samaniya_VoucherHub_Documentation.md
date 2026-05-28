# Samaniya VoucherHub - Project Documentation

## 1. Project Overview
Samaniya VoucherHub is a modern, premium e-commerce platform designed for selling digital vouchers. It features a high-performance interactive frontend with 3D animations and a robust, secure Django-based backend with real-time order tracking.

---

## 2. Technical Stack
### Backend
- **Framework:** Django 4.2
- **API Engine:** Django REST Framework (DRF)
- **Database:** SQLite (Local) / PostgreSQL (Production)
- **Image Processing:** Pillow
- **Authentication:** Token-specific (Bearer Token) with custom verification decorators.

### Frontend
- **Logic:** Vanilla JavaScript (ES6+)
- **Styling:** Modern CSS3 (Glassmorphism & 3D Transitions)
- **Structure:** HTML5 (Semantic & SEO-Optimized)
- **Animations:** CSS Perspective & Intersection Observer API for scroll reveals.

---

## 3. Backend Architecture (Django)

### Core Apps
1.  **Apps.Store:** Manages vouchers, categories, FAQs, and testimonials.
2.  **Apps.Users:** Handles custom user profiles, authentication, and password recovery.
3.  **Apps.Cart:** Manages the shopping cart state persisted in the database.
4.  **Apps.Orders:** Handles order creation, historical processing, and voucher code generation.

### Database Models
- **UserProfile:** Custom user model using email/phone for login.
- **Voucher:** Stores voucher information, pricing, stock, and local images.
- **Order:** Stores order metadata (status, total, user-link).
- **OrderItem:** Links vouchers to orders and stores generated unique **Voucher Codes**.
- **CartItem:** Tracks items in a user's active shopping cart.

---

## 4. API Documentation (V1.1 Updated)

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/v1/auth/signup/` | POST | Register a new user. Redirects to Login if account exists. |
| `/api/v1/auth/login/` | POST | Authenticate user. Redirects to Signup if no account found. |
| `/api/v1/auth/password-reset/request/` | POST | Request OTP via Mobile Number for password recovery. |
| `/api/v1/auth/password-reset/confirm/` | POST | Confirm OTP and set a new password. |
| `/api/v1/vouchers/` | GET | List all active vouchers (search/filter enabled). |
| `/api/v1/cart/` | GET | Fetch the current authenticated user's cart. |
| `/api/v1/orders/` | GET | Fetch purchase history including items and voucher codes. |
| `/api/v1/orders/checkout/` | POST | Convert cart into a paid order with unique voucher codes. |

---

## 5. Frontend Features & UI Logic

### Premium 3D Authentication
- **Flip Transition:** A physical 3D card flip animation between Sign In and Sign Up forms.
- **Smart Logic:** Automatically detects if a user is trying to register an existing account and prompts login, or vice-versa.
- **Glassmorphism:** Dark navy gradients with high-blur backdrops for a professional enterprise feel.

### Personalized User Experience
- **Dynamic Header:** Replaces generic "Sign In" button with the **User's First Name** upon successful authentication.
- **My Orders Page:** Dedicated section for users to view order status, purchase dates, and retrieve their **Voucher Codes** instantly.
- **Toast Notifications:** Real-time feedback for cart actions, login success, and error handling.

### Advanced Navigation
- **Responsive Logo:** Left-aligned branding with optimized right-aligned action menu.
- **Mobile-Friendly:** Full drawer-style navigation for smaller devices.
- **Unified Theme:** Consistent Navy, Cyan, and Ivory palette with Neon Glow shadow effects on all interactive cards.

---

## 6. Security & Performance
- **Secure Password Reset:** Multi-step phone-based recovery ensures session safety.
- **API Optimization:** Order history uses `prefetch_related` to load full details in a single request, reducing frontend latency.
- **Input Cleaning:** Integrated `escapeHtml` helpers for all dynamic content rendering.
- **JWT-like Token Auth:** Custom Bearer token verification on all sensitive endpoints.

---

## 7. Setup & Installation
1.  **Backend:** `pip install -r requirements.txt` -> `python manage.py migrate` -> `python manage.py runserver`
2.  **Access:** Open `http://127.0.0.1:8000/` in any modern browser.
3.  **Dev Tools:** OTP codes for password reset are currently logged to the Django terminal for development convenience.

---
*Documentation revised for Samaniya VoucherHub V1.1*
