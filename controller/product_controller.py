from model.inventory import Inventory
from model.product import Product

class ProductController:
    def __init__(self, inventory: Inventory):
        self.inventory = inventory

    def add_product(self, name, price, stock):
        product = Product(nombre=name, precio=price, stock=stock)
        self.inventory.agregar_producto(product)

    def update_product(self, product_id, name, price, stock):
        product = Product(id=product_id, nombre=name, precio=price, stock=stock)
        self.inventory.actualizar_producto(product)

    def delete_product(self, product_id):
        self.inventory.eliminar_producto(product_id)
