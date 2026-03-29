from flask import Flask, request, render_template
import numpy as np
import pandas as pd
import pickle
import os

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    crop_model = pickle.load(open(os.path.join(BASE_DIR, "models/crop_model.pkl"), "rb"))
    crop_scaler = pickle.load(open(os.path.join(BASE_DIR, "models/crop_scaler.pkl"), "rb"))

    yield_model = pickle.load(open(os.path.join(BASE_DIR, "models/crop_yield_model.pkl"), "rb"))
    yield_preprocessor = pickle.load(open(os.path.join(BASE_DIR, "models/crop_preprocessor.pkl"), "rb"))
except FileNotFoundError:
    print("ERROR: One or more model files not found. Ensure models/ directory exists.")

except Exception as e:
    print(f"An error occurred while loading models: {e}")

crop_dict = {
    1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut",
    6: "Papaya", 7: "Orange", 8: "Apple", 9: "Muskmelon",
    10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
    14: "Pomegranate", 15: "Lentil", 16: "Blackgram",
    17: "Mungbean", 18: "Mothbeans", 19: "Pigeonpeas",
    20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"
}

YIELD_ITEMS = ["Maize", "Wheat", "Rice", "Sugarcane", "Potato", "Soybeans"]
YIELD_AREAS = ["India", "Chile", "Brazil", "United Kingdom", "Indonesia", "Pakistan"]

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/recommendation")
def recommendation():
    return render_template("recommendation.html")

@app.route("/prediction")
def prediction():
    
    return render_template("prediction.html", items=YIELD_ITEMS, areas=YIELD_AREAS)

@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        N = float(request.form.get('N', 0))
        P = float(request.form.get('P', 0))
        K = float(request.form.get('K', 0))
        temperature = float(request.form.get('temperature', 0))
        humidity = float(request.form.get('humidity', 0))
        ph = float(request.form.get('ph', 0))
        rainfall = float(request.form.get('rainfall', 0))

        if N < 0 or P < 0 or K < 0 or humidity < 0 or ph < 0 or rainfall < 0:
             raise ValueError("Input values cannot be negative.")

        df = pd.DataFrame([[N, P, K, temperature, humidity, ph, rainfall]],
                          columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'])

        scaled = crop_scaler.transform(df)
        crop_code = crop_model.predict(scaled)[0]
        crop_name = crop_dict.get(crop_code, "Unknown Crop")

        return render_template("recommendation.html", crop=crop_name)
    
    except ValueError as e:
        
        return render_template("recommendation.html", error=f"Invalid Input: Please ensure all fields have valid numeric values. ({str(e)})")
    
    except Exception as e:
        
        return render_template("recommendation.html", error=f"An unexpected error occurred during recommendation: {str(e)}")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        Year = float(request.form.get('Year', 0))
        avg_rain = float(request.form.get('avg_rain', 0))
        pesticides = float(request.form.get('pesticides', 0))
        avg_temp = float(request.form.get('avg_temp', 0))
        
        Area = request.form.get('Area', '').strip()
        Item = request.form.get('Item', '').strip()

        if not Area or not Item:
            raise ValueError("Area and Crop Name fields are required.")

        features = np.array([[Year, avg_rain, pesticides, avg_temp, Area, Item]])
        
        transformed = yield_preprocessor.transform(features)
        result = yield_model.predict(transformed)[0]

        return render_template("prediction.html", yield_result=round(result, 2), items=YIELD_ITEMS, areas=YIELD_AREAS)
    
    except ValueError as e:
        return render_template("prediction.html", error=f"Input Error: Please ensure all numeric fields are filled correctly and categorical fields are selected. ({str(e)})", items=YIELD_ITEMS, areas=YIELD_AREAS)
    
    except Exception as e:
        return render_template("prediction.html", error=f"An unexpected error occurred during prediction. Check if Area and Crop Name are valid. ({str(e)})", items=YIELD_ITEMS, areas=YIELD_AREAS)

if __name__ == "__main__":
    app.run(debug=True)



    