# Sistema de Gestión de Inventario — API REST & Dashboard Web

Este proyecto es un sistema integral de gestión de inventario desarrollado con **Python (Flask)** y **SQLite**, que expone una **API RESTful** para realizar operaciones CRUD sobre categorías y productos con relación de uno a muchos (1:N). Incluye un **Dashboard Web** desarrollado con HTML, CSS y JavaScript vanilla que consume la API directamente.

---

## 📋 Información del Proyecto

* **Universidad:** Universidad de Sonora
* **Materia:** Desarrollo de Sistemas IV
* **Profesor:** Iván Dostoyewski Meza Ibarra
* **Semestre:** 2026-1
* **Integrantes:**
  * Victoria Vargas Encinas
  * Joaquín Dávila Arenas

---

## 🚀 Características Principales

* **API RESTful Completa:** Soporte para los métodos HTTP `GET`, `POST`, `PUT` y `DELETE`.
* **Integridad Referencial:** Control de llaves foráneas activado con `PRAGMA foreign_keys = ON`.
* **Protección de Datos:** Validación que impide eliminar categorías que contengan productos asociados.
* **Actualización Parcial (PUT):** Permite modificar campos específicos conservando los valores no enviados.
* **Frontend Integrado:** Dashboard interactivo basado en paneles (Formularios y Tablas en tiempo real).
* **Notificaciones Dinámicas:** Notificaciones tipo *toast* y diálogos de confirmación.

---

## 🛠️ Tecnologías Utilizadas

* **Backend:** Python 3, Flask
* **Base de Datos:** SQLite
* **Frontend:** HTML5, CSS3, JavaScript (Vanilla ES6 / Fetch API)

---

## 📂 Estructura del Proyecto

```text
.
├── tienda.py          # Script de inicialización (Crea la BD y las tablas)
├── app.py             # Servidor Flask con los endpoints de la API
├── tienda.db          # Base de datos SQLite (se genera automáticamente)
└── templates/
    └── index.html     # Interfaz de usuario (HTML, CSS y JS embebido)
