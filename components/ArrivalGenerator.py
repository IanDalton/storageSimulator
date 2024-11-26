# Entrada.py
import salabim as sim
import csv
from datetime import datetime

from components.Equipo import Equipo
from components.Pallet import Pallet
from components.Porton import Porton
from components.Sector import Sector
from components.Shelf import Shelf
from components.utils import calculate_distance
from main import almacen


class ArrivalGenerator(sim.Component):
    def __init__(self, csv_file):
        super().__init__()
        self.csv_file = csv_file

    def process(self):
        # Reference start time for the simulation
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
                    arrival_time = (dt - sim_start).total_seconds() / 3600
                    if sim_start is None:
                        sim_start = dt  # Set the reference start time to the first even
                    data[row['id_viaje']] = {
                        "arrival_time": arrival_time, "data": [row]}

                else:
                    # Si ya existe el id_viaje, se agrega a la lista de datos
                    data[row['id_viaje']]["data"].append(row)

            for value in data.values():
                # Create an arrival process for each trip
                ArrivalProcess(arrivals=value["data"]).activate(
                    at=value["arrival_time"])


class ArrivalProcess(sim.Component):
    def __init__(self, arrivals):
        super().__init__()
        self.arrivals = arrivals

    def process(self):
        movimiento = self.arrivals[0]['movimiento']
        porton: Porton = None
        if movimiento.lower() == 'recepción':
            porton = almacen.portones['Ingreso']
        elif movimiento.lower() == 'salidas':
            porton = almacen.portones['Salida']

        yield self.request(porton)

        for arrival in self.arrivals:
            material = arrival['material']
            movimiento = arrival['movimiento']  # 'Recepción' or 'Salidas'
            # TODO: conseguir almacenamiento
            almacenamiento = None
            pallet = Pallet(sku=material, sector=almacenamiento)

            if movimiento.lower() == 'recepción':
                # Simulate the entry process
                # Select the appropriate equipment
                zorra = almacen.equipos["Zorra"]

                yield self.request(zorra)
                yield self.hold(zorra.get_time_to_location(porton.posicion)/3600)
                yield from self.procesar_entrada(pallet, porton)
                self.release(zorra)
                
                TransportProcess(pallet, porton,"entrada").activate()

            elif movimiento.lower() == 'salidas':
                # Simulate the exit process
                yield from self.procesar_salida(pallet, porton)

        self.release(porton)

    def procesar_entrada(self, pallet: Pallet, porton: Porton):
        
        # Simulate picking up the pallet (16 seconds)
        yield self.hold(16 / 3600)
        # Simulate scanning the pallet (15 seconds)
        yield self.hold(15 / 3600)

    def procesar_salida(self, pallet: Pallet, porton: Porton):
        # Simulate picking up the pallet from storage
        sector = almacen.sectores[pallet.sector]
        removed_pallet = sector.almacenamiento[0].remove_pallet()
        if removed_pallet:
            # Simulate picking up the pallet (16 seconds)
            yield self.hold(16 / 3600)

            # Calculate travel time to exit
            origen = self.obtener_destino(pallet)
            destino = (0, 0)  # Exit point
            distancia = self.calcular_distancia(origen, destino)
            tiempo_viaje = distancia / 1.82 / 3600
            yield self.hold(tiempo_viaje)

            # Place the pallet at exit point (16 seconds)
            yield self.hold(16 / 3600)

    def obtener_destino(self, pallet):
        # Get the storage location coordinates
        sector = almacen.sectores[pallet.sector]
        return sector.posicion

    def calcular_distancia(self, origen, destino):
        dx = abs(destino[0] - origen[0])
        dy = abs(destino[1] - origen[1])
        return dx + dy  # Manhattan distance


class TransportProcess(sim.Component):
    def __init__(self, pallet, porton,type):
        super().__init__()
        self.pallet: Pallet = pallet
        self.porton: Porton = porton
        self.transport = None
        self.type = type

    def process(self):
        # Calculate travel time to exit
        

        origen = self.porton.posicion
        if self.type == "entrada":
            shelf,sector = self.obtain_empty_shelf()
        else:
            shelf,sector = self.obtain_material()
        shelf: Shelf
        # Obtain the destination absolute coordinates
        destino = (shelf.posicion[0]+ sector.posicion[0],shelf.posicion[1]+sector.posicion[1])
        floor = shelf.locate_empty()
        height = floor*shelf.shelf_height

        if height < almacen.equipos["Autoelevador"][0].altura_maxima:
            self.transport = almacen.equipos["Autoelevador"]
        elif height < almacen.equipos["Reach Baja"][0].altura_maxima:
            self.transport = almacen.equipos["Reach Baja"]
        else:
            self.transport = almacen.equipos["Reach Alta"]
        
        if self.type != "entrada": # Redundant, it is just to make it easier to read
            origen,destino = destino,origen
        
        yield self.request(self.transport)
        self.transport: Equipo
        yield self.hold(self.transport.get_time_to_location(origen)/3600) # Travel to destination
        # Pick up the pallet
        yield self.hold(16/3600)

        # Travel to the shelf
        yield self.hold(self.transport.get_time_to_location(destino)/3600)

        # Travel to the floor
        yield self.hold((height/self.transport.velocidad)/3600)
        
        # Place the pallet
        yield self.hold(16/3600)
        if self.type == "entrada":
            shelf.add_pallet(self.pallet,floor)
        else:
            shelf.remove_pallet(self.pallet,floor)

        self.release(self.transport)
        self.transport = None


    def obtain_material(self):
        sector:Sector
        nearest_shelf = None
        nearest_sector = None
        distance = None
        for sector in almacen.sectores[self.pallet.sector]:

            shelf,floor = sector.locate(self.pallet.material)
            if shelf is not None:
                if nearest_shelf is None:
                    nearest_shelf = shelf
                    distance = sector.calculate_distance_to_floor(self.transport.posicion,shelf,floor)
                    nearest_sector = sector
                else:
                    calculated_distance = sector.calculate_distance_to_floor(self.transport.posicion,shelf,floor)
                    if calculated_distance < distance:
                        nearest_shelf = shelf
                        distance = calculated_distance
                        nearest_sector = sector
                    
        return nearest_shelf,nearest_sector


    
    def obtain_empty_shelf(self)-> Shelf:
        sector = self.get_nearest_sector(self.porton.posicion)
        shelf = sector.get_open_shelf(self.porton.posicion)
        if shelf is None:
            for sector in almacen.sectores:
                shelf = sector.get_open_shelf(self.porton.posicion)
                if shelf is not None:
                    break
        return shelf,sector
    
    def get_nearest_sector(self,origin)->Sector|None:
        nearest_sector = None
        nearest_distance = None
        for sector in almacen.sectores[self.pallet.sector]:
            if nearest_sector is None:
                nearest_sector = sector
                nearest_distance = calculate_distance(origin,sector.posicion)
            else:
                if calculate_distance(origin,sector.posicion) < nearest_distance:
                    nearest_sector = sector
                    nearest_distance = calculate_distance(origin,sector.posicion)
        return nearest_sector
    
        
