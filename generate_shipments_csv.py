import csv
import random
import datetime
 
 # Crear datos para Shipments y escribir en un CSV
today_date = datetime.date.today().isoformat()
line_ids = list(range(1, 101))
random.shuffle(line_ids)
with open('shipments.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['shipment_id', 'date', 'client_id', 'location_id', 'line_id'])
    
    for shipment_id in range(1, 101):
        client_id = random.randint(1, 10)
        location_id = random.randint(1, 67)
        line_id = line_ids.pop()
        writer.writerow([shipment_id, today_date, client_id, location_id, line_id])

print("CSV con Shipments creado correctamente.")
