import mysql.connector
from mysql.connector import Error
import os

# Configurar idioma para evitar errores de localización
os.environ['LANGUAGE'] = 'en_US'

# Declarar la conexión como variable global
conexion = None

try:
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="PAIN_FULL_INK_DB"
    )
    if conexion.is_connected():
        print("✅ Conexión a la base de datos MySQL establecida.")
    else:
        print("❌ Conexión fallida.")
        conexion = None
except Error as e:
    print(f"❌ Error al conectar a la base de datos: {e}")
    conexion = None
