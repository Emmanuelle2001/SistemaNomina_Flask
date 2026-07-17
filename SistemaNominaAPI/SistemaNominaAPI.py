from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',        
            password='2704',
            database='sistema_nomina'
        )
        return connection
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

@app.route('/empleados', methods=['GET'])
def get_empleados():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Error interno del servidor al conectar a la BD"}), 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nombre, puesto, CAST(salario_base AS DOUBLE) as salario_base, email FROM empleados")
    empleados = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return jsonify(empleados), 200

@app.route('/empleados', methods=['POST'])
def crear_empleado():
    datos = request.get_json()
    nombre = datos.get('nombre')
    puesto = datos.get('puesto')
    salario_base = datos.get('salario_base')
    email = datos.get('email')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        query = "INSERT INTO empleados (nombre, puesto, salario_base, email, fecha_ingreso) VALUES (%s, %s, %s, %s, CURDATE())"
        cursor.execute(query, (nombre, puesto, salario_base, email))
        conn.commit()
        nuevo_id = cursor.lastrowid
        
        return jsonify({"id": nuevo_id, "nombre": nombre, "puesto": puesto, "salario_base": salario_base, "email": email}), 201
    except Error as e:
        return jsonify({"error": f"No se pudo insertar el registro: {e}"}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/empleados/<int:id>', methods=['PUT'])
def actualizar_empleado(id):
    datos = request.get_json()
    nombre = datos.get('nombre')
    puesto = datos.get('puesto')
    salario_base = datos.get('salario_base')
    email = datos.get('email')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        query = "UPDATE empleados SET nombre=%s, puesto=%s, salario_base=%s, email=%s WHERE id=%s"
        cursor.execute(query, (nombre, puesto, salario_base, email, id))
        conn.commit()
        return jsonify({"id": id, "nombre": nombre, "puesto": puesto, "salario_base": salario_base, "email": email}), 200
    except Error as e:
        return jsonify({"error": f"No se pudo actualizar: {e}"}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/empleados/<int:id>', methods=['DELETE'])
def eliminar_empleado(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        query = "DELETE FROM empleados WHERE id = %s"
        cursor.execute(query, (id,))
        conn.commit()
        return '', 204
    except Error as e:
        return jsonify({"error": f"No se pudo eliminar: {e}"}), 400
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)