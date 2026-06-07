import json
import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

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

le_brand = LabelEncoder() 
le_color = LabelEncoder()
le_fuel = LabelEncoder()
le_status = LabelEncoder()

df['brand']     = le_brand.fit_transform(df['brand'])    # type: ignore
df['color']     = le_color.fit_transform(df['color'])    # type: ignore
df['fuel_type'] = le_fuel.fit_transform(df['fuel_type'])   # type: ignore
df['status']    = le_status.fit_transform(df['status'])   # type: ignore

pd.set_option('display.max_rows', None)
print(df)
print(f"\nStatus mapping: {dict(zip(le_status.classes_, le_status.transform(le_status.classes_)))}")   # type: ignore

x = df.drop(columns = ['status'])
y = df['status']

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

clf = RandomForestClassifier(n_estimators = n_samples)
clf.fit(X_train, y_train)

print(f"Accuracy: {clf.score(X_test, y_test) * 100:.1f}%")

feature_names = ['brand', 'year', 'color', 'price', 'mileage', 'fuel_type', 'hp']

print("\nFeature Importances:")
for feature, importance in sorted(zip(feature_names, clf.feature_importances_), key=lambda x: x[1], reverse=True):
    print(f"  {feature:<12} {importance:.3f}")