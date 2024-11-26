import salabim as sim
from components.Almacen import Almacen
from components.ArrivalGenerator import ArrivalGenerator

class ModeloSimulacion:
    def __init__(self):
        self.env = sim.Environment()
        global almacen
        almacen = Almacen()
        
        ArrivalGenerator(csv_file='movimientos.csv')
        # Agregar otros componentes como Salida, Operaciones de Picking, etc.

    def run(self):
        self.env.run()  # Ejecutar la simulación por 100 horas

# Ejecutar la simulación
if __name__ == '__main__':
    modelo = ModeloSimulacion()
    modelo.run()