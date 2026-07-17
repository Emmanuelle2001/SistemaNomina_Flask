CREATE DATABASE IF NOT EXISTS sistema_nomina;
USE sistema_nomina;

CREATE TABLE IF NOT EXISTS departamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS empleados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    puesto VARCHAR(100) NOT NULL,
    salario_base DECIMAL(10, 2) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    fecha_ingreso DATE NOT NULL,
    id_departamento INT,
    FOREIGN KEY (id_departamento) REFERENCES departamentos(id) ON DELETE SET NULL
);

INSERT INTO departamentos (nombre) VALUES 
('Sistemas y Desarrollo'),
('Recursos Humanos'),
('Finanzas');

INSERT INTO empleados (nombre, puesto, salario_base, email, fecha_ingreso, id_departamento) VALUES
('Juan Pérez', 'Desarrollador Junior', 18500.00, 'juan.perez@empresa.com', '2026-01-15', 1),
('Ana Gómez', 'Analista de RH', 15000.50, 'ana.gomez@empresa.com', '2025-08-10', 2),
('Carlos López', 'Contador Senior', 25000.00, 'carlos.lopez@empresa.com', '2026-03-01', 3);

SELECT * FROM departamentos;
SELECT * FROM empleados;