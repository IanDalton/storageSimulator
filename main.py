import salabim as sim
from components.Almacen import Almacen
from components.Entrada import Entrada

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