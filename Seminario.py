import supermercado
from datetime import datetime
import sqlite3

# Lista de productos iniciales
productos_iniciales = [
    ("Manzana", 0.5, 64),
    ("Leche", 1.2, 20),
    ("Pan", 1.0, 50),
    ("Arroz", 0.8, 30),
    ("Fideos", 0.7, 40),
    ("Aceite", 2.5, 25),
    ("Azúcar", 1.3, 35),
    ("Sal", 0.4, 60),
    ("Huevos", 2.0, 12),
    ("Jugo", 1.5, 10),
    ("Cereal", 3.0, 15),
    ("Queso", 4.0, 22)
]

def mostrar_menu():
    print("\n---- MENU ----")
    print("1. Registrar nuevo cliente")
    print("2. Mostrar productos")
    print("3. Mostrar clientes")
    print("4. Realizar compra")
    print("5. Reponer stock")
    print("6. Salir")

def registrar_cliente():
    nombre = input("Nombre: ")
    direccion = input("Dirección: ")
    correo = input("Correo: ")
    supermercado.insertar_cliente(nombre, direccion, correo)
    print("Cliente registrado con éxito.")

def mostrar_productos():
    productos = supermercado.obtener_productos()
    print("\nProductos disponibles:")
    for producto in productos:
        print(f"{producto[0]}. {producto[1]} - ${producto[2]} - Stock: {producto[3]}")

def realizar_compra():
    id_cliente = int(input("Ingrese su ID de cliente: "))
    detalles_pedido = []
    while True:
        mostrar_productos()
        id_producto = int(input("ID del producto a comprar (0 para terminar): "))
        if id_producto == 0:
            break
        cantidad = int(input("Cantidad: "))
        
        # Obtener el precio del producto
        productos = supermercado.obtener_productos()
        precio = None
        stock_disponible = None
        for producto in productos:
            if producto[0] == id_producto:
                precio = producto[2]
                stock_disponible = producto[3]
                break
        
        if precio is None:
            print("Producto no encontrado.")
            continue
        
        if cantidad > stock_disponible:
            print(f"No hay suficiente stock para el producto {producto[1]}. Stock disponible: {stock_disponible}, solicitado: {cantidad}")
            continue

        detalles_pedido.append((id_producto, cantidad, precio))

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        supermercado.insertar_pedido(id_cliente, fecha, detalles_pedido)
        total = sum(cantidad * precio for id_producto, cantidad, precio in detalles_pedido)
        print("\n--- FACTURA ---")
        for detalle in detalles_pedido:
            id_producto, cantidad, precio = detalle
            print(f"Producto ID {id_producto}, Cantidad {cantidad}, Precio Unitario ${precio}, Subtotal ${cantidad * precio}")
        print(f"Total a pagar: ${total}")

        while True:
            pago = float(input("Ingrese el monto con el que va a pagar: "))
            if pago == total:
                print("Pago realizado con éxito.")
                break
            elif pago > total:
                vuelto = pago - total
                print(f"Pago realizado con éxito. Su vuelto es: ${vuelto:.2f}")
                break
            else:
                print("Pago insuficiente. Por favor, ingrese un monto adicional.")

        print("\n--- TICKET DE COMPRA ---")
        print(f"Cliente ID: {id_cliente}")
        for detalle in detalles_pedido:
            id_producto, cantidad, precio = detalle
            print(f"Producto ID {id_producto}, Cantidad {cantidad}, Precio Unitario ${precio}, Subtotal ${cantidad * precio}")
        print(f"Total pagado: ${total}\n")

    except Exception as e:
        print(e)

def reponer_stock():
    id_dueno = int(input("Ingrese su ID de dueño: "))
    detalles_reposicion = []
    while True:
        mostrar_productos()
        id_producto = int(input("ID del producto a reponer (0 para terminar): "))
        if id_producto == 0:
            break
        cantidad_a_reponer = int(input("Cantidad a reponer: "))
        
        # Obtener el precio del producto
        productos = supermercado.obtener_productos()
        precio_unitario = None
        for producto in productos:
            if producto[0] == id_producto:
                precio_unitario = producto[2]
                break
        
        if precio_unitario is None:
            print("Producto no encontrado.")
            continue
        
        detalles_reposicion.append((id_producto, cantidad_a_reponer, precio_unitario))

    total_a_pagar = sum(cantidad * precio for id_producto, cantidad, precio in detalles_reposicion)
    print("\n--- FACTURA DE REPOSICIÓN ---")
    for detalle in detalles_reposicion:
        id_producto, cantidad, precio = detalle
        print(f"Producto ID {id_producto}, Cantidad {cantidad}, Precio Unitario ${precio}, Subtotal ${cantidad * precio}")
    print(f"Total a pagar: ${total_a_pagar}")

    while True:
        pago = float(input("Ingrese el monto con el que va a pagar: "))
        if pago == total_a_pagar:
            print("Pago realizado con éxito. Stock actualizado.")
            break
        elif pago > total_a_pagar:
            vuelto = pago - total_a_pagar
            print(f"Pago realizado con éxito. Su vuelto es: ${vuelto:.2f}")
            break
        else:
            print("Pago insuficiente. Por favor, ingrese un monto adicional.")

    # Actualizar el stock de los productos
    conn = sqlite3.connect('supermercado.db')
    cursor = conn.cursor()
    for detalle in detalles_reposicion:
        id_producto, cantidad, precio = detalle
        cursor.execute('''UPDATE productos SET cantidad = cantidad + ? WHERE id = ?''', (cantidad, id_producto))
    conn.commit()
    conn.close()

    print("\n--- TICKET DE REPOSICIÓN ---")
    print(f"Dueño ID: {id_dueno}")
    for detalle in detalles_reposicion:
        id_producto, cantidad, precio = detalle
        print(f"Producto ID {id_producto}, Cantidad {cantidad}, Precio Unitario ${precio}, Subtotal ${cantidad * precio}")
    print(f"Total pagado: ${total_a_pagar}\n")

def mostrar_clientes():
    clientes = supermercado.obtener_clientes()
    print("\nClientes registrados:")
    for cliente in clientes:
        print(f"ID: {cliente[0]}, Nombre: {cliente[1]}, Dirección: {cliente[2]}, Correo: {cliente[3]}")

def main():
    supermercado.crear_tablas()

    # Insertar algunos productos con stock inicial (si aún no están en la base de datos)
    productos_actuales = supermercado.obtener_productos()
    if not productos_actuales:
        for producto in productos_iniciales:
            supermercado.insertar_producto(*producto)

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            registrar_cliente()
        elif opcion == "2":
            mostrar_productos()
        elif opcion == "3":
            mostrar_clientes()
        elif opcion == "4":
            realizar_compra()
        elif opcion == "5":
            reponer_stock()
        elif opcion == "6":
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Inténtelo de nuevo.")

if __name__ == "__main__":
    main()
