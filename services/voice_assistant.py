def handle_voice_command(command, role):
    text = (command or "").strip().lower()

    if not text:
        return {
            "success": False,
            "message": "I did not hear a command. Please try again."
        }

    routes = [
        (("market", "marketplace", "products", "buy"), "/market", "Opening marketplace."),
        (("crop", "recommend", "recommendation", "ai"), "/predict_crop_page", "Opening crop recommendation."),
        (("disease", "plant disease", "symptoms"), "/disease_predictor", "Opening disease predictor."),
        (("seller", "farmer", "inventory", "add product"), "/seller_dashboard", "Opening seller dashboard."),
        (("buyer", "orders", "my orders"), "/buyer_dashboard", "Opening buyer dashboard."),
        (("admin", "users", "revenue"), "/admin_dashboard", "Opening admin dashboard."),
        (("logout", "sign out"), "/logout", "Logging out.")
    ]

    for keywords, url, message in routes:
        if any(keyword in text for keyword in keywords):
            if url == "/seller_dashboard" and role != "farmer":
                return {"success": True, "message": "Seller dashboard is only for farmer accounts."}
            if url == "/buyer_dashboard" and role != "buyer":
                return {"success": True, "message": "Buyer dashboard is only for buyer accounts."}
            if url == "/admin_dashboard" and role != "admin":
                return {"success": True, "message": "Admin dashboard is only for admin accounts."}
            return {
                "success": True,
                "message": message,
                "redirect": url
            }

    help_text = (
        "You can say: open marketplace, crop recommendation, disease predictor, "
        "seller dashboard, buyer dashboard, admin dashboard, or logout."
    )

    return {
        "success": True,
        "message": help_text
    }
