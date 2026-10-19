from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    flash
)

from models.user import User
from models.db import db

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

auth = Blueprint("auth", __name__)

# ==================================================
# REGISTER
# ==================================================

@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")

        existing = User.query.filter_by(email=email).first()

        if existing:
            flash("Email already exists", "danger")
            return redirect("/register")

        user = User(
            name=name,
            email=email,
            password=generate_password_hash(password),
            role=role
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration Successful. Please Login.", "success")

        return redirect("/login")

    return render_template("register.html")


# ==================================================
# LOGIN
# ==================================================

@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user:

            if check_password_hash(user.password, password):

                session["user_id"] = user.id
                session["name"] = user.name
                session["role"] = user.role

                print(f"Logged in: {user.name}")
                print(f"Role: {user.role}")

                if user.role == "farmer":
                    return redirect("/seller_dashboard")

                elif user.role == "buyer":
                    return redirect("/buyer_dashboard")

                elif user.role == "admin":
                    return redirect("/admin_dashboard")

        flash("Invalid Email or Password", "danger")

        return redirect("/login")

    return render_template("login.html")


# ==================================================
# LOGOUT
# ==================================================

@auth.route("/logout")
def logout():

    session.clear()

    flash("Logged Out Successfully", "success")

    return redirect("/login")