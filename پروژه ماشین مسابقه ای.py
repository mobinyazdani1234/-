import random


class Car:
    def __init__(self, color, accel, decel, max_velocity, fuel_cap, fuel_use, prev_pos=0, start_fuel=0, refuel_time=0, total_fuel=0):
        self.color = color
        self.accel = accel
        self.decel = decel
        self.max_velocity_initial = max_velocity
        self.max_velocity = max_velocity
        self.velocity = 0
        self.position = 0
        self.fuel_cap = fuel_cap
        self.fuel_use = fuel_use
        self.fuel_level = start_fuel
        self.prev_pos = prev_pos
        self.refuel_time = refuel_time
        self.total_fuel = total_fuel
        self.refuel_stations = [100, 200, 300, 400]  

    def speed_up(self):
        fuel_ratio = (self.fuel_cap - self.fuel_level) / self.fuel_cap
        self.max_velocity = self.max_velocity_initial - 20 + (20 * fuel_ratio)
        if self.velocity + self.accel < self.max_velocity and self.refuel_time == 0:
            self.velocity += self.accel

    def slow_down(self):
        if self.velocity >= self.decel:
            self.velocity -= self.decel
        else:
            self.velocity = 0

    def travel(self, sec):
        for station in self.refuel_stations:
            if self.position < station and self.position + (self.velocity / 3600) >= station:
                self.decide_refuel(station, sec)
        if self.fuel_level > 0:
            if self.refuel_time > 0:
                self.refuel_time -= 1
                print(car_names[i], f"velocity={self.velocity} KM/h", f"position={self.position:.2f} KM", f"fuel level={self.fuel_level:.2f} liters", 'Refueling =', self.total_fuel)
            else:
                self.prev_pos = self.position
                self.position += (self.velocity / 3600)
                self.update_fuel_level()
                print(sec, car_names[i], f"velocity={self.velocity} KM/h", f"position={self.position:.2f} KM", f"fuel level={self.fuel_level:.2f} liters", 'Refueling =', self.total_fuel)
        else:
            print(car_names[i], "velocity=0", f"position={self.position:.2f} KM", "fuel level=out of fuel")

    def decide_refuel(self, station, sec):
        distance_left = 500 - self.position
        fuel_needed = (distance_left / 100) * self.fuel_use

        if self.fuel_level < fuel_needed:
            needed_fuel = fuel_needed - self.fuel_level
            if needed_fuel >= self.fuel_cap:
                needed_fuel = self.fuel_cap - self.fuel_level
            self.refuel(needed_fuel)
            while self.velocity > 0:
                self.slow_down()
            print(f"Approaching refuel station at {station} KM. Refueling {needed_fuel:.2f} liters. Total seconds: {sec}")

    def refuel(self, amount):
        if self.refuel_time == 0:
            self.fuel_level += amount
            self.refuel_time = int(amount)  
            self.total_fuel += amount
            print(f"Refueled {amount:.2f} liters. Current fuel level: {self.fuel_level:.2f} liters")

    def update_fuel_level(self):
        fuel_consumed = self.fuel_use * ((self.position - self.prev_pos) / 100)
        if self.fuel_level - fuel_consumed >= 0:
            self.fuel_level -= fuel_consumed
        else:
            self.fuel_level = 0
            self.velocity = 0


cars = [
    Car("Blue", 3, 6, 123, 36, 10, 4, 0),
    Car("Red", 4, 6, 130, 40, 9, 4, 0),
    Car("Green", 2, 6, 150, 50, 8, 4, 0),
    Car("Purple", 5, 6, 140, 60, 7, 4, 0),
    Car("Yellow", 3, 7, 125, 35, 10, 4, 0),
    Car("Orange", 4, 5, 135, 45, 9, 4, 0),
    Car("White", 5, 6, 145, 55, 8, 4, 0),
    Car("Black", 3, 6, 155, 65, 7, 4, 0),
    Car("Grey", 4, 8, 160, 75, 6, 4, 0),
    Car("Pink", 2, 7, 170, 85, 5, 4, 0)
]
car_names = ["car1", "car2", "car3", "car4", "car5", "car6", "car7", "car8", "car9", "car10"]


def configure_cars():
    i = 0
    for selected_car in cars:
        selected_color = random.choice(["red", "blue", 'green', "purple", "yellow", "orange", "white", "black", "grey", "pink"])
        selected_accel = random.randrange(2, 8)
        selected_decel = random.randrange(20, 80)
        selected_max_velocity = random.randrange(110, 221)
        selected_fuel_cap = random.choice([30, 40, 50, 60, 70, 80])
        selected_start_fuel = random.randrange(30, selected_fuel_cap + 1)
        selected_fuel_use = random.randrange(6, 16)

        selected_car.color = selected_color
        selected_car.accel = selected_accel
        selected_car.decel = selected_decel
        selected_car.max_velocity_initial = selected_max_velocity
        selected_car.max_velocity = selected_max_velocity
        selected_car.fuel_cap = selected_fuel_cap
        selected_car.fuel_use = selected_fuel_use
        selected_car.fuel_level = selected_start_fuel
        selected_car.initial_fuel = selected_start_fuel
        print(car_names[i], "color=", selected_car.color, "acceleration =", selected_car.accel, "deceleration =", selected_car.decel, "max velocity=", selected_car.max_velocity, "fuel capacity=", selected_car.fuel_cap, "fuel consumption=", selected_car.fuel_use, "initial fuel=", selected_car.initial_fuel)
        i += 1

configure_cars()
total_seconds = 0
key = input("start by typing 'start': ")
winner = None
winner_sec = 0


while key == 'start' and not winner:
    for sec in range(total_seconds + 1, total_seconds + 3601):
        for i in range(0, 10):
            cars[i].speed_up()
            cars[i].travel(sec)
            if cars[i].position >= 500:
                winner = car_names[i]
                winner_sec = sec
                key = 'q'
                break
        if key == 'q':
            break

    total_seconds += 3600
    if key != 'q' and not winner:
        key = input("Type 'start' to begin another round: ")


if winner:
    print(f"The winner is {winner}, who reached the destination in {winner_sec/3600:.2f} hours!")
else:
    print("No winner in this round.")
