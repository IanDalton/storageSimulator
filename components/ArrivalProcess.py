from components.Almacen import Almacen
from components.TransportProcess import TransportProcess
from components.Equipo import Equipo
from components.Pallet import Pallet
from components.Porton import Porton
import pandas as pd

import salabim as sim


class ArrivalProcess(sim.Component):
    def __init__(self, arrivals, almacen):
        super().__init__()
        self.arrivals = arrivals
        self.almacen:Almacen = almacen
        self.transport_ready = sim.State()

    def process(self):
        movimiento = self.arrivals[0]['movimiento']
        
        if movimiento.lower() == 'recepción':
            portones = self.almacen.portones['Ingreso']
        elif movimiento.lower() == 'salidas':
            portones = self.almacen.portones['Salida']
        else:
            raise ValueError(f"Movimiento no válido: {movimiento}")

        # Wait until a Porton becomes available
        while True:
            for porton in portones:
                if not porton.in_use:
                    porton = porton
                    porton:Porton
                    break
            if porton:
                break
            yield self.hold(60/3600)  # Wait for 1 time unit before checking again

        porton.in_use = True   

        tasks = []

        for arrival in self.arrivals:
            material = arrival['material']
            movimiento = arrival['movimiento']  # 'Recepción' or 'Salidas'
            almacenamiento = arrival['almacenamiento']
            pallet = Pallet(sku=material, sector=almacenamiento,material=material,env=self.env)

            if movimiento.lower() == 'recepción':
                # Simulate the entry process
                yield from self.interaccion_camion(porton)
                task = TransportProcess(pallet, porton, "entrada", almacen=self.almacen, parent=self)
                task.activate()
                yield self.wait(self.transport_ready) ### TOMI
                
            elif movimiento.lower() == 'salidas':
                # Simulate the exit process
                task = TransportProcess(pallet, porton, "salida", almacen=self.almacen, parent=self)
                task.activate()
                yield self.wait(self.transport_ready) ### TOMI
                
    
        porton.in_use = False

    def interaccion_camion(self, porton):
        zorras = self.almacen.equipos["Zorra"]
        zorra = None
        while True:
            for zorra in zorras:
                if not zorra.in_use:
                    zorra = zorra
                    zorra: Equipo
                    break
            if zorra:
                break
            yield self.hold(60/3600)  # Wait for 1 time unit before checking again

        zorra.in_use = True
        
        yield self.hold(zorra.get_time_to_location(porton.posicion)/3600)

        # Simulate picking up the pallet (16 seconds)
        yield self.hold(16 / 3600)
        # Simulate scanning the pallet (15 seconds)
        yield self.hold(15 / 3600)
        
        zorra.in_use = False

    def obtener_destino(self, pallet):
        # Get the storage location coordinates
        sector = self.almacen.sectores[pallet.sector]
        return sector.posicion

    def calcular_distancia(self, origen, destino):
        dx = abs(destino[0] - origen[0])
        dy = abs(destino[1] - origen[1])
        return dx + dy  # Manhattan distance