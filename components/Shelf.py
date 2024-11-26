from .Pallet import Pallet

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
