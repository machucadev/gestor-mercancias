import flet as ft
from flet import Icons
from controller.product_controller import ProductController
from model.inventory import Inventory
from model.product import Product

def launch_ui():
    def main(page: ft.Page):
        page.title = "Gestor de Mercancías - Supermercado"
        page.theme_mode = "light"
        page.window_width = 800
        page.window_height = 600
        page.scroll = "AUTO"

        # Definir el SnackBar desde el inicio
        page.snack_bar = ft.SnackBar(content=ft.Text(""), bgcolor=ft.Colors.RED)
        page.overlay.append(page.snack_bar)

        inventory = Inventory()
        inventory.cargar_productos()
        controller = ProductController(inventory)

        selected_product: Product = None

        nombre_input = ft.TextField(label="Nombre del producto", expand=True)
        precio_input = ft.TextField(label="Precio", width=150, keyboard_type=ft.KeyboardType.NUMBER)
        stock_input = ft.TextField(label="Stock", width=150, keyboard_type=ft.KeyboardType.NUMBER)

        btn_guardar = ft.ElevatedButton("Agregar")

        productos_listview = ft.Column(expand=True)

        def mostrar_error(msg: str):
            page.snack_bar.content.value = msg
            page.snack_bar.bgcolor = ft.Colors.RED
            page.snack_bar.open = True
            page.update()

        def cargar_a_formulario(product: Product):
            nonlocal selected_product
            selected_product = product
            nombre_input.value = product.nombre
            precio_input.value = str(product.precio)
            stock_input.value = str(product.stock)
            btn_guardar.text = "Actualizar"
            page.update()

        def limpiar_formulario():
            nonlocal selected_product
            selected_product = None
            nombre_input.value = ""
            precio_input.value = ""
            stock_input.value = ""
            btn_guardar.text = "Agregar"
            page.update()

        def actualizar_listado():
            productos_listview.controls.clear()
            inventory.cargar_productos()
            for p in inventory.productos:
                productos_listview.controls.append(
                    ft.Card(
                        content=ft.ListTile(
                            title=ft.Text(p.nombre, weight="bold"),
                            subtitle=ft.Text(f"Precio: {p.precio} Gs | Stock: {p.stock}"),
                            leading=ft.Icon(Icons.EDIT),
                            on_click=lambda e, prod=p: cargar_a_formulario(prod),
                            trailing=ft.IconButton(icon=Icons.DELETE, on_click=lambda e, pid=p.id: eliminar_producto(pid))
                        ),
                        margin=10
                    )
                )
            page.update()

        def guardar_producto(e):
            try:
                nombre = nombre_input.value.strip()
                if not nombre:
                    mostrar_error("El nombre no puede estar vacío.")
                    return

                try:
                    precio = float(precio_input.value)
                    if precio < 0:
                        mostrar_error("El precio no puede ser negativo.")
                        return
                except ValueError:
                    mostrar_error("El precio debe ser un número válido.")
                    return

                try:
                    stock = int(stock_input.value)
                    if stock < 0:
                        mostrar_error("El stock no puede ser negativo.")
                        return
                except ValueError:
                    mostrar_error("El stock debe ser un número entero válido.")
                    return

                if selected_product:
                    controller.update_product(selected_product.id, nombre, precio, stock)
                else:
                    controller.add_product(nombre, precio, stock)

                limpiar_formulario()
                actualizar_listado()

            except Exception as ex:
                mostrar_error(str(ex))

        def eliminar_producto(product_id):
            controller.delete_product(product_id)
            limpiar_formulario()
            actualizar_listado()

        actualizar_listado()

        page.add(
            ft.Text("📦 Gestor de Mercancías", size=26, weight="bold"),
            ft.Divider(),
            ft.Row(
                [nombre_input, precio_input, stock_input, btn_guardar],
                spacing=10
            ),
            ft.Row(
                [ft.ElevatedButton("Limpiar", on_click=lambda e: limpiar_formulario())],
                alignment=ft.MainAxisAlignment.END
            ),
            ft.Divider(),
            ft.Text("🧾 Inventario", size=22, weight="w600"),
            productos_listview
        )

        btn_guardar.on_click = guardar_producto

    ft.app(target=main)
