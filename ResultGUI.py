import tkinter as tk
from tkinter import font
import json
import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from CarGenerator import generate_random_cars

BG       = "#0f0f0f"
CARD_BG  = "#1a1a1a"
ACCENT   = "#22c55e"
DIM      = "#ef4444"
TEXT     = "#f1f1f1"
SUBTEXT  = "#888888"
GOLD     = "#facc15"

def train_model():
    samples_path = r"C:\Users\mezin\Desktop\Quartz\Car_Preference_dataset"
    n_samples = len([f for f in os.listdir(samples_path) if f.endswith('.json')])
    rows = []

    for filename in os.listdir(samples_path):
        if filename.endswith('.json'):
            with open(os.path.join(samples_path, filename)) as f:
                data = json.load(f)
            for car in data.values():
                rows.append(car)

    df = pd.DataFrame(rows)

    le_brand  = LabelEncoder()
    le_color  = LabelEncoder()
    le_fuel   = LabelEncoder()
    le_status = LabelEncoder()

    df['brand']     = le_brand.fit_transform(df['brand'])     # type: ignore
    df['color']     = le_color.fit_transform(df['color'])     # type: ignore
    df['fuel_type'] = le_fuel.fit_transform(df['fuel_type'])  # type: ignore
    df['status']    = le_status.fit_transform(df['status'])   # type: ignore

    X = df.drop(columns=['status'])
    y = df['status']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    clf = RandomForestClassifier(n_estimators=n_samples)
    clf.fit(X_train, y_train)

    accuracy = clf.score(X_test, y_test) * 100

    feature_names = ['brand', 'year', 'color', 'price', 'mileage', 'fuel_type', 'hp']
    importances = sorted(zip(feature_names, clf.feature_importances_), key=lambda x: x[1], reverse=True)

    return clf, le_brand, le_color, le_fuel, le_status, accuracy, importances, n_samples

def predict(clf, le_brand, le_color, le_fuel, le_status, cars):
    rows_to_predict = []
    for car in cars:
        rows_to_predict.append({
            "brand":     le_brand.transform([car.brand])[0],    # type: ignore
            "year":      car.year,
            "color":     le_color.transform([car.color])[0],    # type: ignore
            "price":     car.price,
            "mileage":   car.mileage,
            "fuel_type": le_fuel.transform([car.fuel_type])[0], # type: ignore
            "hp":        car.hp
        })

    predict_df = pd.DataFrame(rows_to_predict)
    probabilities = clf.predict_proba(predict_df)
    accepted_index = list(clf.classes_).index(le_status.transform(['accepted'])[0])  # type: ignore

    car1_chance = probabilities[0][accepted_index]
    car2_chance = probabilities[1][accepted_index]
    winner = 0 if car1_chance > car2_chance else 1

    return winner, car1_chance * 100, car2_chance * 100


class ResultGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Car Prediction")
        self.root.configure(bg=BG)
        self.root.geometry("960x700")
        self.root.resizable(False, False)

        self.title_font    = font.Font(family="Courier New", size=16, weight="bold")
        self.header_font   = font.Font(family="Courier New", size=13, weight="bold")
        self.label_font    = font.Font(family="Courier New", size=11, weight="bold")
        self.subtext_font  = font.Font(family="Courier New", size=9)
        self.imp_font      = font.Font(family="Courier New", size=10, weight="bold")

        self.clf, self.le_brand, self.le_color, self.le_fuel, self.le_status, \
            self.accuracy, self.importances, self.n_samples = train_model()

        self.build_ui()
        self.run_prediction()

    def build_ui(self):
        # Top bar
        top = tk.Frame(self.root, bg=BG)
        top.pack(fill="x", padx=32, pady=(20, 0))

        tk.Label(top, text="CAR PREDICTION ENGINE", font=self.title_font,
                 bg=BG, fg=TEXT).pack(side="left")

        stats_frame = tk.Frame(top, bg=BG)
        stats_frame.pack(side="right")

        tk.Label(stats_frame, text=f"SAMPLES: {self.n_samples}",
                 font=self.subtext_font, bg=BG, fg=SUBTEXT).pack(side="left", padx=12)
        tk.Label(stats_frame, text=f"ACCURACY: {self.accuracy:.1f}%",
                 font=self.subtext_font, bg=BG, fg=ACCENT).pack(side="left", padx=12)

        tk.Frame(self.root, bg="#2a2a2a", height=1).pack(fill="x", padx=32, pady=12)

        # Cards row
        cards_row = tk.Frame(self.root, bg=BG)
        cards_row.pack(fill="x", padx=32)

        self.card_widgets = []
        for i in range(2):
            card = tk.Frame(cards_row, bg=CARD_BG, highlightthickness=2,
                            highlightbackground="#2a2a2a")
            card.grid(row=0, column=i, padx=12, sticky="nsew")
            cards_row.columnconfigure(i, weight=1)

            header = tk.Label(card, text=f"CAR {i+1}", font=self.header_font,
                              bg=CARD_BG, fg=SUBTEXT)
            header.pack(pady=(16, 8))

            fields = ["Brand", "Year", "Color", "Price", "Mileage", "Fuel Type", "HP"]
            labels = {}
            for field in fields:
                row = tk.Frame(card, bg=CARD_BG)
                row.pack(fill="x", padx=20, pady=2)
                tk.Label(row, text=f"{field}:", font=self.label_font,
                         bg=CARD_BG, fg=SUBTEXT, width=11, anchor="w").pack(side="left")
                val = tk.Label(row, text="—", font=self.label_font,
                               bg=CARD_BG, fg=TEXT, anchor="w")
                val.pack(side="left")
                labels[field] = val

            conf_label = tk.Label(card, text="", font=self.imp_font, bg=CARD_BG, fg=SUBTEXT)
            conf_label.pack(pady=(10, 16))

            self.card_widgets.append({
                "card": card, "header": header, "labels": labels, "conf": conf_label
            })

        # Winner banner
        self.winner_var = tk.StringVar(value="")
        self.winner_label = tk.Label(self.root, textvariable=self.winner_var,
                                     font=self.title_font, bg=BG, fg=GOLD)
        self.winner_label.pack(pady=(16, 4))

        tk.Frame(self.root, bg="#2a2a2a", height=1).pack(fill="x", padx=32, pady=8)

        # Feature importances
        tk.Label(self.root, text="WHAT THE MODEL LEARNED ABOUT YOU",
                 font=self.subtext_font, bg=BG, fg=SUBTEXT).pack()

        imp_row = tk.Frame(self.root, bg=BG)
        imp_row.pack(pady=8)

        for feature, importance in self.importances:
            col = tk.Frame(imp_row, bg=BG)
            col.pack(side="left", padx=10)
            tk.Label(col, text=f"{importance*100:.1f}%", font=self.imp_font,
                     bg=BG, fg=ACCENT).pack()
            tk.Label(col, text=feature.upper(), font=self.subtext_font,
                     bg=BG, fg=SUBTEXT).pack()

        tk.Frame(self.root, bg="#2a2a2a", height=1).pack(fill="x", padx=32, pady=8)

        # Next button
        btn = tk.Button(self.root, text="PREDICT NEXT PAIR",
                        font=self.header_font, bg=ACCENT, fg=BG,
                        relief="flat", cursor="hand2", pady=8, padx=24,
                        command=self.run_prediction)
        btn.pack(pady=(4, 16))
        btn.bind("<Enter>", lambda e: btn.config(bg="#16a34a"))
        btn.bind("<Leave>", lambda e: btn.config(bg=ACCENT))

    def run_prediction(self):
        self.cars = generate_random_cars()
        winner, c1, c2 = predict(self.clf, self.le_brand, self.le_color,
                                  self.le_fuel, self.le_status, self.cars)

        specs = [
            ("Brand",     lambda c: c.brand),
            ("Year",      lambda c: str(c.year)),
            ("Color",     lambda c: c.color),
            ("Price",     lambda c: f"${c.price:,}"),
            ("Mileage",   lambda c: f"{c.mileage:,} miles"),
            ("Fuel Type", lambda c: c.fuel_type),
            ("HP",        lambda c: f"{c.hp} HP"),
        ]

        confidences = [c1, c2]
        for i, car in enumerate(self.cars):
            w = self.card_widgets[i]
            is_winner = (i == winner)

            highlight = ACCENT if is_winner else DIM
            w["card"].config(highlightbackground=highlight)
            w["header"].config(fg=highlight)
            w["conf"].config(text=f"CONFIDENCE: {confidences[i]:.1f}%", fg=highlight)

            for field, getter in specs:
                w["labels"][field].config(text=getter(car))

        self.winner_var.set(f"★  MODEL PICKS CAR {winner + 1}  ★")


if __name__ == "__main__":
    root = tk.Tk()
    app = ResultGUI(root)
    root.mainloop()