import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'tienda_user',    
    'password': 'Andres123',   
    'database': 'tienda_db'
}
def get_conn():
    """Establece y devuelve una conexión a la base de datos."""
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Error de conexión a la BD: {err}")
        return None