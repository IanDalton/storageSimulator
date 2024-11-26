from components.Shelf import Shelf, ShelfType


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