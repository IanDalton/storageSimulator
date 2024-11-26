import salabim as sim


class Autoelevador(sim.Component):
    def process(self):
        while True:
            # Espera por una tarea
            yield self.passivate()