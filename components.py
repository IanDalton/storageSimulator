import salabim as sim
import csv

# Definición de clases
class Pallet:
    def __init__(self, sku, sector,material):
        self.sku = sku
        self.sector = sector
        self.material = material
    def __eq__(self, other):
        if isinstance(other, str):
            return other == self.material
        elif isinstance(other, Pallet):
            return self.material == other.material 
        return False
    


class ShelfType:
    def __init__(self, nombre,ancho_estante,pasillo,cantidad_filas,largo_estante,pallets_por_fila,costo_mantenimiento=0):
        self.nombre:str = nombre
        self.area:int = largo_estante*(pasillo+ancho_estante*pallets_por_fila)
        self.costo_mantenimiento:float = costo_mantenimiento*self.area
      
        self.ancho_estante:float = ancho_estante
        self.pasillo:float = pasillo
        self.largo_estante:float = largo_estante
        self.cantidad_filas:int = cantidad_filas
        self.pallets_por_fila:int = pallets_por_fila



class Shelf:
    def __init__(self,corridor,position,floors,shelf_height,pallets_per_floor,shelf_type:ShelfType):
        self.corridor = corridor
        self.position = position
        self.floors = floors
        self.shelf_height = shelf_height
        self.shelf_type = shelf_type
        self.content:list[list[Pallet]] = [[None for _ in range(pallets_per_floor)] for _ in range(self.floors)] # Perdon
    def add_pallet(self,pallet,floor):
        self.content[floor] = pallet
    def append_pallet(self,pallet):
        for i,floor in enumerate(self.content):
            if floor.contains(None):
                self.content[i] = pallet
                return i
        return None

    def remove_pallet(self):
        for i, floor in enumerate(self.content):
            for j, pallet in enumerate(floor):
                if pallet is not None:
                    self.content[i][j] = None
                    return pallet
        return None  # If no pallet is found
    
    def locate(self,material):
        for i,floor in enumerate(self.content):
            if material in floor:
                return i
        return None

class SelectivoSimple(ShelfType):
    def __init__(self):
        super().__init__('Selectivo Simple',ancho_estante=1,pasillo=3.1,cantidad_filas=2,largo_estante=2.78,pallets_por_fila=2)
class DriveIn(ShelfType):
    def __init__(self,pallets_por_fila):# Es un carril con su pasillo
        super().__init__('Drive-in',ancho_estante=1.1*pallets_por_fila,pasillo=3,cantidad_filas=1,largo_estante=1.45,pallets_por_fila=pallets_por_fila)

class PushBack(ShelfType):
    def __init__(self,pallets_por_fila):
        super().__init__('Push-back',ancho_estante=1.1*pallets_por_fila,pasillo=3,cantidad_filas=1,largo_estante=1.45,pallets_por_fila=pallets_por_fila,costo_mantenimiento=1.75)

class SelectivoDoble(ShelfType):
    def __init__(self, ):
        super().__init__('Selectivo Doble',ancho_estante=1,pasillo=3.5,cantidad_filas=4,largo_estante=2.78,pallets_por_fila=2)

class Sector:
    def __init__(self, nombre, tipo_estanteria,largo,ancho,posicion,niveles=6):
        self.nombre = nombre
        self.tipo_estanteria:ShelfType = tipo_estanteria
        self.almacenamiento:list[Shelf] = self.generate_shelves(largo,ancho)
        self.costos_mantenimiento = sum([shelf.costo_mantenimiento for shelf in self.almacenamiento])
        self.posicion = posicion
        self.niveles = niveles
    
    def locate(self,material) -> tuple[Shelf,int]:
        shelf:Shelf
        for shelf in self.almacenamiento:
            floor = shelf.locate(material)
            if floor is not None:
                return shelf,floor
        return None,None

    def append_pallet(self,pallet):
        for shelf in self.almacenamiento:
            floor = shelf.append_pallet(pallet)
            if floor is not None:
                return shelf,floor

    def generate_shelves(self,largo, ancho):
        shelves = []

        num_shelves_width = int(largo//self.tipo_estanteria.largo_estante)
        num_shelves_depth = int(ancho//self.tipo_estanteria.ancho_estante)
        assembly_width = self.tipo_estanteria.largo_estante
        shelf_depth = self.tipo_estanteria.ancho_estante
        # Generate shelves
        for w in range(num_shelves_width):
            for d in range(num_shelves_depth):
                position_x = w * assembly_width
                position_y = d * shelf_depth
                shelf = Shelf(
                    corridor=w,
                    position=(position_x, position_y),
                    floors=self.niveles,
                    shelf_height=self.tipo_estanteria.altura_estante,
                    pallets_per_floor=self.tipo_estanteria.pallets_por_fila,
                    shelf_type=self.tipo_estanteria
                )
                shelves.append(shelf)
        return shelves
        
                

class Equipo:
    def __init__(self, nombre, altura_maxima, costo_mensual):
        self.nombre = nombre
        self.altura_maxima = altura_maxima
        self.costo_mensual = costo_mensual

class Autoelevador(sim.Component):
    def process(self):
        while True:
            # Espera por una tarea
            yield self.passivate()

# Definición del almacén
class Almacen:
    def __init__(self):
        self.largo = 285  # metros
        self.sectores = self.crear_sectores()
        self.equipos = self.crear_equipos()

    def crear_sectores(self):
        sectores = {}
        sectores['Frío'] = Sector('Frío', SelectivoSimple(),largo=80,ancho=20,posicion=(220,0))
        sectores['Aerosoles 1'] = Sector('Aerosoles', DriveIn(),largo=70,ancho=25,posicion=(0,130))
        sectores['Aerosoles 2'] = Sector('Aerosoles', DriveIn(),largo=70,ancho=25,posicion=(0,0))
        sectores['Almacén Foods 1'] = Sector('Almacén Foods', PushBack(),largo=90,ancho=20,posicion=(200,30))
        sectores['Almacén Foods 2'] = Sector('Almacén Foods', PushBack(),largo=130,ancho=50,posicion=(150,30))
        sectores["HPC 1"] = Sector("HPC", SelectivoDoble(),largo=130,ancho=30,posicion=(120,30))   
        sectores["HPC 2"] = Sector("HPC", SelectivoDoble(),largo=80,ancho=40,posicion=(80,70))   
        sectores["HPC 3"] = Sector("HPC", SelectivoDoble(),largo=130,ancho=45,posicion=(25,30))   
        return sectores

    def crear_equipos(self):
        equipos = {}
        equipos['Autoelevador'] = Equipo('Autoelevador', altura_maxima=5, costo_mensual=1000)
        equipos['Reach Baja'] = Equipo('Reach Baja', altura_maxima=7, costo_mensual=1200)
        equipos['Reach Alta'] = Equipo('Reach Alta', altura_maxima=10, costo_mensual=1500)
        equipos['Transpaleta'] = Equipo('Transpaleta', altura_maxima=0, costo_mensual=500)
        equipos['Zorra'] = Equipo('Zorra', altura_maxima=0, costo_mensual=300)
        return equipos

# Simulación de flujos de materiales

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

class ModeloSimulacion:
    def __init__(self):
        self.env = sim.Environment()
        global almacen
        almacen = Almacen()
        Entrada()
        # Agregar otros componentes como Salida, Operaciones de Picking, etc.

    def run(self):
        self.env.run(till=100)  # Ejecutar la simulación por 100 horas

# Ejecutar la simulación
if __name__ == '__main__':
    modelo = ModeloSimulacion()
    modelo.run()