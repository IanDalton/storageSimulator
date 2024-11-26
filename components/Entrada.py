# Definición del almacén
from components.Pallet import Pallet
from components.Sector import Sector
from main import almacen


import salabim as sim


import csv


class Entrada(sim.Component):
    def process(self):
        with open('movimientos.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                material = row['Material']
                movimiento = row['Movimiento']  # 'Entrada' or 'Salida'
                hora = row['Hora']
                fecha = row['Fecha']
                almacenamiento = row['Almacenamiento']  # Sector name

                pallet = Pallet(sku=material, sector=almacenamiento, material=material)
                equipo = self.seleccionar_equipo(pallet)

                yield self.request(equipo)
                # Tomar pallet desde el piso y arrancar (16 segundos)
                yield self.hold(16 / 3600)
                # Escanear pallet desde el autoelevador (15 segundos)
                yield self.hold(15 / 3600)

                # Calcular tiempo de viaje
                origen = (0, 0)  # Punto de inicio
                destino = self.obtener_destino(pallet)
                distancia = self.calcular_distancia(origen, destino)
                tiempo_viaje = distancia / 1.82 / 3600
                yield self.hold(tiempo_viaje)

                if movimiento == 'Entrada':
                    # Colocar pallet en el almacenamiento
                    yield self.hold(16 / 3600)  # Dejar pallet y arrancar
                    sector:Sector = almacen.sectores[almacenamiento]
                    shelf,floor = sector.append_pallet(pallet)
                    distancia = self.calcular_distancia(destino, shelf.position)
                    tiempo_viaje = distancia / 1.82 / 3600
                    yield self.hold(tiempo_viaje)
                    tiempo_subir= floor/1.82/3600
                    yield self.hold(tiempo_subir)
                    yield self.hold(16 / 3600)  # Dejar pallet y arrancar

                elif movimiento == 'Salida':
                    # Retirar pallet del almacenamiento
                    yield self.hold(16 / 3600)  # Tomar pallet y arrancar
                    sector = almacen.sectores[almacenamiento]
                    sector.almacenamiento[0].remove_pallet(floor=0)  # Simplificado

                self.release(equipo)
                # Esperar hasta la siguiente acción programada
                yield self.hold(self.tiempo_hasta_siguiente(hora))

    def seleccionar_equipo(self, pallet):
        # Seleccionar el equipo adecuado
        return almacen.equipos['Autoelevador']

    def obtener_destino(self, pallet):
        # Obtener la posición del sector de almacenamiento
        sector = almacen.sectores[pallet.sector]
        return sector.posicion

    def calcular_distancia(self, origen, destino):
        # Calcula la distancia de manhattan entre dos puntos
        dx = abs(destino[0] - origen[0])
        dy = abs(destino[1] - origen[1])
        return dx + dy

    def tiempo_hasta_siguiente(self, hora_actual):
        # Calcular el tiempo hasta la siguiente acción (simplificado)
        return sim.Exponential(1).sample()