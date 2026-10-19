from flask import Blueprint, render_template, redirect, session, flash

from models.user import User
from models.product import Product
from models.order import Order
from models.db import db

admin = Blueprint("admin", __name__)

@admin.route("/admin")
@admin.route("/admin_dashboard")
def admin_dashboard():

    if "user_id" not in session:
        return redirect("/login")

    if session.get("role") != "admin":
        return redirect("/login")

    users = User.query.count()
    farmers = User.query.filter_by(role="farmer").count()
    buyers = User.query.filter_by(role="buyer").count()
    products = Product.query.count()
    orders = Order.query.count()
    revenue = db.session.query(db.func.sum(Order.total_price)).scalar() or 0
    user_list = User.query.order_by(User.id.desc()).all()
    order_list = Order.query.order_by(Order.id.desc()).all()

    return render_template(
        "admin_dashboard.html",
        users=users,
        farmers=farmers,
        buyers=buyers,
        products=products,
        orders=orders,
        revenue=revenue,
        user_list=user_list,
        order_list=order_list
    )


@admin.route("/admin/delete_user/<int:user_id>")
def delete_user(user_id):

    if "user_id" not in session or session.get("role") != "admin":
        return redirect("/login")

    if user_id == session["user_id"]:
        flash("You cannot delete your own admin account.", "danger")
        return redirect("/admin_dashboard")

    user = User.query.get_or_404(user_id)

    try:
        db.session.delete(user)
        db.session.commit()
        flash("User deleted successfully.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Unable to delete user: {str(e)}", "danger")

    return redirect("/admin_dashboard")


@admin.route("/admin/complete_order/<int:order_id>")
def complete_order(order_id):

    if "user_id" not in session or session.get("role") != "admin":
        return redirect("/login")

    order = Order.query.get_or_404(order_id)
    order.status = "Completed"
    db.session.commit()
    flash("Order marked as completed.", "success")

    return redirect("/admin_dashboard")
