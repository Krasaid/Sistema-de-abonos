from database.mysql_connection import conexion
from mysql.connector import Error

def check_connection():
    if conexion is None:
        raise ConnectionError("❌ No hay conexión con la base de datos.")

def obtener_orden_con_cliente(id_orden):
    check_connection()
    query = """
    SELECT c.nombre, c.telefono, o.descripcion, o.precio
    FROM Ordenes o
    JOIN Clientes c ON o.id_cliente = c.id_cliente
    WHERE o.id_orden = %s
    """
    cursor = conexion.cursor()
    cursor.execute(query, (id_orden,))
    row = cursor.fetchone()
    return {
        "nombre": row[0],
        "telefono": row[1],
        "descripcion": row[2],
        "precio": float(row[3])
    }

def get_abonos_por_orden(id_orden):
    check_connection()
    query = "SELECT fecha_abono, monto FROM Abonos WHERE id_orden = %s ORDER BY fecha_abono"
    cursor = conexion.cursor()
    cursor.execute(query, (id_orden,))
    return [{"fecha_abono": row[0], "monto": float(row[1])} for row in cursor.fetchall()]

def agregar_abono(id_orden, monto, fecha_abono):
    check_connection()
    query = "INSERT INTO Abonos (id_orden, fecha_abono, monto) VALUES (%s, %s, %s)"
    cursor = conexion.cursor()
    cursor.execute(query, (id_orden, fecha_abono, monto))
    conexion.commit()

def obtener_ordenes_con_cliente():
    check_connection()
    query = """
    SELECT o.id_orden, c.nombre, o.descripcion, o.precio, o.estado
    FROM Ordenes o
    JOIN Clientes c ON o.id_cliente = c.id_cliente
    ORDER BY o.id_orden DESC
    """
    cursor = conexion.cursor()
    cursor.execute(query)
    return [
        {
            "id_orden": row[0],
            "nombre": row[1],
            "descripcion": row[2],
            "precio": float(row[3]),
            "estado": row[4]
        }
        for row in cursor.fetchall()
    ]

def agregar_cliente_y_orden(nombre, telefono, descripcion, precio):
    check_connection()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO Clientes (nombre, telefono) VALUES (%s, %s)", (nombre, telefono))
    id_cliente = cursor.lastrowid
    cursor.execute(
        "INSERT INTO Ordenes (id_cliente, descripcion, precio, estado) VALUES (%s, %s, %s, %s)",
        (id_cliente, descripcion, precio, "Pendiente")
    )
    conexion.commit()

def registrar_log(id_orden, accion, detalle=""):
    check_connection()
    query = "INSERT INTO Logs (id_orden, fecha, accion, detalle) VALUES (NOW(), %s, %s, %s)"
    cursor = conexion.cursor()
    cursor.execute(query, (id_orden, accion, detalle))
    conexion.commit()

def actualizar_estado_orden(id_orden, nuevo_estado):
    check_connection()
    query = "UPDATE Ordenes SET estado = %s WHERE id_orden = %s"
    cursor = conexion.cursor()
    cursor.execute(query, (nuevo_estado, id_orden))
    conexion.commit()

def get_total_abonos_por_orden(id_orden):
    check_connection()
    query = "SELECT SUM(monto) FROM Abonos WHERE id_orden = %s"
    cursor = conexion.cursor()
    cursor.execute(query, (id_orden,))
    resultado = cursor.fetchone()[0]
    return float(resultado) if resultado is not None else 0.0

def eliminar_abonos_por_orden(id_orden):
    check_connection()
    query = "DELETE FROM Abonos WHERE id_orden = %s"
    cursor = conexion.cursor()
    cursor.execute(query, (id_orden,))
    conexion.commit()

def eliminar_orden(id_orden):
    check_connection()
    eliminar_abonos_por_orden(id_orden)
    query = "DELETE FROM Ordenes WHERE id_orden = %s"
    cursor = conexion.cursor()
    cursor.execute(query, (id_orden,))
    conexion.commit()
