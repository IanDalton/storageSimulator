from components.Almacen import Almacen
from components.TransportProcess import TransportProcess
from components.Equipo import Equipo
from components.Pallet import Pallet
from components.Porton import Porton


import salabim as sim


class ArrivalProcess(sim.Component):
    def __init__(self, arrivals, almacen):
        super().__init__()
        self.arrivals = arrivals
        self.almacen:Almacen = almacen

    def process(self):
        movimiento = self.arrivals[0]['movimiento']
        
        if movimiento.lower() == 'recepción':
            portones = self.almacen.portones['Ingreso']
        elif movimiento.lower() == 'salidas':
            portones = self.almacen.portones['Salida']

        # Wait until a Porton becomes available
        while True:
            for porton in portones:
                if not porton.in_use:
                    self.porton = porton
                    break
            if self.porton:
                break
            yield self.hold(60/3600)  # Wait for 1 time unit before checking again

        self.porton.in_use = True   

        tasks = []

        for arrival in self.arrivals:
            material = arrival['material']
            movimiento = arrival['movimiento']  # 'Recepción' or 'Salidas'
            almacenamiento = None
            pallet = Pallet(sku=material, sector=almacenamiento,material=material,env=self.env)

            if movimiento.lower() == 'recepción':
                # Simulate the entry process
                # Select the appropriate equipment

                yield from self.interaccion_camion()
                TransportProcess(pallet, self.porton, "entrada", almacen=self.almacen).activate()

            elif movimiento.lower() == 'salidas':
                # Simulate the exit process
                task = TransportProcess(pallet, self.porton, "salida", callback=self.interaccion_camion, almacen=self.almacen)
                task.activate()
                yield self.wait(task)



        self.porton.in_use = False

    def interaccion_camion(self):
        zorra = self.almacen.equipos["Zorra"]

        yield self.request(zorra)
        zorra: Equipo
        yield self.hold(zorra.get_time_to_location(self.porton.posicion)/3600)

        # Simulate picking up the pallet (16 seconds)
        yield self.hold(16 / 3600)
        # Simulate scanning the pallet (15 seconds)
        yield self.hold(15 / 3600)
        self.release(zorra)

    def obtener_destino(self, pallet):
        # Get the storage location coordinates
        sector = self.almacen.sectores[pallet.sector]
        return sector.posicion

    def calcular_distancia(self, origen, destino):
        dx = abs(destino[0] - origen[0])
        dy = abs(destino[1] - origen[1])
        return dx + dy  # Manhattan distance