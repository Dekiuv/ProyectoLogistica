import csv
import random
import datetime 
from Models import Constant
# Crear CSV con Constants y escribir un solo registro
with open('constants.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['constant_id', 'velocity', 'workday_time', 'rest_time', 'drivers_hourly_pay', 'fuel_cost_km', 'truck_capacity'])
    constant_record = Constant(constant_id=1, velocity=60.0, workday_time=8, rest_time=2, drivers_hourly_pay=20.0, fuel_cost_km=1.5, truck_capacity=20000)
    writer.writerow([constant_record.constant_id, constant_record.velocity, constant_record.workday_time, constant_record.rest_time, constant_record.drivers_hourly_pay, constant_record.fuel_cost_km, constant_record.truck_capacity])

print("CSV con Constants creado correctamente.")
