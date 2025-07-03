CREATE DATABASE PAIN_FULL_INK_DB;

USE PAIN_FULL_INK_DB;

CREATE TABLE Clientes (
id_cliente INT PRIMARY KEY AUTO_INCREMENT,
nombre VARCHAR(100) NOT NULL,
telefono VARCHAR(20),
fecha_registro DATE DEFAULT CURRENT_DATE
);

CREATE TABLE Ordenes (
id_orden INT PRIMARY KEY AUTO_INCREMENT,
id_cliente INT NOT NULL,
descripcion VARCHAR(255),
precio DECIMAL(10,2) NOT NULL,
fecha_creacion DATE DEFAULT CURRENT_DATE,
FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente)
);

CREATE TABLE Abonos (
id_abono INT PRIMARY KEY AUTO_INCREMENT,
id_orden INT NOT NULL,
fecha_abono DATE NOT NULL,
monto DECIMAL(10,2) NOT NULL,
FOREIGN KEY (id_orden) REFERENCES Ordenes(id_orden)
);
CREATE TABLE LOGS (
    id_log INTEGER PRIMARY KEY AUTOINCREMENT,
    id_orden INTEGER NOT NULL,
    fecha TEXT NOT NULL,
    accion TEXT NOT NULL,
    detalle TEXT,
    FOREIGN KEY (id_orden) REFERENCES Ordenes(id_orden)
);