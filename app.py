"""
AURA — streetwear brand website
Flask backend: serves the storefront and handles checkout + order emails.

SETUP (see README.md for full instructions):
  1. pip install flask
  2. Set these environment variables before running:
       AURA_SMTP_EMAIL      - the Gmail address used to SEND the order email
       AURA_SMTP_APP_PASSWORD - a Gmail "App Password" (not your normal password)
  3. Run: python app.py
  4. Visit http://127.0.0.1:5000

Orders are emailed to ORDER_RECIPIENT_EMAIL (set below).
"""

import os
import re
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

from flask import Flask, render_template, request, jsonify, redirect, url_for

from products import (
    PRODUCTS,
    CATEGORIES,
    CATEGORY_ORDER,
    get_products_by_category,
    get_product,
)

app = Flask(__name__)

# ----------------------------------------------------------------------
# CONFIG
# ----------------------------------------------------------------------

ORDER_RECIPIENT_EMAIL = "iamahmedali78@gmail.com"

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_SENDER_EMAIL = os.environ.get("AURA_SMTP_EMAIL", "")
SMTP_APP_PASSWORD = os.environ.get("AURA_SMTP_APP_PASSWORD", "")

BRAND_NAME = "AURA"
BRAND_TAGLINE = "Karachi, 2025 — Streetwear for the GenZ aura."


# ----------------------------------------------------------------------
# HELPERS
# ----------------------------------------------------------------------

def is_valid_email(email: str) -> bool:
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email or ""))


def is_valid_phone(phone: str) -> bool:
    digits = re.sub(r"[^\d]", "", phone or "")
    return len(digits) >= 7


def build_order_email_body(order: dict) -> str:
    lines = []
    lines.append(f"New order received on {BRAND_NAME}")
    lines.append(f"Placed at: {order['timestamp']}")
    lines.append("")
    lines.append("CUSTOMER DETAILS")
    lines.append(f"  Name:    {order['name']}")
    lines.append(f"  Phone:   {order['phone']}")
    lines.append(f"  Email:   {order['email']}")
    lines.append(f"  Address: {order['address']}")
    lines.append("")
    lines.append("ORDER ITEMS")
    for item in order["items"]:
        line = f"  - {item['name']} x{item['quantity']}  (Rs. {item['price']:,} each)"
        if item.get("size"):
            line += f"  | Size: {item['size']}"
        if item.get("customization"):
            line += f"  | Customization notes: {item['customization']}"
        lines.append(line)
    lines.append("")
    lines.append(f"TOTAL: Rs. {order['total']:,}")
    lines.append("")
    lines.append("Payment method: Cash on Delivery (COD)")
    if order.get("notes"):
        lines.append("")
        lines.append(f"Customer notes: {order['notes']}")
    return "\n".join(lines)


def send_order_email(order: dict) -> tuple[bool, str]:
    """Attempts to send the order notification email. Returns (success, message)."""
    if not SMTP_SENDER_EMAIL or not SMTP_APP_PASSWORD:
        return False, (
            "Email not sent: SMTP credentials are not configured. "
            "Set AURA_SMTP_EMAIL and AURA_SMTP_APP_PASSWORD environment variables. "
            "The order was still recorded below."
        )

    body = build_order_email_body(order)
    msg = MIMEText(body)
    msg["Subject"] = f"New {BRAND_NAME} Order — {order['name']} — Rs. {order['total']:,}"
    msg["From"] = SMTP_SENDER_EMAIL
    msg["To"] = ORDER_RECIPIENT_EMAIL

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15) as server:
            server.starttls()
            server.login(SMTP_SENDER_EMAIL, SMTP_APP_PASSWORD)
            server.sendmail(SMTP_SENDER_EMAIL, [ORDER_RECIPIENT_EMAIL], msg.as_string())
        return True, "Order email sent successfully."
    except Exception as exc:  # noqa: BLE001
        return False, f"Failed to send order email: {exc}"


