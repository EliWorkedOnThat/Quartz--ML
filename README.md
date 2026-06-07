# Quartz — Car Preference ML

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)
![scikit-learn](https://img.shields.io/badge/scikit--learn-RandomForest-orange?style=flat-square&logo=scikit-learn)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-purple?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

> A machine learning project that learns your car preferences and predicts which car you'd choose — before you even choose it.

---

## Screenshots

| Car Selector | Prediction Results |
|---|---|
| *Coming soon* | *Coming soon* |

> Add screenshots of `CarGUI.py` and `ResultGUI.py` here once running.

---

## How It Works

1. **You choose** between two randomly generated cars using the GUI
2. Every choice is **saved as a JSON file** — both cars, one labeled `accepted`, one `rejected`
3. After enough samples, a **Random Forest classifier** trains on your choices
4. The model learns **which features drive your decisions** (HP? Price? Mileage?)
5. It then **predicts your next choice** with a confidence percentage

The model doesn't guess — it finds the actual pattern in your behavior. With 40+ samples it reaches 80-90% accuracy and surfaces a ranked feature importance table showing exactly what you subconsciously prioritize.

---

## Project Structure

```
Quartz/
├── CarGenerator.py          # Car class, random generation, dataset saving
├── CarGUI.py                # Tkinter GUI for collecting preference data
├── DecisionAnalysis.py      # Model training, accuracy, feature importances
├── ResultGUI.py             # Tkinter GUI showing predictions and results
├── Car_Preference_dataset/  # Your personal JSON dataset (gitignored)
└── README.md
```

---

## Installation

**Clone the repo**
```bash
git clone https://github.com/EliWorkedOnThat/Quartz--ML.git
cd Quartz--ML
```

**Install dependencies**
```bash
pip install scikit-learn pandas
```

> Python 3.11+ required. Tkinter comes built into Python on Windows.

---

## Usage

### Step 1 — Collect your preferences
```bash
python CarGUI.py
```
Use ← → arrow keys or click the buttons to choose between two cars. The more choices you make, the better the model learns. Aim for 40+ samples.

### Step 2 — Train and predict
```bash
python ResultGUI.py
```
The model trains on your dataset and predicts which car you'd pick from a new random pair. Hit **"Predict Next Pair"** to keep testing.

### Step 3 — Inspect the analysis (optional)
```bash
python DecisionAnalysis.py
```
Prints accuracy, full feature importance rankings, and a prediction test in the terminal.

---

## Dataset Format

Each choice saves a single JSON file to `Car_Preference_dataset/`:

```json
{
    "car_1": {
        "brand": "BMW",
        "year": 2019,
        "color": "Black",
        "price": 35000,
        "mileage": 20000,
        "fuel_type": "Hybrid",
        "hp": 401,
        "status": "accepted"
    },
    "car_2": {
        "brand": "Toyota",
        "year": 2012,
        "color": "White",
        "price": 11000,
        "mileage": 95000,
        "fuel_type": "Gasoline",
        "hp": 162,
        "status": "rejected"
    }
}
```

---

## 🌲 The Model

- **Algorithm:** Random Forest Classifier (`sklearn.ensemble.RandomForestClassifier`)
- **Features:** Brand, Year, Color, Price, Mileage, Fuel Type, Horsepower
- **Labels:** `accepted` / `rejected`
- **Split:** 80% training / 20% testing
- **Trees:** Scales with your sample count (`n_estimators = n_samples`)

### Example Feature Importances
```
hp           0.259   ████████████
price        0.218   ██████████
year         0.144   ███████
mileage      0.130   ██████
brand        0.120   ██████
color        0.067   ███
fuel_type    0.061   ███
```

---

## Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create a branch** for your feature
```bash
git checkout -b feature/your-feature-name
```
3. **Commit your changes**
```bash
git commit -m "Add your feature description"
```
4. **Push to your branch**
```bash
git push origin feature/your-feature-name
```
5. **Open a Pull Request** on GitHub

### Ideas for contributions
- Add more car attributes (torque, engine size, number of seats)
- Export the trained model to a file so it persists between runs
- Add a model comparison mode (Random Forest vs XGBoost vs Logistic Regression)
- Build a web version with Flask or FastAPI
- Add a progress bar showing how many samples until the model is reliable

---

## Roadmap

- [x] Car generation and random pairing
- [x] Tkinter GUI for data collection
- [x] JSON dataset storage
- [x] Random Forest training pipeline
- [x] Feature importance visualization
- [x] Prediction GUI with confidence scores
- [ ] Persist trained model to disk
- [ ] Cross-validation for more reliable accuracy
- [ ] Web interface

---

## License

MIT — do whatever you want with it.

---

<p align="center">Built by <a href="https://github.com/EliWorkedOnThat">Eli</a></p>