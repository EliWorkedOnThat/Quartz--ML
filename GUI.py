import tkinter as tk
from tkinter import font
from CarGenerator import Car, generate_random_cars, save_to_dataset

BG        = "#0f0f0f"
CARD_BG   = "#1a1a1a"
ACCENT_L  = "#3b82f6"
ACCENT_R  = "#f97316"
TEXT      = "#f1f1f1"
SUBTEXT   = "#888888"
BTN_HVR_L = "#2563eb"
BTN_HVR_R = "#ea6c0a"

class CarGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Car Selector")
        self.root.configure(bg=BG)
        self.root.geometry("900x720")
        self.root.resizable(False, False)

        self.cars = []
        self.build_ui()
        self.load_new_cars()

        self.root.bind("<Left>",  lambda e: self.choose(0))
        self.root.bind("<Right>", lambda e: self.choose(1))

    def build_ui(self):
        title_font  = font.Font(family="Courier New", size=18, weight="bold")
        header_font = font.Font(family="Courier New", size=14, weight="bold")
        label_font  = font.Font(family="Courier New", size=13, weight="bold")
        hint_font   = font.Font(family="Courier New", size=11)

        tk.Label(self.root, text="CHOOSE YOUR CAR", font=title_font,
                 bg=BG, fg=TEXT).pack(pady=(24, 4))

        tk.Label(self.root, text="← left arrow   right arrow →",
                 font=hint_font, bg=BG, fg=SUBTEXT).pack(pady=(0, 16))

        cards_frame = tk.Frame(self.root, bg=BG)
        cards_frame.pack(fill="both", expand=True, padx=32)

        self.card_frames = []
        self.stat_labels = []
        accents = [ACCENT_L, ACCENT_R]
        hovers  = [BTN_HVR_L, BTN_HVR_R]
        labels  = ["CAR 1", "CAR 2"]

        for i in range(2):
            col = tk.Frame(cards_frame, bg=BG)
            col.grid(row=0, column=i, padx=16, sticky="nsew")
            cards_frame.columnconfigure(i, weight=1)

            card = tk.Frame(col, bg=CARD_BG, bd=0, highlightthickness=2,
                            highlightbackground=accents[i])
            card.pack(fill="both", expand=True, pady=4)

            tk.Label(card, text=labels[i], font=header_font,
                     bg=CARD_BG, fg=accents[i]).pack(pady=(20, 12))

            stats_frame = tk.Frame(card, bg=CARD_BG)
            stats_frame.pack(padx=24, pady=4, fill="x")

            fields = ["Brand", "Year", "Color", "Price", "Mileage", "Fuel Type", "Horsepower","Number of Seats", "Transmission", "Torque"]
            car_labels = {}
            for field in fields:
                row = tk.Frame(stats_frame, bg=CARD_BG)
                row.pack(fill="x", pady=3)
                tk.Label(row, text=f"{field}:", font=label_font,
                         bg=CARD_BG, fg=SUBTEXT, width=12, anchor="w").pack(side="left")
                val_lbl = tk.Label(row, text="—", font=label_font,
                                   bg=CARD_BG, fg=TEXT, anchor="w")
                val_lbl.pack(side="left")
                car_labels[field] = val_lbl

            self.stat_labels.append(car_labels)

            btn = tk.Button(card, text=f"CHOOSE  CAR {i+1}",
                            font=header_font, bg=accents[i], fg=BG,
                            relief="flat", cursor="hand2", pady=10,
                            command=lambda idx=i: self.choose(idx))
            btn.pack(fill="x", padx=24, pady=(16, 20))

            btn.bind("<Enter>", lambda e, b=btn, h=hovers[i]: b.config(bg=h))
            btn.bind("<Leave>", lambda e, b=btn, a=accents[i]: b.config(bg=a))

            self.card_frames.append(card)

        self.status_var = tk.StringVar(value="")
        tk.Label(self.root, textvariable=self.status_var, font=hint_font,
                 bg=BG, fg=SUBTEXT).pack(pady=(8, 16))

    def load_new_cars(self):
        self.cars = generate_random_cars()
        fields_map = {
            "Brand":      lambda c: c.brand,
            "Year":       lambda c: str(c.year),
            "Color":      lambda c: c.color,
            "Price":      lambda c: f"${c.price:,}",
            "Mileage":    lambda c: f"{c.mileage:,} miles",
            "Fuel Type":  lambda c: c.fuel_type,
            "Horsepower": lambda c: f"{c.hp} HP",
            "Number of Seats": lambda c: str(c.num_seats),
            "Transmission": lambda c: c.transmission,
            "Torque": lambda c: f"{c.torque} Nm",
        }
        for i, car in enumerate(self.cars):
            for field, getter in fields_map.items():
                self.stat_labels[i][field].config(text=getter(car))

        self.status_var.set("")

    def choose(self, idx):
        accepted = self.cars[idx]
        rejected = self.cars[1 - idx]
        save_to_dataset(accepted, rejected)
        self.status_var.set(f"✓ Car {idx + 1} saved — loading next pair...")
        self.root.after(600, self.load_new_cars)

if __name__ == "__main__":
    root = tk.Tk()
    app = CarGUI(root)
    root.mainloop()