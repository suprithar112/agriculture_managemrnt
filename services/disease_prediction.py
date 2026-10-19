DISEASE_RULES = [
    {
        "name": "Leaf Blast",
        "crops": {"rice", "wheat", "barley"},
        "keywords": {"diamond", "spots", "lesions", "gray", "brown", "dry leaves"},
        "treatment": "Remove infected leaves, avoid overhead watering, and apply a recommended fungicide such as tricyclazole or mancozeb.",
        "prevention": "Use resistant varieties, keep good field spacing, and avoid excess nitrogen."
    },
    {
        "name": "Powdery Mildew",
        "crops": {"wheat", "barley", "vegetables", "grapes"},
        "keywords": {"white", "powder", "dust", "mildew", "patches"},
        "treatment": "Spray sulfur-based or potassium bicarbonate fungicide and remove heavily affected parts.",
        "prevention": "Improve air circulation, reduce leaf wetness, and avoid dense planting."
    },
    {
        "name": "Bacterial Leaf Blight",
        "crops": {"rice", "maize", "cotton"},
        "keywords": {"yellow", "wilting", "water soaked", "streaks", "leaf edges"},
        "treatment": "Remove affected plants where possible and use copper-based bactericide as advised locally.",
        "prevention": "Use certified seed, maintain clean irrigation water, and avoid working in wet fields."
    },
    {
        "name": "Root Rot",
        "crops": {"cotton", "sugarcane", "vegetables", "pulses"},
        "keywords": {"root", "black roots", "stunted", "wilting", "soft stem", "rotting"},
        "treatment": "Improve drainage, remove badly infected plants, and treat soil with a suitable fungicide.",
        "prevention": "Avoid waterlogging, rotate crops, and use healthy seedlings."
    },
    {
        "name": "Rust Disease",
        "crops": {"wheat", "barley", "maize"},
        "keywords": {"rust", "orange", "brown powder", "pustules", "reddish"},
        "treatment": "Apply a recommended systemic fungicide and remove volunteer host plants.",
        "prevention": "Plant resistant varieties and monitor fields during humid weather."
    }
]


def predict_disease(crop, symptoms):
    crop_value = (crop or "").strip().lower()
    symptom_text = (symptoms or "").strip().lower()

    if not crop_value or not symptom_text:
        raise ValueError("Please enter crop name and visible symptoms.")

    best_match = None
    best_score = 0

    for rule in DISEASE_RULES:
        keyword_score = sum(1 for keyword in rule["keywords"] if keyword in symptom_text)
        crop_score = 1 if crop_value in rule["crops"] else 0
        score = keyword_score + crop_score

        if score > best_score:
            best_score = score
            best_match = rule

    if best_match and best_score >= 2:
        confidence = min(95, 50 + best_score * 12)
        return {
            "disease": best_match["name"],
            "confidence": confidence,
            "treatment": best_match["treatment"],
            "prevention": best_match["prevention"]
        }

    return {
        "disease": "General Plant Stress",
        "confidence": 45,
        "treatment": "Check irrigation, soil nutrition, pest attack, and remove damaged leaves. Consult a local agriculture expert for severe symptoms.",
        "prevention": "Maintain balanced fertilizer use, proper drainage, field hygiene, and regular crop monitoring."
    }
