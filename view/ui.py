import flet as ft
from flet import Icons
from controller.product_controller import ProductController
from model.inventory import Inventory
from model.product import Product

def launch_ui():
    def main(page: ft.Page):
        page.title = "Gestor de Mercancías - Supermercado"
        page.theme_mode = "light"
        page.window_width = 900
        page.window_height = 650
        page.scroll = "AUTO"
        page.horizontal_alignment = "center"
        page.vertical_alignment = "start"
        page.padding = 20

        # SnackBar para errores
        page.snack_bar = ft.SnackBar(content=ft.Text(""), bgcolor=ft.Colors.RED)
        page.overlay.append(page.snack_bar)

        inventory = Inventory()
        inventory.cargar_productos()
        controller = ProductController(inventory)
        selected_product: Product = None

        # Campos de entrada
        nombre_input = ft.TextField(label="Nombre del producto", expand=True, border_radius=10, filled=True)
        precio_input = ft.TextField(label="Precio", width=150, keyboard_type=ft.KeyboardType.NUMBER, border_radius=10, filled=True)
        stock_input = ft.TextField(label="Stock", width=150, keyboard_type=ft.KeyboardType.NUMBER, border_radius=10, filled=True)
        btn_guardar = ft.ElevatedButton("Agregar", icon=Icons.ADD, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))

        # Buscador
        busqueda_input = ft.TextField(
            label="🔍 Buscar producto",
            expand=True,
            on_change=lambda e: actualizar_listado(),
            border_radius=10,
            filled=True
        )

        productos_listview = ft.Column(expand=True, spacing=10)

        def mostrar_error(msg: str):
            page.snack_bar.content.value = msg
            page.snack_bar.open = True
            page.update()

        def cargar_a_formulario(product: Product):
            nonlocal selected_product
            selected_product = product
            nombre_input.value = product.nombre
            precio_input.value = str(product.precio)
            stock_input.value = str(product.stock)
            btn_guardar.text = "Actualizar"
            btn_guardar.icon = Icons.UPDATE
            page.update()

        def limpiar_formulario():
            nonlocal selected_product
            selected_product = None
            nombre_input.value = ""
            precio_input.value = ""
            stock_input.value = ""
            btn_guardar.text = "Agregar"
            btn_guardar.icon = Icons.ADD
            page.update()

        def formatear_guaranies(valor):
            return f"{int(valor):,}".replace(",", ".") + " Gs"

        def actualizar_listado():
            productos_listview.controls.clear()
            inventory.cargar_productos()
            filtro = busqueda_input.value.lower().strip()

            filtrados = [p for p in inventory.productos if filtro in p.nombre.lower()]
            if not filtrados:
                productos_listview.controls.append(
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(name=Icons.INBOX, color=ft.Colors.BLUE_GREY, size=24),
                                ft.Text(
                                    "No hay productos que coincidan con tu búsqueda.",
                                    size=16,
                                    italic=True,
                                    color=ft.Colors.BLUE_GREY_900 if page.theme_mode == "light" else ft.Colors.WHITE70
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        padding=20,
                        border_radius=10,
                        bgcolor=ft.Colors.BLUE_GREY_100 if page.theme_mode == "light" else ft.Colors.BLUE_GREY_900
                    )
                )

            for p in filtrados:
                productos_listview.controls.append(
                    ft.Card(
                        elevation=4,
                        shape=ft.RoundedRectangleBorder(radius=12),
                        content=ft.Container(
                            padding=10,
                            content=ft.ListTile(
                                title=ft.Text(p.nombre, weight="bold"),
                                subtitle=ft.Text(
                                    f"Precio: {formatear_guaranies(p.precio)} Gs | Stock: {p.stock}",
                                    color=color_por_stock(p.stock)
                                ),
                                leading=ft.Icon(Icons.EDIT_NOTE),
                                on_click=lambda e, prod=p: cargar_a_formulario(prod),
                                trailing=ft.IconButton(
                                    icon=Icons.DELETE,
                                    icon_color=ft.Colors.RED,
                                    on_click=lambda e, pid=p.id: eliminar_producto(pid)
                                )
                            )
                        )
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

        def color_por_stock(stock):
            if stock == 0:
                return ft.Colors.RED_900
            elif stock < 5:
                return ft.Colors.RED
            elif stock <= 10:
                return ft.Colors.AMBER
            else:
                return ft.Colors.GREEN

        def eliminar_producto(product_id):
            controller.delete_product(product_id)
            limpiar_formulario()
            actualizar_listado()

        actualizar_listado()

        tema_toggle = ft.Switch(label="🌙 Modo oscuro", value=False)

        def cambiar_tema(e):
            page.theme_mode = "dark" if tema_toggle.value else "light"
            page.update()

        tema_toggle.on_change = cambiar_tema

        # Layout final  
        page.add(
            ft.Row([
                ft.Column([
                    ft.Text("📦 Gestor de Mercancías", size=32, weight="bold"),
                    ft.Text("Sistema de gestión de stock para supermercados", size=16, color=ft.Colors.BLUE_GREY),
                ], expand=True),
                tema_toggle
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(),
            ft.Container(
                content=ft.Row(
                    [nombre_input, precio_input, stock_input, btn_guardar],
                    spacing=10
                ),
                padding=10
            ),
            ft.Row(
                [ft.TextButton("🧹 Limpiar", on_click=lambda e: limpiar_formulario())],
                alignment=ft.MainAxisAlignment.END
            ),
            ft.Divider(),
            busqueda_input,
            ft.Text("📋 Inventario", size=22, weight="w600"),
            productos_listview
        )


        btn_guardar.on_click = guardar_producto

    ft.app(target=main)
