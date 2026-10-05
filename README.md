# Restaurante App - Semana 16

## Programación Orientada a Objetos

**Estudiante:** Byron Alejandro Baque Tsahuanda  
**Actividad:** Tarea Semana 16  
**Tema:** Manejo de eventos en Tkinter  

---

## Descripción del proyecto

Restaurante App es una aplicación desarrollada en Python para gestionar productos, usuarios y ventas de un restaurante.

La versión correspondiente a la Semana 16 continúa el desarrollo realizado en semanas anteriores y conserva la arquitectura modular, la interfaz gráfica con Tkinter/ttk, la persistencia mediante archivos JSON, el inicio de sesión, la gestión de productos y el registro de ventas.

Durante esta semana se evolucionó específicamente la sección de Usuarios para implementar un CRUD completo y aplicar eventos mediante `bind()` y callbacks.

---

## Evolución realizada en la Semana 16

En esta versión se incorporaron las siguientes mejoras:

- Se mantuvo la arquitectura modular del proyecto.
- Se conservaron las secciones Productos y Ventas.
- Se mantuvo el inicio de sesión.
- Se agregó el atributo `rol` al modelo `Usuario`.
- Se incorporaron los roles:
  - Administrador
  - Empleado
  - Cliente
- Se implementó la gestión completa de usuarios.
- Se permite registrar usuarios.
- Se permite consultar usuarios.
- Se permite actualizar usuarios.
- Se permite eliminar usuarios.
- Se incorporó un formulario de usuarios.
- Se agregó un `Treeview` para mostrar los usuarios registrados.
- Se incorporó un `Combobox` para seleccionar el rol.
- Se implementó `<<TreeviewSelect>>`.
- Se implementó `<Return>`.
- Se implementó `<Escape>`.
- Se implementó `<<ComboboxSelected>>`.
- Se mantuvo `command=` en los botones principales.
- Se reutilizan métodos existentes dentro de los callbacks.
- Las validaciones y la persistencia continúan delegándose a `RestauranteServicio`.
- Se implementó control básico de acceso por roles.
- Solo el Administrador puede gestionar usuarios.
- Se impide eliminar accidentalmente la cuenta Administrador que mantiene la sesión activa.
- Se mantiene el uso de logo e íconos desde la carpeta `assets/`.

---

## Estructura del proyecto

```text
restaurante_app/
├── assets/
│   ├── logo.png
│   ├── icon_productos.png
│   ├── icon_usuarios.png
│   └── icon_ventas.png
│
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
│
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
│
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
│
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
│
└── main.py