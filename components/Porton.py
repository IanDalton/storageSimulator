import salabim as sim
class Porton(sim.Component):
    def __init__(self, tipo, posicion):
        super().__init__()
        self.tipo = tipo
        self.posicion:tuple[int,int] = posicion
        self.id = None
    def assign_id(self, id):
        self.id = id
    def process(self):
        while True:
            # Espera por una tarea
            yield self.passivate()
    

        