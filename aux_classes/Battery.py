from aux_classes.HouseRequest import HouseRequest

class Battery:
    def __init__(self, capacity: int, charging_rate, discharge_rate,max_charge):
        self.capacity = capacity
        self.max_charge = max_charge
        self.charging_rate = charging_rate
        self.discharge_rate = discharge_rate

    def get_capacity(self) -> int:
        return self.capacity

    def get_charge(self) -> int:
        return self.charge

    def charge(self, charge_amount: int):
        if self.charge + charge_amount > self.capacity:
            self.charge = self.capacity
        else: 
            self.charge += charge_amount


    def discharge(self, request: HouseRequest):
        discharge = request.getEnergyNeeded()
        if request > self.discharge_rate:
                discharge = self.discharge_rate
        if self.charge - discharge > 0:
            self.charge -= self.discharge_rate
            return discharge()
        else:
            ret = self.charge
            self.charge = 0
            return ret

    def __str__(self):
        return "Capacity: " + str(self.capacity) + " Charge: " + str(self.charge)