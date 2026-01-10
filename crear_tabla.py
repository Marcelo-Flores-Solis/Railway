import mysql.connector

# CONFIGURACIÓN PÚBLICA (La que funciona desde tu casa)
config = {
    'host': 'ballast.proxy.rlwy.net',        # Tu Host Público
    'user': 'root',
    'password': 'hiOlGXJZEDkyQKWcrxzISOsRaXGcBpho', # Tu contraseña
    'database': 'railway',                   # Nombre de la DB
    'port': 15344                            # Tu Puerto Público (¡OJO: 15344!)
}

try:
    print(f"Conectando a {config['host']}...")
    conexion = mysql.connector.connect(**config)
    cursor = conexion.cursor()

    # SQL para crear la tabla
    sql = """
    CREATE TABLE IF NOT EXISTS mensajes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL,
        mensaje TEXT NOT NULL,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    cursor.execute(sql)
    print("tabla creada")
    
    # Insertamos un mensaje de prueba para que no se vea vacío
    cursor.execute("INSERT INTO mensajes (nombre, email, mensaje) VALUES ('Sistema', 'admin@railway.app', 'Base de datos inicializada correctamente')")
    conexion.commit()

except Exception as e:
    print(f"Error: {e}")

finally:
    if 'conexion' in locals() and conexion.is_connected():
        cursor.close()
        conexion.close()