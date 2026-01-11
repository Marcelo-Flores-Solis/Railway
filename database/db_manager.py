import mysql.connector

# --- CONFIGURACIÓN DE LA BASE DE DATOS ---
DB_CONFIG = {
    'host': 'ballast.proxy.rlwy.net',       
    'user': 'root',
    'password': 'hiOlGXJZEDkyQKWcrxzISOsRaXGcBpho', 
    'database': 'railway',                   
    'port': 15344                           
}

def guardar_mensaje(nombre, email, mensaje):
    """Guarda un nuevo contacto en la base de datos"""
    conexion = None
    try:
        print(f"Conectando a: {DB_CONFIG['host']}...") 
        
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

def obtener_estadisticas():
    """Calcula datos para el dashboard"""
    stats = {"total": 0, "usuarios": 0, "ultimo": "N/A"}
    conexion = None
    try:
        conexion = mysql.connector.connect(**DB_CONFIG)
        cursor = conexion.cursor()
        
       
        cursor.execute("SELECT COUNT(*) FROM mensajes")
        stats["total"] = cursor.fetchone()[0]
        
       
        cursor.execute("SELECT COUNT(DISTINCT email) FROM mensajes")
        stats["usuarios"] = cursor.fetchone()[0]
        
        
        cursor.execute("SELECT fecha FROM mensajes ORDER BY id DESC LIMIT 1")
        res = cursor.fetchone()
        if res:
            stats["ultimo"] = str(res[0]).split()[0] 
            
    except Exception as e:
        print(f"Error Stats: {e}")
    finally:
        if conexion and conexion.is_connected():
            cursor.close()
            conexion.close()
    return stats