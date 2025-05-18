class SmartOrderRouter:
    def __init__(self, exchanges): self.exchanges = exchanges
    def route_order(self, qty, side):
        ex = min(self.exchanges, key=lambda e: e.price) if side.lower() == 'buy' else max(self.exchanges, key=lambda e: e.price)
        return ex.name, ex.price, qty