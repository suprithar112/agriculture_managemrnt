from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    session,
    redirect
)

from models.product import Product
from models.order import Order
from models.db import db

marketplace = Blueprint("marketplace", __name__)

# ==========================================
# MARKETPLACE PAGE
# ==========================================

@marketplace.route("/market")
def market():

    if "user_id" not in session:
        return redirect("/login")

    search = request.args.get("search", "").strip()
    min_price = request.args.get("min_price", "").strip()
    max_price = request.args.get("max_price", "").strip()

    query = Product.query

    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    try:
        if min_price:
            query = query.filter(Product.price >= float(min_price))

        if max_price:
            query = query.filter(Product.price <= float(max_price))
    except ValueError:
        min_price = ""
        max_price = ""

    products = query.order_by(Product.id.desc()).all()

    return render_template(
        "marketplace.html",
        products=products,
        search=search,
        min_price=min_price,
        max_price=max_price
    )

# ==========================================
# ADD PRODUCT
# ==========================================

@marketplace.route("/add_product", methods=["POST"])
def add_product():

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "Login Required"
        })

    if session.get("role") != "farmer":
        return jsonify({
            "success": False,
            "message": "Only farmers can add products"
        })

    try:

        product = Product(
            name=request.form["name"],
            price=float(request.form["price"]),
            quantity=int(request.form["quantity"]),
            farmer_id=session["user_id"]
        )

        db.session.add(product)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Product Added Successfully"
        })

    except Exception as e:

        db.session.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        })

# ==========================================
# PLACE ORDER
# ==========================================

@marketplace.route("/order", methods=["POST"])
def place_order():

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "Please Login First"
        })

    if session.get("role") != "buyer":
        return jsonify({
            "success": False,
            "message": "Only buyers can place orders"
        })

    try:

        data = request.get_json()

        product_id = int(data["product_id"])
        quantity = int(data["quantity"])

        buyer_id = session["user_id"]

        product = Product.query.filter_by(
            id=product_id
        ).first()

        if not product:

            return jsonify({
                "success": False,
                "message": "Product Not Found"
            })

        if quantity <= 0:

            return jsonify({
                "success": False,
                "message": "Invalid Quantity"
            })

        if product.quantity < quantity:

            return jsonify({
                "success": False,
                "message": "Insufficient Stock"
            })

        total_price = product.price * quantity

        order = Order(
            buyer_id=buyer_id,
            product_id=product.id,
            quantity=quantity,
            total_price=total_price
        )

        product.quantity -= quantity

        db.session.add(order)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Order Placed Successfully"
        })

    except Exception as e:

        db.session.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        })
