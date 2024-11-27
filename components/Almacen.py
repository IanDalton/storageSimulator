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

    def crear_portones(self, salida1=8, salida2=4, entrada=2):
        portones = {}
        portones['Ingreso'] = [Porton('Ingreso', posicion=(
            4+17*(salida1+i), 0), capacity=1) for i in range(entrada)]
        portones['Salida'] = [
            Porton('Salida', posicion=(i*17+4, 0), capacity=1) for i in range(salida1)]
        portones['Salida'].extend([Porton('Salida', posicion=(
            4+17*(i+entrada), 0), capacity=1) for i in range(salida1, salida2)])

        for i, porton in enumerate(portones['Ingreso']):
            porton.assign_id(i)
        last_id = portones['Ingreso'][-1].id
        for i, porton in enumerate(portones['Salida']):
            i += last_id + 1
            porton.assign_id(i)
        return portones

    def crear_sectores(self):
        sectores = {}
        sectores['Frío'] = Sector(
            'Frío', SelectivoSimple(), largo=80, ancho=20, posicion=(220, 0))
        sectores['Aerosoles'] = [Sector(
            'Aerosoles', DriveIn(4), largo=70, ancho=25, posicion=(0, 130)),
            Sector('Aerosoles', DriveIn(4), largo=70, ancho=25, posicion=(0, 0))] # TODO: Crear variable decision
        sectores["Food"] = [Sector('Almacén Foods', PushBack(4), largo=90, ancho=20, posicion=(200, 30)),# TODO: Crear variable decision
                         Sector('Almacén Foods', PushBack(4), largo=130, ancho=50, posicion=(150, 30))]
        sectores["HPC"] = [Sector(
            "HPC", SelectivoDoble(), largo=130, ancho=30, posicion=(120, 30)),
            Sector(
            "HPC", SelectivoDoble(), largo=80, ancho=40, posicion=(80, 70)),
            Sector(
            "HPC", SelectivoDoble(), largo=130, ancho=45, posicion=(25, 30))]
        return sectores

    def crear_equipos(self, autoelevadores=3, reach_baja=2, reach_alta=2, transpaletas=2, zorras=2):
        equipos = {}
        equipos['Autoelevador'] = [Equipo(
            'Autoelevador', altura_maxima=6, costo_mensual=1250)for _ in range(autoelevadores)]
        equipos['Reach Baja'] = [Equipo(
            'Reach Baja', altura_maxima=8, costo_mensual=1260) for _ in range(reach_baja)]
        equipos['Reach Alta'] = [Equipo(
            'Reach Alta', altura_maxima=10, costo_mensual=1800)for _ in range(reach_alta)]
        equipos['Zorra'] = [
            Equipo('Zorra', altura_maxima=0, costo_mensual=1000) for _ in range(zorras)]
        return equipos
