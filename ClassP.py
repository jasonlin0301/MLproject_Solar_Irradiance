class SolarSystem:
    def __init__(self, system_capacity, efficiency, esh, energy_demand):
        self.system_capacity = system_capacity  # 系統容量 (kW)
        self.efficiency = efficiency  # 系統效率
        self.esh = esh  # 等效日射小時 (hours/day)
        self.energy_demand = energy_demand  # 每日能量需求 (kWh/day)

    def calculate_system_capacity(self):
        # 計算所需的系統容量 P
        P = self.system_capacity * self.efficiency * self.esh / self.energy_demand
        return P

    def calculate_energy_demand(self):
        # 計算每日能量需求 E
        E = self.system_capacity * self.efficiency * self.esh
        return E

# 使用示例
system_capacity = 8  # kW
efficiency = 0.75  # 系統效率
esh = 5  # 等效日射小時 (hours/day)
energy_demand = 30  # 每日能量需求 (kWh/day)

solar_system = SolarSystem(system_capacity, efficiency, esh, energy_demand)

# 計算所需的系統容量
required_capacity = solar_system.calculate_system_capacity()
print(f'Required System Capacity: {required_capacity:.2f} kW')

# 計算每日能量需求
daily_energy = solar_system.calculate_energy_demand()
print(f'Daily Energy Production: {daily_energy:.2f} kWh')
