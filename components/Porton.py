import salabim as sim

class Porton(sim.Resource):
    def __init__(self, tipo, posicion, capacity=1):
        super().__init__(capacity=capacity)
        self.tipo = tipo
        self.posicion: tuple[int, int] = posicion
        self.id = None
        self.priority = 1  # Add priority attribute
        self.in_use = False
    
    def isavailable(self):
        return self.in_use

    def assign_id(self, id):
        self.id = id

    def process(self):
        while True:
            # Espera por una tarea
            yield self.passivate()


