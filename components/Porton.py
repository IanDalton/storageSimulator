import salabim as sim

class Porton(sim.Resource):
    def __init__(self, tipo, posicion, capacity=1):
        super().__init__(capacity=capacity)
        self.tipo = tipo
        self.posicion: tuple[int, int] = posicion
        self.id = None
        self.in_use = False

    def assign_id(self, id):
        self.id = id

    def process(self):
        while True:
            # Espera por una tarea
            yield self.passivate()


