from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    session,
    redirect
)

from config import Config

from models.db import db
from models.user import User
from models.product import Product
from models.order import Order

from auth.auth_routes import auth
from marketplace.marketplace_routes import marketplace
from admin.admin_routes import admin
from seller.seller_routes import seller

from services.ai_recommendation import recommend_crop
from services.disease_prediction import predict_disease
from services.voice_assistant import handle_voice_command

# ==================================================
# APP CONFIG
# ==================================================

app = Flask(__name__)

app.config.from_object(Config)

app.secret_key = "smart_agro_secret_key"

db.init_app(app)

# ==================================================
# REGISTER BLUEPRINTS
# ==================================================

app.register_blueprint(auth)
app.register_blueprint(marketplace)
app.register_blueprint(admin)
app.register_blueprint(seller)

# ==================================================
# HOME
# ==================================================

@app.route("/")
def home():

    if "user_id" in session:

        role = session.get("role")

        if role == "farmer":
            return redirect("/seller_dashboard")

        elif role == "buyer":
            return redirect("/buyer_dashboard")

        elif role == "admin":
            return redirect("/admin_dashboard")

    return redirect("/login")

# ==================================================
# FARMER DASHBOARD
# ==================================================

@app.route("/farmer_dashboard")
def farmer_dashboard():

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
        "farmer_dashboard.html",
        total_products=len(products),
        total_orders=len(orders),
        revenue=revenue,
        predictions=0
    )

# ==================================================
# BUYER DASHBOARD
# ==================================================

@app.route("/buyer_dashboard")
def buyer_dashboard():

    if "user_id" not in session:
        return redirect("/login")

    if session.get("role") != "buyer":
        return redirect("/login")

    orders = Order.query.filter_by(
        buyer_id=session["user_id"]
    ).all()

    spent = sum(order.total_price for order in orders)
    purchased = sum(order.quantity for order in orders)

    return render_template(
        "buyer_dashboard.html",
        orders=orders,
        total_orders=len(orders),
        spent=spent,
        purchased=purchased
    )

# ==================================================
# AI PAGE
# ==================================================

@app.route("/predict_crop_page")
def predict_crop_page():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("ai_recommendation.html")

# ==================================================
# AI PREDICTION API
# ==================================================

@app.route("/predict_crop", methods=["POST"])
def predict_crop():

    try:

        data = request.get_json()

        crop = recommend_crop(
            season=data["season"],
            temperature=float(data["temperature"]),
            humidity=float(data["humidity"]),
            ph=float(data["ph"]),
            rainfall=float(data["rainfall"]),
            N=float(data.get("N", 50)),
            P=float(data.get("P", 40)),
            K=float(data.get("K", 40))
        )

        return jsonify({
            "success": True,
            "recommended_crop": crop
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        })

# ==================================================
# DISEASE PREDICTION
# ==================================================

@app.route("/disease_predictor")
def disease_predictor_page():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("disease_predictor.html")


@app.route("/predict_disease", methods=["POST"])
def predict_disease_api():

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "error": "Login required"
        })

    try:

        data = request.get_json() or {}
        result = predict_disease(
            crop=data.get("crop", ""),
            symptoms=data.get("symptoms", "")
        )

        return jsonify({
            "success": True,
            "result": result
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        })

# ==================================================
# VOICE ASSISTANT
# ==================================================

@app.route("/voice_assistant")
def voice_assistant_page():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("voice_assistant.html")


@app.route("/voice_command", methods=["POST"])
def voice_command():

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "Please login first."
        })

    data = request.get_json() or {}
    result = handle_voice_command(
        data.get("command", ""),
        session.get("role")
    )

    return jsonify(result)

# ==================================================
# DATABASE INIT
# ==================================================

with app.app_context():

    try:

        db.create_all()

        print("Database connected successfully")

    except Exception as e:

        print("Database error")
        print(e)

# ==================================================
# RUN APP
# ==================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )
