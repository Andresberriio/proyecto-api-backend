
from fastapi import APIRouter, HTTPException
from typing import List
from database.database import get_conn 
from models.producto_model import Producto 

router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)

@router.get("/", response_model=List[Producto])
def listar_productos():
    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos")
        productos_raw = cursor.fetchall()
        productos_lista = []
        for row in productos_raw:
            productos_lista.append(
                Producto(
                    id=row["idproductos"],
                    nombre=row["nombre"],
                    precio=float(row["precio"]),
                    disponible=bool(row["disponible"]),
                    descripcion=row["descripcion"]
                )
            )
        return productos_lista
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error del servidor: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

@router.post("/", response_model=Producto, status_code=201)
def crear_producto(producto: Producto):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        sql = "INSERT INTO productos (nombre, precio, disponible, descripcion) VALUES (%s, %s, %s, %s)"
        val = (producto.nombre, producto.precio, producto.disponible, producto.descripcion)
        cursor.execute(sql, val)
        conn.commit()
        producto.id = cursor.lastrowid
        return producto
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error del servidor: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

@router.get("/{id}", response_model=Producto)
def obtener_producto(id: int):
    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos WHERE idproductos = %s", (id,))
        producto = cursor.fetchone()
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        return Producto(
            id=producto["idproductos"],
            nombre=producto["nombre"],
            precio=float(producto["precio"]),
            disponible=bool(producto["disponible"]),
            descripcion=producto["descripcion"]
        )
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail=f"Error del servidor: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

@router.put("/{id}", response_model=Producto)
def actualizar_producto(id: int, producto: Producto):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        sql = "UPDATE productos SET nombre = %s, precio = %s, disponible = %s, descripcion = %s WHERE idproductos = %s"
        val = (producto.nombre, producto.precio, producto.disponible, producto.descripcion, id)
        cursor.execute(sql, val)
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        producto.id = id
        return producto
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail=f"Error del servidor: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

@router.delete("/{id}", status_code=204)
def eliminar_producto(id: int):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE idproductos = %s", (id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail=f"Error del servidor: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()