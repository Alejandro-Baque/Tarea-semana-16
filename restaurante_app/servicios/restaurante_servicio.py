from pathlib import Path

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio


class RestauranteServicio:
    """
    Servicio principal de restaurante_app.

    Administra productos, usuarios y ventas, aplica las reglas
    de negocio y coordina la persistencia mediante ArchivoServicio.
    """

    def __init__(self) -> None:
        # ======================================================
        # COLECCIONES PRINCIPALES
        # ======================================================

        self._productos: list[Producto] = []
        self._usuarios: list[Usuario] = []
        self._ventas: list[Venta] = []

        # ======================================================
        # ÍNDICES AUXILIARES
        # ======================================================

        self._productos_por_codigo: dict[str, Producto] = {}
        self._usuarios_por_id: dict[str, Usuario] = {}
        self._ventas_por_usuario: dict[str, list[Venta]] = {}

        # ======================================================
        # RUTAS DE PERSISTENCIA
        # ======================================================

        directorio_base = Path(__file__).resolve().parent.parent
        directorio_datos = directorio_base / "datos"

        self._archivo_servicio = ArchivoServicio(
            ruta_productos=str(
                directorio_datos / "productos.json"
            ),
            ruta_usuarios=str(
                directorio_datos / "usuarios.json"
            ),
            ruta_ventas=str(
                directorio_datos / "ventas.json"
            )
        )

        self._cargar_datos()

    # ==========================================================
    # CARGA INICIAL
    # ==========================================================

    def _cargar_datos(self) -> None:
        """
        Recupera productos, usuarios y ventas desde JSON
        y reconstruye los índices auxiliares.
        """

        productos = self._archivo_servicio.cargar_productos()
        usuarios = self._archivo_servicio.cargar_usuarios()
        ventas = self._archivo_servicio.cargar_ventas()

        self.cargar_productos(productos)
        self.cargar_usuarios(usuarios)
        self.cargar_ventas(ventas)

    # ==========================================================
    # LOGIN Y PERMISOS
    # ==========================================================

    def validar_login(
        self,
        identificacion: str,
        correo: str
    ) -> Usuario | None:
        """
        Valida el acceso utilizando identificación y correo.
        """

        usuario = self.buscar_usuario(identificacion)

        if usuario is None:
            return None

        if usuario.correo.strip().lower() != correo.strip().lower():
            return None

        return usuario

    def puede_gestionar_usuarios(
        self,
        usuario_actual: Usuario
    ) -> bool:
        """
        Indica si el usuario autenticado puede acceder
        a la gestión administrativa de usuarios.
        """

        return usuario_actual.es_administrador()

    # ==========================================================
    # PRODUCTOS
    # ==========================================================

    def registrar_producto(
        self,
        producto: Producto
    ) -> bool:
        """
        Registra un producto y actualiza su persistencia.
        """

        clave = producto.codigo.strip().lower()

        if clave in self._productos_por_codigo:
            return False

        self._productos.append(producto)
        self._productos_por_codigo[clave] = producto

        if not self._archivo_servicio.guardar_productos(
            self._productos
        ):
            self._productos.remove(producto)
            del self._productos_por_codigo[clave]
            return False

        return True

    def cargar_productos(
        self,
        productos: list[Producto]
    ) -> None:
        """
        Carga productos y reconstruye el índice por código.
        """

        self._productos.clear()
        self._productos_por_codigo.clear()

        for producto in productos:
            clave = producto.codigo.strip().lower()

            if clave not in self._productos_por_codigo:
                self._productos.append(producto)
                self._productos_por_codigo[clave] = producto

    def buscar_producto(
        self,
        codigo: str
    ) -> Producto | None:
        """Busca un producto mediante su código."""

        clave = codigo.strip().lower()

        return self._productos_por_codigo.get(clave)

    def actualizar_producto(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: float,
        stock: int
    ) -> bool:
        """
        Actualiza los datos de un producto.
        """

        producto = self.buscar_producto(codigo)

        if producto is None:
            return False

        try:
            producto.nombre = nombre
            producto.categoria = categoria
            producto.precio = precio
            producto.stock = stock

        except ValueError:
            return False

        return self._archivo_servicio.guardar_productos(
            self._productos
        )

    def eliminar_producto(
        self,
        codigo: str
    ) -> bool:
        """
        Elimina un producto de la colección y del índice.
        """

        clave = codigo.strip().lower()

        producto = self._productos_por_codigo.get(clave)

        if producto is None:
            return False

        self._productos.remove(producto)
        del self._productos_por_codigo[clave]

        if not self._archivo_servicio.guardar_productos(
            self._productos
        ):
            self._productos.append(producto)
            self._productos_por_codigo[clave] = producto
            return False

        return True

    def listar_productos(self) -> list[Producto]:
        """Devuelve una copia de los productos."""

        return self._productos.copy()

    # ==========================================================
    # USUARIOS
    # ==========================================================

    def cargar_usuarios(
        self,
        usuarios: list[Usuario]
    ) -> None:
        """
        Carga usuarios y reconstruye el índice
        por identificación.
        """

        self._usuarios.clear()
        self._usuarios_por_id.clear()

        for usuario in usuarios:
            clave = usuario.identificacion.strip().lower()

            if clave not in self._usuarios_por_id:
                self._usuarios.append(usuario)
                self._usuarios_por_id[clave] = usuario

    def buscar_usuario(
        self,
        identificacion: str
    ) -> Usuario | None:
        """
        Busca un usuario mediante su identificación.
        """

        clave = identificacion.strip().lower()

        return self._usuarios_por_id.get(clave)

    def listar_usuarios(self) -> list[Usuario]:
        """
        Devuelve una copia de los usuarios registrados.
        """

        return self._usuarios.copy()

    def _existe_usuario_repetido(
        self,
        nombre_usuario: str,
        correo: str,
        identificacion_ignorada: str | None = None
    ) -> bool:
        """
        Comprueba si ya existe el nombre de usuario
        o correo electrónico.
        """

        nombre_usuario = nombre_usuario.strip().lower()
        correo = correo.strip().lower()

        for usuario in self._usuarios:
            if (
                identificacion_ignorada is not None
                and usuario.identificacion.strip().lower()
                == identificacion_ignorada.strip().lower()
            ):
                continue

            if usuario.usuario.strip().lower() == nombre_usuario:
                return True

            if usuario.correo.strip().lower() == correo:
                return True

        return False

    def registrar_usuario(
        self,
        usuario: Usuario,
        usuario_actual: Usuario
    ) -> tuple[bool, str]:
        """
        Registra un nuevo usuario.

        La operación solo puede ser realizada por
        un usuario con rol Administrador.
        """

        if not self.puede_gestionar_usuarios(
            usuario_actual
        ):
            return (
                False,
                "Solo un Administrador puede registrar usuarios."
            )

        clave = usuario.identificacion.strip().lower()

        if clave in self._usuarios_por_id:
            return (
                False,
                "Ya existe un usuario con esa identificación."
            )

        if self._existe_usuario_repetido(
            usuario.usuario,
            usuario.correo
        ):
            return (
                False,
                "El nombre de usuario o correo ya está registrado."
            )

        self._usuarios.append(usuario)
        self._usuarios_por_id[clave] = usuario

        if not self._archivo_servicio.guardar_usuarios(
            self._usuarios
        ):
            self._usuarios.remove(usuario)
            del self._usuarios_por_id[clave]

            return (
                False,
                "No fue posible guardar el usuario."
            )

        return (
            True,
            "Usuario registrado correctamente."
        )

    def actualizar_usuario(
        self,
        identificacion: str,
        nombre: str,
        correo: str,
        nombre_usuario: str,
        rol: str,
        usuario_actual: Usuario
    ) -> tuple[bool, str]:
        """
        Actualiza un usuario existente.

        La identificación se utiliza como clave del registro
        y no se modifica.
        """

        if not self.puede_gestionar_usuarios(
            usuario_actual
        ):
            return (
                False,
                "Solo un Administrador puede actualizar usuarios."
            )

        usuario = self.buscar_usuario(
            identificacion
        )

        if usuario is None:
            return (
                False,
                "El usuario seleccionado no existe."
            )

        if self._existe_usuario_repetido(
            nombre_usuario,
            correo,
            identificacion_ignorada=identificacion
        ):
            return (
                False,
                "El nombre de usuario o correo ya pertenece a otro usuario."
            )

        # Evita que el administrador autenticado
        # elimine accidentalmente su propio permiso.
        if (
            usuario.identificacion.strip().lower()
            == usuario_actual.identificacion.strip().lower()
            and rol != "Administrador"
        ):
            return (
                False,
                "No puede quitar el rol Administrador "
                "a la cuenta actualmente autenticada."
            )

        try:
            datos_nuevos = Usuario(
                identificacion=usuario.identificacion,
                nombre=nombre,
                correo=correo,
                usuario=nombre_usuario,
                rol=rol
            )

        except ValueError as error:
            return (
                False,
                str(error)
            )

        datos_anteriores = (
            usuario.nombre,
            usuario.correo,
            usuario.usuario,
            usuario.rol
        )

        usuario.nombre = datos_nuevos.nombre
        usuario.correo = datos_nuevos.correo
        usuario.usuario = datos_nuevos.usuario
        usuario.rol = datos_nuevos.rol

        if not self._archivo_servicio.guardar_usuarios(
            self._usuarios
        ):
            (
                usuario.nombre,
                usuario.correo,
                usuario.usuario,
                usuario.rol
            ) = datos_anteriores

            return (
                False,
                "No fue posible guardar los cambios del usuario."
            )

        return (
            True,
            "Usuario actualizado correctamente."
        )

    def eliminar_usuario(
        self,
        identificacion: str,
        usuario_actual: Usuario
    ) -> tuple[bool, str]:
        """
        Elimina un usuario existente.

        Impide que el administrador autenticado
        pueda eliminar su propia cuenta.
        """

        if not self.puede_gestionar_usuarios(
            usuario_actual
        ):
            return (
                False,
                "Solo un Administrador puede eliminar usuarios."
            )

        usuario = self.buscar_usuario(
            identificacion
        )

        if usuario is None:
            return (
                False,
                "El usuario seleccionado no existe."
            )

        if (
            usuario.identificacion.strip().lower()
            == usuario_actual.identificacion.strip().lower()
        ):
            return (
                False,
                "No puede eliminar la cuenta "
                "que tiene la sesión iniciada."
            )

        clave = usuario.identificacion.strip().lower()

        posicion = self._usuarios.index(usuario)

        self._usuarios.remove(usuario)
        del self._usuarios_por_id[clave]

        if not self._archivo_servicio.guardar_usuarios(
            self._usuarios
        ):
            self._usuarios.insert(
                posicion,
                usuario
            )

            self._usuarios_por_id[clave] = usuario

            return (
                False,
                "No fue posible eliminar el usuario."
            )

        return (
            True,
            "Usuario eliminado correctamente."
        )

    # ==========================================================
    # VENTAS
    # ==========================================================

    def cargar_ventas(
        self,
        ventas: list[Venta]
    ) -> None:
        """
        Carga las ventas y reconstruye el índice
        agrupado por usuario.
        """

        self._ventas.clear()
        self._ventas_por_usuario.clear()

        for venta in ventas:
            self._ventas.append(venta)

            clave_usuario = venta.usuario_id.strip().lower()

            if clave_usuario not in self._ventas_por_usuario:
                self._ventas_por_usuario[
                    clave_usuario
                ] = []

            self._ventas_por_usuario[
                clave_usuario
            ].append(venta)

    def registrar_venta(
        self,
        identificacion_usuario: str,
        codigo_producto: str,
        cantidad: int = 1
    ) -> tuple[bool, str]:
        """
        Valida y registra una venta.
        """

        usuario = self.buscar_usuario(
            identificacion_usuario
        )

        if usuario is None:
            return (
                False,
                "El usuario seleccionado no existe."
            )

        producto = self.buscar_producto(
            codigo_producto
        )

        if producto is None:
            return (
                False,
                "El producto seleccionado no existe."
            )

        if cantidad <= 0:
            return (
                False,
                "La cantidad debe ser mayor que cero."
            )

        if producto.stock < cantidad:
            return (
                False,
                "No existe stock suficiente para realizar la venta."
            )

        stock_anterior = producto.stock

        try:
            venta = Venta(
                usuario_id=usuario.identificacion,
                producto_codigo=producto.codigo,
                cantidad=cantidad
            )

            producto.vender(cantidad)

        except ValueError as error:
            return (
                False,
                str(error)
            )

        self._ventas.append(venta)

        clave_usuario = usuario.identificacion.strip().lower()

        if clave_usuario not in self._ventas_por_usuario:
            self._ventas_por_usuario[
                clave_usuario
            ] = []

        self._ventas_por_usuario[
            clave_usuario
        ].append(venta)

        productos_guardados = (
            self._archivo_servicio.guardar_productos(
                self._productos
            )
        )

        ventas_guardadas = (
            self._archivo_servicio.guardar_ventas(
                self._ventas
            )
        )

        if not productos_guardados or not ventas_guardadas:
            producto.stock = stock_anterior

            self._ventas.remove(venta)

            self._ventas_por_usuario[
                clave_usuario
            ].remove(venta)

            if not self._ventas_por_usuario[
                clave_usuario
            ]:
                del self._ventas_por_usuario[
                    clave_usuario
                ]

            self._archivo_servicio.guardar_productos(
                self._productos
            )

            self._archivo_servicio.guardar_ventas(
                self._ventas
            )

            return (
                False,
                "No fue posible guardar la venta."
            )

        return (
            True,
            "Venta registrada correctamente."
        )

    def vender_producto(
        self,
        codigo_producto: str,
        identificacion_usuario: str,
        cantidad: int
    ) -> bool:
        """
        Mantiene compatibilidad con versiones anteriores.
        """

        resultado, _ = self.registrar_venta(
            identificacion_usuario,
            codigo_producto,
            cantidad
        )

        return resultado

    def consultar_ventas_usuario(
        self,
        identificacion_usuario: str
    ) -> list[Venta]:
        """
        Consulta las ventas de un usuario.
        """

        clave = identificacion_usuario.strip().lower()

        return self._ventas_por_usuario.get(
            clave,
            []
        ).copy()

    def listar_ventas(self) -> list[Venta]:
        """
        Devuelve una copia de las ventas.
        """

        return self._ventas.copy()

    # ==========================================================
    # INFORMACIÓN PARA INTERFAZ
    # ==========================================================

    def obtener_nombre_usuario(
        self,
        identificacion: str
    ) -> str:
        """Obtiene el nombre de un usuario."""

        usuario = self.buscar_usuario(
            identificacion
        )

        if usuario is None:
            return "Usuario no disponible"

        return usuario.nombre

    def obtener_nombre_producto(
        self,
        codigo: str
    ) -> str:
        """Obtiene el nombre de un producto."""

        producto = self.buscar_producto(
            codigo
        )

        if producto is None:
            return "Producto no disponible"

        return producto.nombre

    def obtener_categorias(self) -> set[str]:
        """
        Devuelve las categorías únicas de productos.
        """

        return {
            producto.categoria
            for producto in self._productos
        }