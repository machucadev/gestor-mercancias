
---

### ✅ `README.md`

```markdown
# 🛒 Gestor de Mercancías - Supermercado

Sistema de gestión de productos para un supermercado, desarrollado en **Python** con interfaz gráfica en **Flet**.  
Permite registrar, actualizar y eliminar productos con control de stock y precios.

---

## ✅ Funcionalidades principales

- Alta, baja y modificación de productos
- Validación de datos desde la interfaz
- Registro de logs de actividad:
  - En consola
  - En base de datos SQLite
  - En servidor remoto (cliente-servidor)
- Interfaz moderna construida con **Flet**
- Arquitectura organizada: **POO + MVC + Patrón Observador + Decorador**

---

## 🧠 Requisitos cumplidos

| Criterio                                | Estado     |
|----------------------------------------|------------|
| Programación Orientada a Objetos (POO) | ✅          |
| Arquitectura MVC                       | ✅          |
| Decorador para registrar logs          | ✅          |
| Patrón Observador                      | ✅          |
| Cliente-servidor de logs               | ✅          |
| Control de errores en la interfaz      | ✅          |



---

## 📦 Estructura del proyecto

```

supermarket_manager/
├── main.py
├── ver_logs.py
├── README.md
├── controller/
│   └── product_controller.py
├── model/
│   ├── product.py
│   ├── inventory.py
│   ├── logger.py
│   └── observer.py
├── view/
│   └── ui.py
├── utils/
│   ├── decorators.py
│   ├── consola_observer.py
│   └── sesion.py
├── database/
│   └── db_manager.py
├── server/
│   ├── log_server.py
│   └── log_client.py
└── supermarket.db (se crea automáticamente)

````

---

## 🚀 Instrucciones para ejecutar

### 1. Instalar dependencias

```bash
pip install flet
````

### 2. Ejecutar el servidor de logs (en una terminal separada)

```bash
python -m server.log_server
```

### 3. Ejecutar la aplicación principal

```bash
python main.py
```

---

## 🔍 Visualización de logs

Los logs se almacenan en:

* `supermarket.db`, tabla `logs`
* Consola (vía observador)
* Servidor TCP (`log_server.py`)

También podés verlos con este comando adicional:

```bash
python ver_logs.py
```

---

## 👤 Usuario

El archivo `utils/sesion.py` define el nombre del usuario actual:

```python
usuario_actual = "admin"
```

---

## 🛠 Requisitos técnicos

* Python 3.9+
* Flet (interfaz gráfica)
* SQLite (base de datos integrada)
* TCP/IP sockets (para cliente-servidor de logs)

---

## ✨ Autor

Desarrollado por: **Santiago Machuca Páez**
Proyecto académico - Gestión de Mercancías
