# AURA — product catalog
# Each product belongs to a category with a FIXED price (per the brand's pricing rules).
# Prices are in PKR.

CATEGORIES = {
    "women": {
        "label": "Women",
        "price": 7999,
        "customizable": False,
    },
    "winter": {
        "label": "Winter",
        "price": 8999,
        "customizable": False,
    },
    "bottoms": {
        "label": "Bottoms",
        "price": 5999,
        "customizable": False,
    },
    "tshirts": {
        "label": "T-Shirts",
        "price": 2000,
        "customizable": False,
    },
    "caps": {
        "label": "Caps",
        "price": 1700,
        "customizable": False,
    },
    "exclusive": {
        "label": "Exclusive",
        "price": 35999,
        "customizable": True,
    },
}

# Category display order on the site
CATEGORY_ORDER = ["exclusive", "women", "winter", "bottoms", "tshirts", "caps"]

PRODUCTS = [
    # WOMEN
    {"id": "women-01", "category": "women", "name": "No Gods Allowed Tee", "image": "women/women-01.jpg",
     "description": "Oversized graphic tee with bold front print. Streetwear essential, built for comfort and attitude."},
    {"id": "women-02", "category": "women", "name": "Rich Man Graphic Tee", "image": "women/women-02.jpg",
     "description": "Vintage-inspired oversized tee with statement graphic print. Easy, relaxed fit."},

    # WINTER
    {"id": "winter-01", "category": "winter", "name": "Ocean Danger Hoodie", "image": "winter/winter-01.jpg",
     "description": "Heavyweight fleece hoodie with bold back graphic. Built warm, built loud."},
    {"id": "winter-02", "category": "winter", "name": "Shearling Collar Puffer", "image": "winter/winter-02.jpg",
     "description": "Insulated puffer jacket with detachable-look shearling collar. Street-ready warmth."},
    {"id": "winter-03", "category": "winter", "name": "Canvas Hooded Jacket", "image": "winter/winter-03.jpg",
     "description": "Durable canvas work jacket with layered hood. Built to last, styled to stand out."},
    {"id": "winter-04", "category": "winter", "name": "Red Fleece Zip Hoodie", "image": "winter/winter-04.jpg",
     "description": "Full-zip fleece hoodie with contrast piping and face-mask hood. Maximum warmth, maximum presence."},
    {"id": "winter-05", "category": "winter", "name": "Striped Puffer Jacket", "image": "winter/winter-05.jpg",
     "description": "Classic puffer silhouette with side racing stripe. A cold-weather staple."},

    # BOTTOMS
    {"id": "bottoms-01", "category": "bottoms", "name": "Flame Embroidered Sweatpants", "image": "bottoms/bottoms-01.jpg",
     "description": "Relaxed-fit sweatpants with tonal flame embroidery down the leg."},
    {"id": "bottoms-02", "category": "bottoms", "name": "Graphic Logo Shorts", "image": "bottoms/bottoms-02.jpg",
     "description": "Loose-fit sweat shorts with bold wraparound graphic lettering."},
    {"id": "bottoms-03", "category": "bottoms", "name": "Side-Stripe Track Pants", "image": "bottoms/bottoms-03.jpg",
     "description": "Wide-leg track pants with tonal side stripes. Clean, minimal, versatile."},

    # T-SHIRTS
    {"id": "tshirts-01", "category": "tshirts", "name": "CB Star Graphic Tee", "image": "tshirts/tshirts-01.jpg",
     "description": "Classic fit white tee with bold front graphic and star detail."},

    # CAPS
    {"id": "caps-01", "category": "caps", "name": "Script Snapback", "image": "caps/caps-01.jpg",
     "description": "Structured snapback with embroidered script lettering."},
    {"id": "caps-02", "category": "caps", "name": "Classic Team Cap", "image": "caps/caps-02.jpg",
     "description": "Structured fitted cap with embroidered front logo."},
    {"id": "caps-03", "category": "caps", "name": "Washed Dad Cap", "image": "caps/caps-03.jpg",
     "description": "Garment-washed low-profile cap with embroidered front logo. Soft, broken-in feel."},

    # EXCLUSIVE
    {"id": "exclusive-01", "category": "exclusive", "name": "Burgundy Tailored Suit", "image": "exclusive/exclusive-01.jpg",
     "description": "Fully tailored two-piece suit in deep burgundy. Customizable fit, fabric and detailing."},
    {"id": "exclusive-02", "category": "exclusive", "name": "Pinstripe Executive Suit", "image": "exclusive/exclusive-02.jpg",
     "description": "Classic pinstripe tailoring with a modern cut. Customizable fit, fabric and detailing."},
    {"id": "exclusive-03", "category": "exclusive", "name": "Midnight Double-Breasted Suit", "image": "exclusive/exclusive-03.jpg",
     "description": "Double-breasted suit in deep black. Sharp, formal, uncompromising. Customizable fit, fabric and detailing."},
    {"id": "exclusive-04", "category": "exclusive", "name": "Heritage Pinstripe Three-Piece", "image": "exclusive/exclusive-04.jpg",
     "description": "Three-piece pinstripe suit with vest and pocket detailing. Customizable fit, fabric and detailing."},
    {"id": "exclusive-05", "category": "exclusive", "name": "Vintage Chain Pinstripe Suit", "image": "exclusive/exclusive-05.jpg",
     "description": "Vintage-inspired pinstripe suit with statement chain detailing. Customizable fit, fabric and detailing."},
]


def get_products_by_category(category):
    return [p for p in PRODUCTS if p["category"] == category]


def get_product(product_id):
    for p in PRODUCTS:
        if p["id"] == product_id:
            return p
    return None


def get_price(category):
    return CATEGORIES[category]["price"]
