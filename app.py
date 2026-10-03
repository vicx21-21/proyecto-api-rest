from flask import Flask, jsonify, request, render_template
import sqlite3

app = Flask(__name__)

def conexionDB():
    conn = sqlite3.connect("tienda.db")
    conn.row_factory = sqlite3.Row # Esto ayuda a que los datos sean más fáciles de manejar
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# RUTA PARA CARGAR LA INTERFAZ 
@app.route("/")
def index():
    return render_template("index.html")

# --- ENTIDAD CATEGORIAS ---
#Crear una categoria nueva usando POST
@app.route("/categorias", methods=["POST"])
def agregarCategoria():
    data = request.json
    try:
        conn = conexionDB()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO categorias (nombre) VALUES (?)", (data["nombre"],))
        conn.commit()
        return jsonify({"mensaje": "Categoría creada"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()
#actualizar categorias por id usando PUT
@app.route("/categorias/<int:id>", methods=["PUT"])
def actualizarCategoria(id):
    data = request.json
    # Validación de datos (Punto V)
    if "nombre" not in data:
        return jsonify({"error": "El nombre es obligatorio"}), 400
    
    try:
        conn = conexionDB()
        cursor = conn.cursor()
        # Verificamos si la categoría existe primero
        cursor.execute("UPDATE categorias SET nombre = ? WHERE id = ?", (data["nombre"], id))
        conn.commit()
        #si no se encontro la categoria 
        if cursor.rowcount == 0:
            return jsonify({"error": "Categoría no encontrada"}), 404
        #si si se encontro    
        return jsonify({"mensaje": "Categoría actualizada correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()
#Eliminar categoria por id
@app.route("/categorias/<int:id>", methods=["DELETE"])
def eliminarCategoria(id):
    try:
        conn = conexionDB()
        cursor = conn.cursor()

        # VALIDACIÓN: Contar productos relacionados
        cursor.execute("SELECT COUNT(*) FROM productos WHERE categoria_id = ?", (id,))
        cantidad_productos = cursor.fetchone()[0]
        #Si existe la categoria pero esta relaccionada a un producto no se podra eliminar
        if cantidad_productos > 0:
            return jsonify({
                "error": f"No se puede eliminar: esta categoría tiene {cantidad_productos} productos asociados."
            }), 400

        # Si llegamos aquí, la categoría está vacía y se puede borrar
        cursor.execute("DELETE FROM categorias WHERE id = ?", (id,))
        conn.commit()
        #si no eciste la categroia
        if cursor.rowcount == 0:
            return jsonify({"error": "Categoría no encontrada"}), 404
        #devuelve mensaje de que si se pudo eliminar
        return jsonify({"mensaje": "Categoría eliminada con éxito"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

#Obtener todas las categorias
@app.route("/categorias", methods=["GET"])
def obtenerCategorias():
    try:
        conn = conexionDB()
        cursor = conn.cursor()
        # Traemos todas las columnas de la tabla padre
        cursor.execute("SELECT * FROM categorias")
        datos = cursor.fetchall()
        
        # Estructuramos los datos para que el JS los entienda fácil
        categorias = []
        for fila in datos:
            categorias.append({
                "id": fila[0],
                "nombre": fila[1]
            })
            
        return jsonify(categorias), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()
 #Obtener una categoria por su id        
@app.route("/categorias/<int:id>", methods=["GET"])
def obtenerCategoriaPorId(id):
    try:
        conn = conexionDB()
        cursor = conn.cursor()
        
        # Buscamos la categoría por su ID
        cursor.execute("SELECT id, nombre FROM categorias WHERE id = ?", (id,))
        fila = cursor.fetchone()
        
        if fila:
            # Si existe, devolvemos el objeto JSON
            return jsonify({
                "id": fila[0],
                "nombre": fila[1]
            }), 200
        else:
            # Si no existe, devolvemos error 404
            return jsonify({"error": "Categoría no encontrada"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()
 # Obtener los productos de una categoría específica (Para la tabla relacional)
@app.route("/categorias/<int:id>/productos", methods=["GET"])
def obtenerProductosPorCategoria(id):
    try:
        conn = conexionDB()
        cursor = conn.cursor()
        # Buscamos solo los productos que tengan el categoria_id solicitado
        cursor.execute("SELECT id, nombre FROM productos WHERE categoria_id = ?", (id,))
        filas = cursor.fetchall()
        
        productos = []
        for f in filas:
            productos.append({"id": f[0], "nombre": f[1]})
            
        return jsonify({"productos": productos}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


# --- ENTIDAD PRODUCTOS (Con FK a Categorias) ---
#Crear un nuevo producto
@app.route("/productos", methods=["POST"])
def agregarProducto():
    data = request.json
    # Validación de seguridad básica (Punto V)
    if "nombre" not in data or "categoria_id" not in data:
        return jsonify({"error": "Faltan campos obligatorios"}), 400
    
    try:
        conn = conexionDB()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO productos (nombre, precio, stock, categoria_id) 
            VALUES (?, ?, ?, ?)
        """, (data["nombre"], data["precio"], data["stock"], data["categoria_id"]))
        conn.commit()
        return jsonify({"mensaje": "Producto creado"}), 201
    #si no existe el id de la categoria mandara error
    except sqlite3.IntegrityError:
        return jsonify({"error": "La categoría no existe"}), 400
    finally:
        conn.close()
#Obtener todos los productos que existen
@app.route("/productos", methods=["GET"])
def obtenerProductos():
    try:
        conn = conexionDB()
        cursor = conn.cursor()
        # Unimos productos (p) con categorias (c) usando la Foreign Key
        cursor.execute("""
            SELECT p.id, p.nombre, p.precio, p.stock, p.categoria_id, c.nombre
            FROM productos p
            INNER JOIN categorias c ON p.categoria_id = c.id
        """)
        datos = cursor.fetchall()
        
        productos = []
        for fila in datos:
            productos.append({
                "id": fila[0],
                "nombre": fila[1],
                "precio": fila[2],
                "stock": fila[3],
                "categoria_id": fila[4],
                "categoria_nombre": fila[5]  # <--- aqui pone el nombre de la categoria relaccionada al id
            })
        return jsonify(productos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()
 #obtener un producto por su id       
@app.route("/productos/<int:id>", methods=["GET"])
def obtenerProductoPorId(id):
    try:
        conn = conexionDB()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id, p.nombre, p.precio, p.stock, p.categoria_id, c.nombre
            FROM productos p
            INNER JOIN categorias c ON p.categoria_id = c.id
            WHERE p.id = ?
        """, (id,))
        fila = cursor.fetchone()
        
        if fila:
            producto = {
                "id": fila[0],
                "nombre": fila[1],
                "precio": fila[2],
                "stock": fila[3],
                "categoria_id": fila[4],
                "categoria_nombre": fila[5] #lo mismo de arriba,se relacciona la id de la categoria y se pone el nombre tambien
            }
            return jsonify(producto), 200
        else:
            return jsonify({"error": "Producto no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()
#Eliminar un producto por su id
@app.route("/productos/<int:id>", methods=["DELETE"])
def eliminarProducto(id):
    try:
        conn = conexionDB()
        cursor = conn.cursor()
        
        # 1. Intentar eliminar el producto por su ID
        cursor.execute("DELETE FROM productos WHERE id = ?", (id,))
        conn.commit()
        
        # 2. Verificar si realmente se borró algo (si el ID existía)
        if cursor.rowcount == 0:
            return jsonify({"error": "El producto no existe"}), 404
         #mensaje de exito   
        return jsonify({"mensaje": "Producto eliminado con éxito"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()
#Actualizar un producto por id 
@app.route("/productos/<int:id>", methods=["PUT"])
def actualizarProducto(id):
    try:
        data = request.json
        conn = conexionDB()
        cursor = conn.cursor()

        # 1. Buscamos los datos actuales del producto antes de cambiar nada
        cursor.execute("SELECT nombre, precio, stock, categoria_id FROM productos WHERE id = ?", (id,))
        producto_actual = cursor.fetchone()

        if not producto_actual:
            return jsonify({"error": "Producto no encontrado"}), 404

        # 2. Usamos el valor nuevo SI viene en el JSON, si no, dejamos el que ya estaba
        # data.get("campo", valor_por_defecto)
        #esto facilita al usuario solo escribir el valor que quiere cambiar
        nombre = data.get("nombre", producto_actual[0])
        precio = data.get("precio", producto_actual[1])
        stock = data.get("stock", producto_actual[2])
        categoria_id = data.get("categoria_id", producto_actual[3])

        # 3. Ejecutamos la actualización con los valores finales
        cursor.execute("""
            UPDATE productos 
            SET nombre = ?, precio = ?, stock = ?, categoria_id = ?
            WHERE id = ?
        """, (nombre, precio, stock, categoria_id, id))
        
        conn.commit()
        return jsonify({"mensaje": "Producto actualizado con éxito"}), 200
    #Errores por si no existe

    except sqlite3.IntegrityError:
        return jsonify({"error": "Error de integridad: el producto no existe"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


if __name__ == "__main__":
    app.run(debug=True)