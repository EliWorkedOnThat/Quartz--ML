from CarGenerator import Car
from sklearn.ensemble import RandomForestClassifier
import os 

samples_path = r"C:\Users\mezin\Desktop\Quartz\Car_Preference_dataset"
n_samples = len([f for f in os.listdir(samples_path) if f.endswith('.json')])

clf = RandomForestClassifier(n_estimators=n_samples)