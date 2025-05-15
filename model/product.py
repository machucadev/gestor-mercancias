class Product:
    def __init__(self, id: int = None, nombre: str = "", precio: float = 0.0, stock: int = 0):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    def __repr__(self):
        return f"{self.nombre} - {self.precio} Gs - Stock: {self.stock}"
