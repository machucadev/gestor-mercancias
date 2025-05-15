from database.db_manager import get_connection
from model.product import Product
from utils.decorators import log_action
from utils.consola_observer import ConsolaObserver
from model.logger import Logger

class Inventory:
    def __init__(self):
        self.productos = []
        self.logger = Logger()
        self.logger.registrar_observador(ConsolaObserver()) 

    def cargar_productos(self):
        self.productos.clear()
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, precio, stock FROM productos")
            for row in cursor.fetchall():
                self.productos.append(Product(*row))

    @log_action("Agregar producto")
    def agregar_producto(self, producto: Product):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
                           (producto.nombre, producto.precio, producto.stock))
            conn.commit()
            self.logger.notificar_observadores("Producto agregado")

    @log_action("Actualizar producto")
    def actualizar_producto(self, producto: Product):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE productos
                SET nombre = ?, precio = ?, stock = ?
                WHERE id = ?
            """, (producto.nombre, producto.precio, producto.stock, producto.id))
            conn.commit()
            self.logger.notificar_observadores("Producto actualizado")

    @log_action("Eliminar producto")
    def eliminar_producto(self, producto_id: int):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
            conn.commit()
            self.logger.notificar_observadores("Producto eliminado")
