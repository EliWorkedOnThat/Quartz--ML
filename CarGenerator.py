import random
import os
import json
from typing import Any

class Car:
    def __init__(self, brand, year, color, price, mileage, fuel_type , hp):
        self.brand = brand
        self.year = year
        self.color = color
        self.price = price
        self.mileage = mileage
        self.fuel_type = fuel_type
        self.hp = hp

def generate_random_cars():
    brands = ['Toyota', 'Honda', 'Ford', 'Chevrolet', 'BMW']
    colors = ['Red', 'Blue', 'Black', 'White', 'Silver']
    fuel_types = ['Gasoline', 'Diesel', 'Electric', 'Hybrid']

    cars = []
    for i in range(2):
        car = Car(
            random.choice(brands),
            random.randint(2000, 2022),
            random.choice(colors),
            random.randint(5000, 50000),
            random.randint(0, 200000),
            random.choice(fuel_types),
            random.randint(100, 800)
        )
        cars.append(car)
    return cars

def display_cars(cars):
    for i, car in enumerate(cars):
        print(f"\nCar {i+1}:")
        print(f"  Brand:     {car.brand}")
        print(f"  Year:      {car.year}")
        print(f"  Color:     {car.color}")
        print(f"  Price:     ${car.price}")
        print(f"  Mileage:   {car.mileage} miles")
        print(f"  Fuel Type: {car.fuel_type}")
        print(f"  Horsepower: {car.hp} HP")

def choose_car(cars):
    while True:
        choice = input("\nPlease choose a car by entering 1 or 2: ")
        if choice == '1':
            print("\nYou have chosen Car 1.")
            return cars[0], cars[1]
        elif choice == '2':
            print("\nYou have chosen Car 2.")
            return cars[1], cars[0]
        else:
            print("Invalid choice. Please enter 1 or 2.")

def car_to_dict(car) -> dict[str, Any]:
    return {
        "brand":     car.brand,
        "year":      car.year,
        "color":     car.color,
        "price":     car.price,
        "mileage":   car.mileage,
        "fuel_type": car.fuel_type,
        "hp":        car.hp
    }

def save_to_dataset(accepted, rejected, folder_path="PATH/TO/DATASET/FOLDER"):
    os.makedirs(folder_path, exist_ok=True)

    existing_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    next_index = len(existing_files) + 1

    entry = {
        "car_1": {**car_to_dict(accepted), "status": "accepted"},
        "car_2": {**car_to_dict(rejected), "status": "rejected"}
    }

    file_path = os.path.join(folder_path, f"Car_{next_index}.json")
    with open(file_path, 'w') as f:
        json.dump(entry, f, indent=4)

    print(f"\nPreference saved as Car_{next_index}.json")
    print(f"Saved to: '{file_path}'")

try:
    while True:
        cars = generate_random_cars()
        display_cars(cars)
        accepted, rejected = choose_car(cars)
        save_to_dataset(accepted, rejected)

except KeyboardInterrupt:
    print("\nThanks for your input! Exiting.")
except Exception as e:
    print(f"An error occurred while generating cars: {e}")