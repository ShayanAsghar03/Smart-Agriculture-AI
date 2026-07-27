# Smart Agriculture AI

A Flask web application that provides two agriculture-focused tools:

- **Crop recommendation** based on soil nutrients and weather conditions.
- **Crop yield prediction** based on crop, country, year, rainfall, pesticide use, and average temperature.

## Features

- Recommends one of 22 crops using nitrogen, phosphorus, potassium, temperature, humidity, pH, and rainfall values.
- Predicts crop yield for Maize, Wheat, Rice, Sugarcane, Potato, and Soybeans.
- Simple browser-based interface built with Flask templates.
- Pre-trained machine-learning models included in the `models/` directory.

## Tech Stack

- Python
- Flask
- NumPy
- Pandas
- Scikit-learn

## Project Structure

```text
Smart-Agriculture-AI/
├── app.py
├── requirements.txt
├── models/
│   ├── crop_model.pkl
│   ├── crop_scaler.pkl
│   ├── crop_yield_model.pkl
│   └── crop_preprocessor.pkl
└── templates/
    ├── home.html
    ├── recommendation.html
    └── prediction.html
```

## Installation and Setup

1. Clone the repository and enter the project directory.

   ```bash
   git clone https://github.com/ShayanAsghar03/Smart-Agriculture-AI.git
   cd Smart-Agriculture-AI
   ```

2. Create and activate a virtual environment.

   **Windows PowerShell:**

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **macOS/Linux:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies.

   ```bash
   pip install -r requirements.txt
   ```

4. Start the application.

   ```bash
   python app.py
   ```

5. Open the app in your browser:

   ```text
   http://127.0.0.1:5000
   ```

## Usage

### Crop Recommendation

Enter the soil nutrient values (N, P, K), temperature, humidity, pH, and rainfall. The application returns a recommended crop.

### Yield Prediction

Select a crop and area, then provide the year, average rainfall, pesticide quantity, and average temperature. The application returns the estimated yield.

## Notes

- Keep all `.pkl` files inside the `models/` directory; the app needs them to make predictions.
- The development server runs with Flask debug mode enabled.

## License

This project is intended for educational purposes.
