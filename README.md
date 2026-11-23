# AURA — Streetwear Website

A fully functional e-commerce website for AURA, a Karachi-based streetwear brand.
Black / silver / lime-green minimalist design, Y2K-styled branding, product
categories with fixed pricing, a working cart, and a checkout flow that emails
every order's full details straight to **iamahmedali78@gmail.com**.

Backend: Python (Flask). Payment method: Cash on Delivery only.

---

## 1. Install dependencies

You need Python 3.8+ installed. Then, from this folder, run:

```
pip install flask
```

## 2. Set up order emails (Gmail)

The site sends order emails using Gmail's SMTP server. You need a Gmail
**App Password** (NOT your normal Gmail password — Google blocks normal
passwords for this).

**Steps to get an App Password:**
1. Go to https://myaccount.google.com/security
2. Turn on **2-Step Verification** if it isn't already on (required for App Passwords).
3. Go to https://myaccount.google.com/apppasswords
4. Create a new App Password (name it "AURA Website").
5. Copy the 16-character password it gives you.

**Then set two environment variables** (replace with your real sending Gmail
account — this can be the same Gmail account the orders are delivered to,
or a different one):

On Mac/Linux:
```
export AURA_SMTP_EMAIL="your-sending-email@gmail.com"
export AURA_SMTP_APP_PASSWORD="your16charapppassword"
```

On Windows (PowerShell):
```
$env:AURA_SMTP_EMAIL="your-sending-email@gmail.com"
$env:AURA_SMTP_APP_PASSWORD="your16charapppassword"
```

If you skip this step, the site still works completely — every order is
automatically saved as a text file in the `orders/` folder — but no email
will be sent until you configure these.

To change which email address RECEIVES the orders, open `app.py` and edit
this line near the top:

```python
ORDER_RECIPIENT_EMAIL = "iamahmedali78@gmail.com"
```

## 3. Run the website

```
python app.py
```

Then open your browser to:

```
http://127.0.0.1:5000
```

## 4. How it works

- **Categories & pricing** — edit `products.py` to add/remove products or
  change prices. Each category (Women, Winter, Bottoms, T-Shirts, Caps,
  Exclusive) has one fixed price applied to every product in it.
- **Cart** — stored in the browser (localStorage), so it persists between
  pages without needing a database.
- **Checkout** — collects name, phone, email, and address (required), plus
  optional order notes. All prices are re-verified on the server before the
  order total is calculated — nothing is trusted from the browser.
- **Order emails** — every order sends a plain-text email with full
  customer + item + total details, and is also saved to `orders/` as a
  backup in case the email fails to send.
- **Exclusive category** — suits are customizable; customers can add fit,
  fabric, or color notes per item instead of a size.

## 5. Going live (optional)

This runs on your own computer for testing. To make it publicly accessible
as a real website, you'll need to deploy it to a hosting service (e.g.
PythonAnywhere, Render, Railway, or a VPS). Let me know if you want help
with that step — the code is ready for it, it just needs a host.

## 6. Image rights note

The product photos used in this build were the ones you provided. Please
make sure you have commercial usage rights for all of them (and the
homepage hero illustration) before the site goes live publicly.
