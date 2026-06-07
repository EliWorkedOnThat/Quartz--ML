#In this file we will generate 2 cars with different features to gather info for the user
#Imports
import random

#Car Class to represent a car with its attributes
class Car:
    def __init__(self, brand, year, color, price, mileage, fuel_type):
        self.brand = brand
        self.year = year
        self.color = color
        self.price = price
        self.mileage = mileage
        self.fuel_type = fuel_type

#Function to generate 2 random cars and print their details for the user to choose
def generate_random_cars():
    brands = ['Toyota', 'Honda', 'Ford', 'Chevrolet', 'BMW']
    colors = ['Red', 'Blue', 'Black', 'White', 'Silver']
    fuel_types = ['Gasoline', 'Diesel', 'Electric', 'Hybrid']

    cars = []
    for i in range(2):
        brand = random.choice(brands)
        year = random.randint(2000, 2022)
        color = random.choice(colors)
        price = random.randint(5000, 50000)
        mileage = random.randint(0, 200000)
        fuel_type = random.choice(fuel_types)

        car = Car(brand, year, color, price, mileage, fuel_type)
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

def choose_car(cars):
    while True:
        choice = input("\nPlease choose a car by entering 1 or 2: ")
        if choice == '1':
            print("\nYou have chosen Car 1.")
            print(f"  Brand:     {cars[0].brand}")
            print(f"  Year:      {cars[0].year}")
            print(f"  Color:     {cars[0].color}")
            print(f"  Price:     ${cars[0].price}")
            print(f"  Mileage:   {cars[0].mileage} miles")
            print(f"  Fuel Type: {cars[0].fuel_type}")
            break
        elif choice == '2':
            print("\nYou have chosen Car 2.")
            print(f"  Brand:     {cars[1].brand}")
            print(f"  Year:      {cars[1].year}")
            print(f"  Color:     {cars[1].color}")
            print(f"  Price:     ${cars[1].price}")
            print(f"  Mileage:   {cars[1].mileage} miles")
            print(f"  Fuel Type: {cars[1].fuel_type}")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

try:
    cars = generate_random_cars()
    display_cars(cars)
    choose_car(cars)
except Exception as e:
    print(f"An error occurred while generating cars: {e}")