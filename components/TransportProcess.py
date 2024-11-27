from components.Equipo import Equipo
from components.Pallet import Pallet
from components.Porton import Porton
from components.Sector import Sector
from components.Shelf import Shelf
from components.utils import calculate_distance


import salabim as sim


import csv
import os


class TransportProcess(sim.Component):
    def __init__(self, pallet, porton, type, almacen, callback=None):
        super().__init__()
        self.pallet: Pallet = pallet
        self.porton: Porton = porton
        self.transport = None
        self.type = type
        self.almacen = almacen
        self.callback = callback



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

        if height < self.almacen.equipos["Autoelevador"][0].altura_maxima:
            self.transport = self.almacen.equipos["Autoelevador"]
        elif height < self.almacen.equipos["Reach Baja"][0].altura_maxima:
            self.transport = self.almacen.equipos["Reach Baja"]
        else:
            self.transport = self.almacen.equipos["Reach Alta"]

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

        if self.callback:
            yield self.wait(self.callback())

        if self.type =="entrada":
            self.pallet.store_end_time = sim.now()
        else:
            self.pallet.retrieve_end_time = sim.now()



        # Documentar transaccion

        if not os.path.exists('transacciones.csv'):
            with open('transacciones.csv', 'w') as csvfile:
                writer = csv.DictWriter(
                    csvfile, fieldnames=['sku', 'sector', 'material', 'movimiento', 'hora_inicio', 'hora_fin',"sim_id"])
                writer.writeheader()
        with open('transacciones.csv', 'a') as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=['sku', 'sector', 'material', 'movimiento', 'hora_inicio', 'hora_fin',"sim_id"])
            if self.type == "entrada":
                writer.writerow({'sku': self.pallet.sku, 'sector': self.pallet.sector, 'material': self.pallet.material,
                                 'movimiento': 'Entrada', 'hora_inicio': self.pallet.store_start_time, 'hora_fin': self.pallet.store_end_time,"sim_id":sim.id()})
            else:
                writer.writerow({'sku': self.pallet.sku, 'sector': self.pallet.sector, 'material': self.pallet.material,
                                 'movimiento': 'Salida', 'hora_inicio': self.pallet.retrieve_start_time, 'hora_fin': self.pallet.retrieve_end_time,"sim_id":sim.id()})




    def obtain_material(self):
        sector:Sector
        nearest_shelf = None
        nearest_sector = None
        distance = None
        for sector in self.almacen.sectores[self.pallet.sector]:

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
            for sector in self.almacen.sectores:
                shelf = sector.get_open_shelf(self.porton.posicion)
                if shelf is not None:
                    break
        return shelf,sector

    def get_nearest_sector(self,origin)->Sector|None:
        nearest_sector = None
        nearest_distance = None
        for sector in self.almacen.sectores[self.pallet.sector]:
            if nearest_sector is None:
                nearest_sector = sector
                nearest_distance = calculate_distance(origin,sector.posicion)
            else:
                if calculate_distance(origin,sector.posicion) < nearest_distance:
                    nearest_sector = sector
                    nearest_distance = calculate_distance(origin,sector.posicion)
        return nearest_sector