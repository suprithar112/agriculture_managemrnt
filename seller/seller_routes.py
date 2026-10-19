from flask import Blueprint, render_template, request, redirect, session, flash
from models.product import Product
from models.order import Order
from models.db import db

seller = Blueprint("seller", __name__)

# ---------------- SELLER DASHBOARD ----------------

@seller.route("/seller_dashboard")
def seller_dashboard():

    if "user_id" not in session:
        return redirect("/login")

    if session.get("role") != "farmer":
        return redirect("/login")

    products = Product.query.filter_by(
        farmer_id=session["user_id"]
    ).all()

    product_ids = [product.id for product in products]
    orders = Order.query.filter(Order.product_id.in_(product_ids)).all() if product_ids else []
    revenue = sum(order.total_price for order in orders)

    return render_template(
        "seller_dashboard.html",
        products=products,
        total_orders=len(orders),
        revenue=revenue,
        best_crop=products[0].name if products else "No products yet"
    )


# ---------------- ADD PRODUCT ----------------

@seller.route("/seller/add_product", methods=["POST"])
def add_product():

    if "user_id" not in session:
        return redirect("/login")

    if session.get("role") != "farmer":
        return redirect("/login")

    try:

        product = Product(
            name=request.form["name"],
            price=float(request.form["price"]),
            quantity=int(request.form["quantity"]),
            farmer_id=session["user_id"]
        )

        db.session.add(product)
        db.session.commit()

        flash("Product Added Successfully", "success")

    except Exception as e:

        db.session.rollback()
        flash(f"Error: {str(e)}", "danger")

    return redirect("/seller_dashboard")


# ---------------- DELETE PRODUCT ----------------

@seller.route("/delete_product/<int:id>")
def delete_product(id):

    if "user_id" not in session:
        return redirect("/login")

    if session.get("role") != "farmer":
        return redirect("/login")

    product = Product.query.get_or_404(id)

    # Prevent deleting other farmer products
    if product.farmer_id != session["user_id"]:
        flash("Unauthorized Access", "danger")
        return redirect("/seller_dashboard")

    db.session.delete(product)
    db.session.commit()

    flash("Product Deleted Successfully", "success")

    return redirect("/seller_dashboard")
