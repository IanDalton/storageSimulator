# Entrada.py
import salabim as sim
import csv
from datetime import datetime

from components.ArrivalProcess import ArrivalProcess


class ArrivalGenerator(sim.Component):
    def __init__(self, csv_file, almacen):
        super().__init__()
        self.csv_file = csv_file
        self.almacen = almacen

    def process(self):
        # Reference start time for the simulation
        yield self.hold(0)
        sim_start = None
        with open(self.csv_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            data = dict()
            for row in reader:
                if row['id_viaje'] not in data:
                    # Si no existe el id_viaje en el diccionario, se crea una nueva lista
                    # La lista tiene dos cosas: El horario y una lista con los datos con los datos
                    # La lista luego se convierte en un DataFrame
                    hora = row['hora']
                    fecha = row['fecha']
                    dt = datetime.strptime(
                        fecha + ' ' + hora, '%d/%m/%Y %H:%M:%S')
                    if sim_start is None:
                        sim_start = dt  # Set the reference start time to the first even
                    arrival_time = (dt - sim_start).total_seconds() / 3600
                    
                    data[row['id_viaje']] = {
                        "arrival_time": arrival_time, "data": [row]}

                else:
                    # Si ya existe el id_viaje, se agrega a la lista de datos
                    data[row['id_viaje']]["data"].append(row)

            for value in data.values():
                # Create an arrival process for each trip
                ArrivalProcess(arrivals=value["data"], almacen=self.almacen).activate(
                    at=value["arrival_time"])
        




