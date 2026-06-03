# CKD Prediction Flask API

## Setup & Run Karne Ka Tarika

### Step 1: Files arrange karo
```
CKD_Flask_API/
├── app.py
├── requirements.txt
├── ckd_model.pkl        ← Colab se download kiya hua
├── scaler.pkl           ← Colab se download kiya hua
└── templates/
    └── index.html
```

### Step 2: Dependencies install karo
```bash
pip install -r requirements.txt
```

### Step 3: API run karo
```bash
python app.py
```

### Step 4: Browser mein kholo
```
http://localhost:5000
```

## API Endpoints

| Endpoint   | Method | Description              |
|------------|--------|--------------------------|
| `/`        | GET    | Frontend form            |
| `/predict` | POST   | JSON input → prediction  |
| `/health`  | GET    | API status check         |

## /predict Example (JSON)

```json
POST /predict
{
  "Age": 55,
  "Gender": 1,
  "BMI": 27.5,
  "SerumCreatinine": 1.8,
  "GFR": 65,
  ...
}
```

## Response
```json
{
  "prediction": 1,
  "diagnosis": "CKD Detected",
  "confidence": 92.5,
  "ckd_probability": 92.5,
  "healthy_probability": 7.5
}
```
