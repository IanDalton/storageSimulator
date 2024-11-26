# Definición de clases
class Pallet:
    def __init__(self, sku, sector,material):
        self.sku = sku
        self.sector = sector
        self.material = material
    def __eq__(self, other):
        if isinstance(other, str):
            return other == self.material
        elif isinstance(other, Pallet):
            return self.material == other.material
        return False