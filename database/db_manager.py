import mysql.connector

# --- CONFIGURACIÓN DE LA BASE DE DATOS ---
# (Debe estar aquí afuera, al principio del archivo)
DB_CONFIG = {
    'host': 'ballast.proxy.rlwy.net',        # Tu Host Público
    'user': 'root',
    'password': 'hiOlGXJZEDkyQKWcrxzISOsRaXGcBpho', # Tu contraseña
    'database': 'railway',                   # Nombre de la base de datos
    'port': 15344                            # Tu Puerto Público
}

def guardar_mensaje(nombre, email, mensaje):
    """Guarda un nuevo contacto en la base de datos"""
    conexion = None
    try:
        print(f"Conectando a: {DB_CONFIG['host']}...") # DEBUG
        
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
        
        cursor.execute("SELECT id, nombre, email, mensaje, fecha FROM mensajes ORDER BY fecha DESC")
        resultados = cursor.fetchall()
        
        for row in resultados:
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
        filas_html = f"<tr><td colspan='5'>Error de conexión: {err}</td></tr>"
    finally:
        if conexion and conexion.is_connected():
            cursor.close()
            conexion.close()
            
    return filas_html