import salabim as sim
class Pallet:
    def __init__(self, sku, sector,material):
        self.sku = sku
        self.sector = sector
        self.material = material
        self.store_start_time = sim.now()
        self.store_end_time = None
        self.retrieve_start_time = sim.now()
        self.retrieve_end_time = None
    def __eq__(self, other):
        if isinstance(other, str):
            return other == self.material
        elif isinstance(other, Pallet):
            return self.material == other.material
        return False