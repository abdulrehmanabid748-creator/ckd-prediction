import os
from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np

app = Flask(__name__)

# Load model and scaler
model = pickle.load(open('ckd_model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))

# Feature names (same order as training)
FEATURES = [
    'Age', 'Gender', 'Ethnicity', 'SocioeconomicStatus', 'EducationLevel',
    'BMI', 'Smoking', 'AlcoholConsumption', 'PhysicalActivity', 'DietQuality',
    'SleepQuality', 'FamilyHistoryKidneyDisease', 'FamilyHistoryHypertension',
    'FamilyHistoryDiabetes', 'PreviousAcuteKidneyInjury', 'UrinaryTractInfections',
    'SystolicBP', 'DiastolicBP', 'FastingBloodSugar', 'HbA1c',
    'SerumCreatinine', 'BUNLevels', 'GFR', 'ProteinInUrine',
    'ACR', 'SerumElectrolytesSodium', 'SerumElectrolytesPotassium',
    'SerumElectrolytesCalcium', 'SerumElectrolytesPhosphorus', 'HemoglobinLevels', 'CholesterolTotal',
    'CholesterolLDL', 'CholesterolHDL', 'CholesterolTriglycerides',
    'ACEInhibitors', 'Diuretics', 'NSAIDsUse', 'Statins', 'AntidiabeticMedications',
    'Edema', 'FatigueLevels', 'NauseaVomiting', 'MuscleCramps', 'Itching',
    'QualityOfLifeScore', 'HeavyMetalsExposure', 'OccupationalExposureChemicals',
    'WaterQuality', 'MedicalCheckupsFrequency', 'MedicationAdherence',
    'HealthLiteracy'
]

@app.route('/')
def home():
    return render_template('index.html', features=FEATURES)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        input_values = []
        for feature in FEATURES:
            value = data.get(feature)
            if value is None:
                return jsonify({'error': f'Missing field: {feature}'}), 400
            input_values.append(float(value))

        input_array = np.array([input_values])
        input_scaled = scaler.transform(input_array)
        prediction = model.predict(input_scaled)[0]
        probability = model.predict_proba(input_scaled)[0]

        result = {
            'prediction': int(prediction),
            'diagnosis': 'CKD Detected' if prediction == 1 else 'No CKD',
            'confidence': round(float(max(probability)) * 100, 2),
            'ckd_probability': round(float(probability[1]) * 100, 2),
            'healthy_probability': round(float(probability[0]) * 100, 2)
        }
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'API is running', 'model': 'CKD Prediction Model'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
