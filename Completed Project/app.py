from flask import Flask, render_template, request
from flask_cors import CORS
import pickle
import logging
import numpy as np
from features import featureExtraction

app = Flask(__name__)
CORS(app)

# Feature names matching your feature extraction
FEATURE_NAMES = [
    "having_ip", "have_at_sign", "url_length", "url_depth",
    "redirection", "http_domain", "tiny_url", "prefix_suffix",
    "dns_record", "web_traffic", "domain_age", "domain_end",
    "iframe", "mouse_over", "right_click", "forwarding"
]

# Load ML models
try:
    dt_model = pickle.load(open('DecisionTree.pickle', 'rb'))
    rf_model = pickle.load(open('RandomForest.pickle', 'rb'))
    print("✅ Models loaded successfully!")
except Exception as e:
    logging.error(f"❌ Model loading failed: {e}")
    raise

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        web_link = request.form.get('link', '').strip()
        model_choice = int(request.form.get('model', 1))  # Default to Decision Tree
        
        # Validate input
        if not web_link:
            return render_template('home.html', error="Please enter a URL")
        if not web_link.startswith(('http://', 'https://')):
            return render_template('home.html', error="URL must start with http:// or https://")

        # Extract features
        features = featureExtraction(web_link)
        if len(features) != 16:
            return render_template('home.html', error="Couldn't analyze this URL")

        # Make prediction
        model = dt_model if model_choice == 1 else rf_model
        prediction = model.predict([features])[0]
        confidence = model.predict_proba([features])[0][1]
        importances = model.feature_importances_

        # Prepare results
        features_analysis = [{
            "name": FEATURE_NAMES[i].replace('_', ' ').title(),
            "importance": importances[i] * 100
        } for i in range(len(FEATURE_NAMES))]

        return render_template('result.html',
                            pred=bool(prediction),
                            confidence=confidence,
                            features=features_analysis,
                            link=web_link)

    except Exception as e:
        logging.error(f"🚨 Prediction error: {e}")
        return render_template('home.html', error="Analysis failed. Please try another URL.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(host='0.0.0.0', port=8000, debug=True)