def log_order_to_file(order: dict, email_status: str):
    """Always keep a local backup of every order, regardless of email success."""
    os.makedirs("orders", exist_ok=True)
    filename = os.path.join("orders", f"order_{order['timestamp'].replace(':', '-').replace(' ', '_')}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(build_order_email_body(order))
        f.write(f"\n\nEmail status: {email_status}\n")


# ----------------------------------------------------------------------
# ROUTES — storefront
# ----------------------------------------------------------------------

@app.route("/")
def home():
    featured = []
    for cat in CATEGORY_ORDER:
        products = get_products_by_category(cat)
        if products:
            featured.append({
                "category": cat,
                "label": CATEGORIES[cat]["label"],
                "price": CATEGORIES[cat]["price"],
                "product": products[0],
            })
    return render_template("index.html", featured=featured, brand=BRAND_NAME, tagline=BRAND_TAGLINE)


@app.route("/shop/<category>")
def shop_category(category):
    if category not in CATEGORIES:
        return redirect(url_for("home"))
    products = get_products_by_category(category)
    return render_template(
        "category.html",
        category=category,
        category_label=CATEGORIES[category]["label"],
        price=CATEGORIES[category]["price"],
        customizable=CATEGORIES[category]["customizable"],
        products=products,
        categories=CATEGORY_ORDER,
        category_meta=CATEGORIES,
    )


@app.route("/cart")
def cart():
    return render_template("cart.html")


@app.route("/checkout")
def checkout_page():
    return render_template("checkout.html")


@app.route("/order-confirmed")
def order_confirmed():
    return render_template("confirmation.html")


# ----------------------------------------------------------------------
# ROUTES — API (used by cart.js)
# ----------------------------------------------------------------------

@app.route("/api/products")
def api_products():
    """Returns full product list with prices, so the frontend cart never
    has to trust client-side price data."""
    out = []
    for p in PRODUCTS:
        out.append({
            **p,
            "price": CATEGORIES[p["category"]]["price"],
            "customizable": CATEGORIES[p["category"]]["customizable"],
        })
    return jsonify(out)


@app.route("/api/checkout", methods=["POST"])
def api_checkout():
    data = request.get_json(force=True, silent=True) or {}

    name = (data.get("name") or "").strip()
    phone = (data.get("phone") or "").strip()
    email = (data.get("email") or "").strip()
    address = (data.get("address") or "").strip()
    notes = (data.get("notes") or "").strip()
    cart_items = data.get("items") or []

    errors = {}
    if not name:
        errors["name"] = "Name is required."
    if not phone or not is_valid_phone(phone):
        errors["phone"] = "A valid phone number is required."
    if not email or not is_valid_email(email):
        errors["email"] = "A valid email address is required."
    if not address or len(address) < 8:
        errors["address"] = "A complete delivery address is required."
    if not cart_items:
        errors["items"] = "Your cart is empty."

    if errors:
        return jsonify({"success": False, "errors": errors}), 400

    # Re-price every item server-side — never trust the client's price.
    priced_items = []
    total = 0
    for item in cart_items:
        product = get_product(item.get("id", ""))
        if not product:
            continue
        price = CATEGORIES[product["category"]]["price"]
        quantity = max(1, int(item.get("quantity", 1)))
        priced_items.append({
            "name": product["name"],
            "price": price,
            "quantity": quantity,
            "size": item.get("size", ""),
            "customization": item.get("customization", ""),
        })
        total += price * quantity

    if not priced_items:
        return jsonify({"success": False, "errors": {"items": "Your cart could not be processed."}}), 400

    order = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "name": name,
        "phone": phone,
        "email": email,
        "address": address,
        "notes": notes,
        "items": priced_items,
        "total": total,
    }

    success, message = send_order_email(order)
    log_order_to_file(order, message)

    return jsonify({
        "success": True,
        "email_sent": success,
        "message": "Order placed successfully." if success else "Order placed, but the notification email could not be sent. " + message,
        "total": total,
    })


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
