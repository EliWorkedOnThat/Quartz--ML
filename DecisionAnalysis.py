import json
import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from CarGenerator import generate_random_cars

samples_path = r"C:\Users\mezin\Desktop\Quartz\Car_Preference_dataset"
n_samples = len([f for f in os.listdir(samples_path) if f.endswith('.json')])
rows = []

for filename in os.listdir(samples_path):
    if filename.endswith('.json'):
        with open(os.path.join(samples_path, filename)) as f:
            data = json.load(f)
        for car in data.values():
            rows.append(car)

print(f"Loaded {len(rows)} rows")

df = pd.DataFrame(rows)

le_brand  = LabelEncoder()
le_color  = LabelEncoder()
le_fuel   = LabelEncoder()
le_status = LabelEncoder()
le_transmission = LabelEncoder()

df['brand']     = le_brand.fit_transform(df['brand'])     # type: ignore
df['color']     = le_color.fit_transform(df['color'])     # type: ignore
df['fuel_type'] = le_fuel.fit_transform(df['fuel_type'])  # type: ignore
df['status']    = le_status.fit_transform(df['status'])   # type: ignore
df['transmission'] = le_transmission.fit_transform(df['transmission'])     # type: ignore

print(f"Status mapping: {dict(zip(le_status.classes_, le_status.transform(le_status.classes_)))}")  # type: ignore

X = df.drop(columns=['status'])
y = df['status']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = RandomForestClassifier(n_estimators=n_samples)
clf.fit(X_train, y_train)

print(f"Accuracy: {clf.score(X_test, y_test) * 100:.1f}%")

feature_names = ['brand', 'year', 'color', 'price', 'mileage', 'fuel_type', 'hp', 'num_seats', 'transmission', 'torque']

print("\nFeature Importances:")
for feature, importance in sorted(zip(feature_names, clf.feature_importances_), key=lambda x: x[1], reverse=True):
    print(f"  {feature:<12} {importance:.3f}")

test_cars = generate_random_cars()

print("\n--- Prediction Test ---")
for i, car in enumerate(test_cars):
    print(f"\nCar {i+1}: {car.brand} {car.year} | ${car.price:,} | {car.mileage:,} miles | {car.hp}HP | {car.fuel_type} | {car.color} | {car.transmission} | {car.num_seats} Seats | {car.torque} Nm")

rows_to_predict = []
for car in test_cars:
    rows_to_predict.append({
        "brand":     le_brand.transform([car.brand])[0],    # type: ignore
        "year":      car.year,
        "color":     le_color.transform([car.color])[0],    # type: ignore
        "price":     car.price,
        "mileage":   car.mileage,
        "fuel_type": le_fuel.transform([car.fuel_type])[0], # type: ignore
        "hp":        car.hp,
        "num_seats": car.num_seats,
        "transmission": le_transmission.transform([car.transmission])[0], # type: ignore
        "torque": car.torque
    })

predict_df = pd.DataFrame(rows_to_predict)

probabilities = clf.predict_proba(predict_df)

accepted_index = list(clf.classes_).index(le_status.transform(['accepted'])[0])  # type: ignore
car1_chance = probabilities[0][accepted_index]
car2_chance = probabilities[1][accepted_index]

winner = 0 if car1_chance > car2_chance else 1

print(f"\nModel predicts you'd pick: Car {winner + 1}")
w = test_cars[winner]
print(f"  Brand:     {w.brand}")
print(f"  Year:      {w.year}")
print(f"  Color:     {w.color}")
print(f"  Price:     ${w.price:,}")
print(f"  Mileage:   {w.mileage:,} miles")
print(f"  Fuel Type: {w.fuel_type}")
print(f"  HP:        {w.hp}HP")
print(f"  Number of seats: {w.num_seats}")
print(f"  Transmission: {w.transmission}")
print(f"  Torque: {w.torque}")

print(f"\nConfidence:")
print(f"  Car 1: {car1_chance * 100:.1f}%")
print(f"  Car 2: {car2_chance * 100:.1f}%")