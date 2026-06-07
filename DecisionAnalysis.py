import json
import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder

samples_path = r"C:\Users\mezin\Desktop\Quartz\Car_Preference_dataset"
rows = []

for filename in os.listdir(samples_path):
    if filename.endswith('.json'):
        with open(os.path.join(samples_path, filename)) as f:
            data = json.load(f)
        for car in data.values():
            rows.append(car)

print(f"Loaded {len(rows)} rows")

df = pd.DataFrame(rows)
pd.set_option('display.max_rows', None)
print(df)

le_brand = LabelEncoder()
le_color = LabelEncoder()
le_fuel = LabelEncoder()
le_status = LabelEncoder()

df['brand']     = le_brand.fit_transform(df['brand'])
df['color']     = le_color.fit_transform(df['color'])
df['fuel_type'] = le_fuel.fit_transform(df['fuel_type'])
df['status']    = le_status.fit_transform(df['status'])

print(df.head(10))
print(f"\nStatus mapping: {dict(zip(le_status.classes_, le_status.transform(le_status.classes_)))}")