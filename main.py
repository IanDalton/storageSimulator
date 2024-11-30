import salabim as sim
from components.Almacen import Almacen
from components.ArrivalGenerator import ArrivalGenerator
from components.Equipo import Equipo
from components.Sector import Sector
from components.Shelf import DriveIn, PushBack, SelectivoDoble, SelectivoSimple
from components.Porton import Porton

class ModeloSimulacion:
    def __init__(self, **data):
        self.env = sim.Environment()
        self.almacen = Almacen(autoelevadores=data['autoelevadores'], reach_baja=data['reach_baja'],
                               reach_alta=data['reach_alta'], zorras=data['zorras'], sectores=data['sectores'], run_id=data['run_id'])

        ArrivalGenerator(csv_file=data["csv_file"], almacen=self.almacen)
        # Agregar otros componentes como Salida, Operaciones de Picking, etc.

    def run(self):
        self.env.run()

    def serialize_environment(self):
        return self.env.serialize()

def run_simulation(**params):
    
    modelo = ModeloSimulacion(**params)
    modelo.run()
    serialized_env = modelo.serialize_environment()
    print(serialized_env)  # Or handle the serialized environment as needed

# Ejecutar la simulación
if __name__ == '__main__':
    sim.yieldless(False)
    sectores_variation_1 = {
        # Changed to SelectivoDoble
        'FRIO': Sector('Frío', SelectivoDoble(), largo=80, ancho=20, posicion=(220, 0)),
        'AEROSOL': [
            Sector('Aerosoles', PushBack(4), largo=70, ancho=25,
                   posicion=(0, 130)),  # Changed to PushBack
            Sector('Aerosoles', PushBack(4), largo=70, ancho=25,
                   posicion=(0, 0))  # Changed to PushBack
        ],
        'FOODS': [
            Sector('Almacén Foods', DriveIn(4), largo=90, ancho=20,
                   posicion=(200, 30)),  # Changed to DriveIn
            Sector('Almacén Foods', DriveIn(4), largo=130, ancho=50,
                   posicion=(150, 30))  # Changed to DriveIn
        ],
        'HPC': [
            Sector('HPC', SelectivoSimple(), largo=130, ancho=30,
                   posicion=(120, 30)),  # Changed to SelectivoSimple
            Sector('HPC', SelectivoSimple(), largo=80, ancho=40,
                   posicion=(80, 70)),  # Changed to SelectivoSimple
            Sector('HPC', SelectivoSimple(), largo=130, ancho=45,
                   posicion=(25, 30))  # Changed to SelectivoSimple
        ]
    }
    sectores_variation_2 = {
        # Changed to DriveIn
        'FRIO': Sector('Frío', DriveIn(4), largo=80, ancho=20, posicion=(220, 0)),
        'AEROSOL': [
            Sector('Aerosoles', SelectivoSimple(), largo=70, ancho=25,
                   posicion=(0, 130)),  # Changed to SelectivoSimple
            Sector('Aerosoles', SelectivoDoble(), largo=70, ancho=25,
                   posicion=(0, 0))  # Changed to SelectivoDoble
        ],
        'FOODS': [
            Sector('Almacén Foods', PushBack(4), largo=90, ancho=20,
                   posicion=(200, 30)),  # Changed to PushBack
            Sector('Almacén Foods', SelectivoSimple(), largo=130, ancho=50,
                   posicion=(150, 30))  # Changed to SelectivoSimple
        ],
        'HPC': [
            Sector('HPC', DriveIn(4), largo=130, ancho=30,
                   posicion=(120, 30)),  # Changed to DriveIn
            Sector('HPC', PushBack(4), largo=80, ancho=40,
                   posicion=(80, 70)),  # Changed to PushBack
            Sector('HPC', SelectivoDoble(), largo=130, ancho=45,
                   posicion=(25, 30))  # Kept as SelectivoDoble
        ]
    }
    sectores_variation_3 = {
        # Changed to PushBack
        'FRIO': Sector('Frío', PushBack(4), largo=80, ancho=20, posicion=(220, 0)),
        'AEROSOL': [
            Sector('Aerosoles', PushBack(4), largo=70, ancho=25,
                   posicion=(0, 130)),  # Changed to PushBack
            Sector('Aerosoles', PushBack(4), largo=70, ancho=25,
                   posicion=(0, 0))  # Changed to PushBack
        ],
        'FOODS': [
            Sector('Almacén Foods', PushBack(4), largo=90, ancho=20,
                   posicion=(200, 30)),  # Changed to PushBack
            Sector('Almacén Foods', PushBack(4), largo=130, ancho=50,
                   posicion=(150, 30))  # Changed to PushBack
        ],
        'HPC': [
            Sector('HPC', PushBack(4), largo=130, ancho=30,
                   posicion=(120, 30)),  # Changed to PushBack
            Sector('HPC', PushBack(4), largo=80, ancho=40,
                   posicion=(80, 70)),  # Changed to PushBack
            Sector('HPC', PushBack(4), largo=130, ancho=45,
                   posicion=(25, 30))  # Changed to PushBack
        ]
    }
    sectores_variation_4 = {
        # Kept as SelectivoSimple
        'FRIO': Sector('Frío', DriveIn(4), largo=80, ancho=20, posicion=(220, 0)),
        'AEROSOL': [
            Sector('Aerosoles', SelectivoSimple(), largo=70, ancho=25,
                   posicion=(0, 130)),  # Changed to SelectivoDoble
            Sector('Aerosoles', SelectivoDoble(), largo=70, ancho=25,
                   posicion=(0, 0))  # Changed to DriveIn
        ],
        'FOODS': [
            Sector('Almacén Foods', SelectivoSimple(), largo=90, ancho=20,
                   posicion=(200, 30)),  # Changed to SelectivoSimple
            Sector('Almacén Foods', SelectivoSimple(), largo=130, ancho=50,
                   posicion=(150, 30))  # Changed to SelectivoDoble
        ],
        'HPC': [
            Sector('HPC', DriveIn(4), largo=130, ancho=30,
                   posicion=(120, 30)),  # Changed to PushBack
            Sector('HPC', DriveIn(4), largo=80, ancho=40,
                   posicion=(80, 70)),  # Changed to DriveIn
            Sector('HPC', DriveIn(4), largo=130, ancho=45,
                   posicion=(25, 30))  # Changed to SelectivoSimple
        ]
    }
    parameters: list[dict] = [
        {'csv_file': 'movements.csv', 'autoelevadores': 3, 'reach_baja': 2, 'reach_alta': 2, 'zorras': 2,
            'sectores': sectores_variation_1, 'run_id': 1},
        {'csv_file': 'movements.csv', 'autoelevadores': 3, 'reach_baja': 2, 'reach_alta': 2, 'zorras': 2,
            'sectores': sectores_variation_2, 'run_id': 2},
        {'csv_file': 'movements.csv', 'autoelevadores': 3, 'reach_baja': 2, 'reach_alta': 2, 'zorras': 2,
            'sectores': sectores_variation_3, 'run_id': 3},
        {'csv_file': 'movements.csv', 'autoelevadores': 3, 'reach_baja': 2, 'reach_alta': 2, 'zorras': 2,
            'sectores': sectores_variation_4, 'run_id': 4}
    ]
    for params in parameters:
        run_simulation(**params)