from components.Equipo import Equipo
from components.Sector import Sector
from components.Shelf import DriveIn, PushBack, SelectivoDoble, SelectivoSimple
from components.Porton import Porton


class Almacen:
    def __init__(self):
        self.largo = 285  # metros
        self.sectores = self.crear_sectores()
        self.equipos = self.crear_equipos()
        self.portones = self.crear_portones()

    def crear_portones(self,salida1,salida2,entrada):
        portones = {}
        portones['Ingreso'] = [Porton('Ingreso', posicion=(4+17*(salida1+i), 0)) for i in range(entrada)]
        portones['Salida'] = [Porton('Salida', posicion=(i*17+4, 0)) for i in range(salida1)]
        portones['Salida'].extend([Porton('Salida', posicion=(4+17*(i+entrada), 0)) for i in range(salida1,salida2)])
        return portones
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