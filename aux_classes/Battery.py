from aux_classes.HouseRequest import HouseRequest

class Battery:
    def __init__(self, charging_rate, discharge_rate,max_charge, owner_jid, charge_left = 0):
        self.owner = owner_jid
        self.charge_left = charge_left
        self.max_charge = max_charge
        self.charging_rate = charging_rate
        self.discharge_rate = discharge_rate

    def get_max_charge(self) -> int:
        return self.max_charge

    def get_charge_left(self) -> int:
        return self.charge_left
    
    def get_charging_rate(self) -> int:
        return self.charging_rate
    
    def get_discharge_rate(self) -> int:
        return self.discharge_rate
    
    def get_owner(self) -> str:
        return self.owner

    def charge(self, charge_amount: int):
        charge_amount = min(charge_amount, self.charging_rate)
        if self.charge_left + charge_amount > self.max_charge:
            self.charge_left = self.max_charge
        else: 
            self.charge_left += charge_amount
        print("Battery: {}kWh charged with {} kWh".format(self.charge_left, charge_amount))


    def discharge(self, request: HouseRequest):
        discharge = min(request.getEnergyNeeded(), self.discharge_rate)
        if self.charge - discharge > 0:
            self.charge -= self.discharge_rate
            return discharge()
        else:
            ret = self.charge
            self.charge = 0
            return ret
        
    def __lt__(self, obj): 
        return self.charge_left < obj.charge_left
  
    def __gt__(self, obj): 
        return self.charge_left > obj.charge_left
  
    def __le__(self, obj): 
        return self.charge_left <= obj.charge_left
  
    def __ge__(self, obj): 
        return self.charge_left >= obj.charge_left
  
    def __eq__(self, obj):
        return self.charge_left == obj.charge_left

    def __str__(self):
        return "Capacity: " + str(self.capacity) + " Charge: " + str(self.charge)