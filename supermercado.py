import sqlite3

# Función para crear la base de datos y las tablas
def crear_tablas():
    conn = sqlite3.connect('supermercado.db')
    cursor = conn.cursor()

    # Tabla de clientes
    cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL,
                        direccion TEXT,
                        correo TEXT
                    )''')

    # Tabla de productos
    cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL,
                        precio REAL NOT NULL,
                        cantidad INTEGER NOT NULL
                    )''')

    # Tabla de pedidos
    cursor.execute('''CREATE TABLE IF NOT EXISTS pedidos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_cliente INTEGER NOT NULL,
                        fecha TEXT NOT NULL,
                        total REAL,
                        FOREIGN KEY (id_cliente) REFERENCES clientes (id)
                    )''')

    # Tabla de detalles de pedidos
    cursor.execute('''CREATE TABLE IF NOT EXISTS detalle_pedidos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_pedido INTEGER NOT NULL,
                        id_producto INTEGER NOT NULL,
                        cantidad INTEGER NOT NULL,
                        precio REAL NOT NULL,
                        FOREIGN KEY (id_pedido) REFERENCES pedidos (id),
                        FOREIGN KEY (id_producto) REFERENCES productos (id)
                    )''')

    conn.commit()
    conn.close()

# Función para insertar un cliente en la base de datos
def insertar_cliente(nombre, direccion, correo):
    conn = sqlite3.connect('supermercado.db')
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO clientes (nombre, direccion, correo) VALUES (?, ?, ?)''', (nombre, direccion, correo))

    conn.commit()
    conn.close()

# Función para insertar un producto en la base de datos
def insertar_producto(nombre, precio, cantidad):
    conn = sqlite3.connect('supermercado.db')
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO productos (nombre, precio, cantidad) VALUES (?, ?, ?)''', (nombre, precio, cantidad))

    conn.commit()
    conn.close()

# Función para insertar un pedido en la base de datos
def insertar_pedido(id_cliente, fecha, detalles):
    conn = sqlite3.connect('supermercado.db')
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO pedidos (id_cliente, fecha, total) VALUES (?, ?, ?)''', (id_cliente, fecha, None))
    id_pedido = cursor.lastrowid

    total = 0
    for detalle in detalles:
        id_producto, cantidad, precio = detalle
        
        # Verificar el stock disponible
        cursor.execute('''SELECT cantidad FROM productos WHERE id = ?''', (id_producto,))
        stock_disponible = cursor.fetchone()[0]
        if stock_disponible < cantidad:
            conn.close()
            raise Exception(f"No hay suficiente stock para el producto con id {id_producto}. Stock disponible: {stock_disponible}, solicitado: {cantidad}")
        
        # Actualizar el stock del producto
        cursor.execute('''UPDATE productos SET cantidad = cantidad - ? WHERE id = ?''', (cantidad, id_producto))
        
        cursor.execute('''INSERT INTO detalle_pedidos (id_pedido, id_producto, cantidad, precio) VALUES (?, ?, ?, ?)''', (id_pedido, id_producto, cantidad, precio))
        total += cantidad * precio

    cursor.execute('''UPDATE pedidos SET total = ? WHERE id = ?''', (total, id_pedido))

    conn.commit()
    conn.close()

# Función para obtener todos los clientes
def obtener_clientes():
    conn = sqlite3.connect('supermercado.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM clientes''')
    clientes = cursor.fetchall()

    conn.close()
    return clientes

# Función para obtener todos los productos
def obtener_productos():
    conn = sqlite3.connect('supermercado.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM productos''')
    productos = cursor.fetchall()

    conn.close()
    return productos

# Función para obtener todos los pedidos
def obtener_pedidos():
    conn = sqlite3.connect('supermercado.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM pedidos''')
    pedidos = cursor.fetchall()

    conn.close()
    return pedidos

# Crear las tablas si no existen
crear_tablas()
