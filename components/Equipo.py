import salabim as sim
from components.utils import calculate_distance

class Equipo(sim.Resource):
    def __init__(self, nombre, altura_maxima, costo_mensual,velocidad=1.82, capacity=1):
        super().__init__(capacity=capacity)
        self.nombre = nombre
        self.altura_maxima = altura_maxima
        self.costo_mensual = costo_mensual
        self.posicion = (120,20)
        self.velocidad = velocidad
        self.in_use = False
    
    def get_time_to_location(self,location)->float:
        return calculate_distance(self.posicion,location)/self.velocidad