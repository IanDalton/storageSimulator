import salabim as sim
from components.Almacen import Almacen
from components.ArrivalGenerator import ArrivalGenerator

class ModeloSimulacion:
    def __init__(self):
        self.env = sim.Environment()
        self.almacen = Almacen()
        
        ArrivalGenerator(csv_file='movements.csv', almacen=self.almacen)
        # Agregar otros componentes como Salida, Operaciones de Picking, etc.

    def run(self):
        self.env.run() 

# Ejecutar la simulación
if __name__ == '__main__':
    sim.yieldless(False)
    modelo = ModeloSimulacion()
    modelo.run()