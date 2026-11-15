class DomainError(Exception):
    pass

class InvalidQuantity(DomainError):
    pass

class UnknownSku(DomainError):
    def __init__(self, sku: str) -> None:
        super().__init__(f"Unknown sku: {sku}")
        self.sku = sku

class OutofStock(DomainError):
    def __init__(self, sku: str, requested: int, available: int) -> None:
        super().__init__(
            f"Out of stock: {sku}, requested {requested}, available {available}"
        )

        self.sku = sku
        self.requested = requested
        self.available = available