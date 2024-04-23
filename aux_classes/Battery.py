
class Battery:
    def __init__(self, capacity: int, charge: int):
        self.capacity = capacity
        self.charge = charge

    def get_capacity(self) -> int:
        return self.capacity

    def get_charge(self) -> int:
        return self.charge

    def set_charge(self, charge: int):
        self.charge = charge

    def charge_battery(self, charge: int):
        self.charge += charge
        if self.charge > self.capacity:
            self.charge = self.capacity

    def discharge_battery(self, discharge: int):
        self.charge -= discharge
        if self.charge < 0:
            self.charge = 0

    def __str__(self):
        return "Capacity: " + str(self.capacity) + " Charge: " + str(self.charge)