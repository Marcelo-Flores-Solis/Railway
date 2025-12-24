import mysql.connector

# Configuracion de conexion a WampServer
DB_CONFIG = {
    'host': os.environ.get('MYSQLHOST', 'localhost'),
    'user': os.environ.get('MYSQLUSER', 'root'),
    'password': os.environ.get('MYSQLPASSWORD', ''),
    'database': os.environ.get('MYSQLDATABASE', 'cefiro_db'),
    'port': int(os.environ.get('MYSQLPORT', 3306))
}

def guardar_mensaje(nombre, email, mensaje):
    """Guarda un nuevo contacto en la base de datos"""
    conexion = None
    try:
        conexion = mysql.connector.connect(**DB_CONFIG)
        cursor = conexion.cursor()
        
        sql = "INSERT INTO mensajes (nombre, email, mensaje) VALUES (%s, %s, %s)"
        val = (nombre, email, mensaje)
        
        cursor.execute(sql, val)
        conexion.commit()
        print("DB: Mensaje guardado correctamente.")
        
    except mysql.connector.Error as err:
        print(f"DB Error: {err}")
    finally:
        if conexion and conexion.is_connected():
            cursor.close()
            conexion.close()

def obtener_mensajes():
    """Devuelve las filas HTML para la tabla de admin"""
    conexion = None
    filas_html = ""
    try:
        conexion = mysql.connector.connect(**DB_CONFIG)
        cursor = conexion.cursor()
        
        # Ordenamos por fecha descendente (lo mas nuevo primero)
        cursor.execute("SELECT id, nombre, email, mensaje, fecha FROM mensajes ORDER BY fecha DESC")
        resultados = cursor.fetchall()
        
        for row in resultados:
            # Construimos el HTML aqui para que el server.py este limpio
            filas_html += f"""
            <tr>
                <td>{row[0]}</td>
                <td>{row[1]}</td>
                <td>{row[2]}</td>
                <td>{row[3]}</td>
                <td>{row[4]}</td>
            </tr>
            """
            
    except mysql.connector.Error as err:
        print(f"DB Error: {err}")
        filas_html = "<tr><td colspan='5'>Error de conexión a la base de datos</td></tr>"
    finally:
        if conexion and conexion.is_connected():
            cursor.close()
            conexion.close()
            
    return filas_html