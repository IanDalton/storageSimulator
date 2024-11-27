import salabim as sim
class Pallet:
    def __init__(self, sku, sector,material,env):
        self.sku = sku
        self.sector = sector
        self.material = material
        self.env = env
        self.store_start_time = self.env.now()
        self.store_end_time = None
        self.cost_start = None
        self.retrieve_start_time = self.env.now()
        self.retrieve_end_time = None
        self.cost_end = None

        return None
    def __eq__(self, other):
        if isinstance(other, str):
            return other == self.material
        elif isinstance(other, Pallet):
            return self.material == other.material
        return False