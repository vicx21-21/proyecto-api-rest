import sqlite3

conn = sqlite3.connect("tienda.db")
cursor = conn.cursor()

# Borramos si existen para empezar de cero y limpio
cursor.execute("DROP TABLE IF EXISTS productos")
cursor.execute("DROP TABLE IF EXISTS categorias")

# Creamos Categorías
cursor.execute("""
    CREATE TABLE categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE
    )
""")

# Creamos Productos con la columna que te faltaba
cursor.execute("""
    CREATE TABLE productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL,
        stock INTEGER NOT NULL,
        categoria_id INTEGER,
        FOREIGN KEY (categoria_id) REFERENCES categorias(id)
    )
""")

conn.commit()
conn.close()
print("Base de datos creada :)")