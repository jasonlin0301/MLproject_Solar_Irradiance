# E = 30  # 每日能量需求 (kWh/day)
# I = 5  # 日射量 (kWh/m²/day)
# η = 0.75  # 系統效率
# ESH = 5  # 等效日射小時 (hours/day)

# # 計算系統規模
# P = E / (I * η * ESH)

class SolarSystemscale:
    def __init__(self, daily_energy_demand, system_efficiency, equivalent_sun_hours):
        self.daily_energy_demand = daily_energy_demand  # 每日能量需求 (kWh/day)
        self.system_efficiency = system_efficiency  # 系統效率
        self.equivalent_sun_hours = equivalent_sun_hours  # 等效日射小時 (hours/day)

    def calculate_system_size(self):
        # 計算系統規模
        system_size = self.daily_energy_demand / (self.system_efficiency * self.equivalent_sun_hours)
        return system_size

# 使用示例
daily_energy_demand = 30  # 每日能量需求 (kWh/day)
system_efficiency = 0.75  # 系統效率
equivalent_sun_hours = 5  # 等效日射小時 (hours/day)

solar_system = SolarSystemscale(daily_energy_demand, system_efficiency, equivalent_sun_hours)
system_size = solar_system.calculate_system_size()
print(f"所需的太陽能系統規模: {system_size} kW")


