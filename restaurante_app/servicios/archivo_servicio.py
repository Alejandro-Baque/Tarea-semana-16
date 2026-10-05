import json

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class ArchivoServicio:
    """
    Servicio encargado de guardar y cargar productos,
    usuarios y ventas utilizando archivos JSON.
    """

    def __init__(
        self,
        ruta_productos: str,
        ruta_usuarios: str,
        ruta_ventas: str
    ) -> None:
        self.ruta_productos = ruta_productos
        self.ruta_usuarios = ruta_usuarios
        self.ruta_ventas = ruta_ventas

    # ==========================================================
    # PRODUCTOS
    # ==========================================================

    def guardar_productos(
        self,
        productos: list[Producto]
    ) -> bool:
        """Guarda los productos en formato JSON."""

        datos = [
            producto.to_dict()
            for producto in productos
        ]

        try:
            with open(
                self.ruta_productos,
                "w",
                encoding="utf-8"
            ) as archivo:
                json.dump(
                    datos,
                    archivo,
                    indent=4,
                    ensure_ascii=False
                )

            return True

        except PermissionError:
            print(
                "Error: no existen permisos para escribir "
                "el archivo de productos."
            )
            return False

        except OSError as error:
            print(
                f"Error al guardar los productos: {error}"
            )
            return False

    def cargar_productos(self) -> list[Producto]:
        """Carga y reconstruye los productos desde JSON."""

        productos: list[Producto] = []

        try:
            with open(
                self.ruta_productos,
                "r",
                encoding="utf-8"
            ) as archivo:
                datos = json.load(archivo)

            if not isinstance(datos, list):
                print(
                    "Error: productos.json debe contener "
                    "una lista."
                )
                return productos

            for registro in datos:
                try:
                    producto = Producto(
                        codigo=registro["codigo"],
                        nombre=registro["nombre"],
                        categoria=registro["categoria"],
                        precio=float(registro["precio"]),
                        stock=int(registro["stock"])
                    )

                    productos.append(producto)

                except KeyError as error:
                    print(
                        "Advertencia: se omitió un producto "
                        f"porque falta la clave {error}."
                    )

                except (TypeError, ValueError) as error:
                    print(
                        "Advertencia: se omitió un producto "
                        f"con datos inválidos: {error}"
                    )

        except FileNotFoundError:
            print(
                "Información: productos.json todavía no existe."
            )

        except json.JSONDecodeError:
            print(
                "Error: productos.json no contiene "
                "un JSON válido."
            )

        except PermissionError:
            print(
                "Error: no existen permisos para leer "
                "productos.json."
            )

        except OSError as error:
            print(
                f"Error al leer productos.json: {error}"
            )

        return productos

    # ==========================================================
    # USUARIOS
    # ==========================================================

    def guardar_usuarios(
        self,
        usuarios: list[Usuario]
    ) -> bool:
        """
        Guarda los usuarios en usuarios.json,
        incluyendo usuario y rol.
        """

        datos = [
            usuario.to_dict()
            for usuario in usuarios
        ]

        try:
            with open(
                self.ruta_usuarios,
                "w",
                encoding="utf-8"
            ) as archivo:
                json.dump(
                    datos,
                    archivo,
                    indent=4,
                    ensure_ascii=False
                )

            return True

        except PermissionError:
            print(
                "Error: no existen permisos para escribir "
                "el archivo de usuarios."
            )
            return False

        except OSError as error:
            print(
                f"Error al guardar los usuarios: {error}"
            )
            return False

    def cargar_usuarios(self) -> list[Usuario]:
        """
        Carga y reconstruye los usuarios desde usuarios.json.

        También mantiene compatibilidad con usuarios antiguos
        que todavía no tengan usuario o rol.
        """

        usuarios: list[Usuario] = []

        try:
            with open(
                self.ruta_usuarios,
                "r",
                encoding="utf-8"
            ) as archivo:
                datos = json.load(archivo)

            if not isinstance(datos, list):
                print(
                    "Error: usuarios.json debe contener "
                    "una lista."
                )
                return usuarios

            for registro in datos:
                try:
                    correo = registro["correo"]

                    usuario = Usuario(
                        identificacion=registro["identificacion"],
                        nombre=registro["nombre"],
                        correo=correo,
                        usuario=registro.get(
                            "usuario",
                            correo.split("@")[0]
                        ),
                        rol=registro.get(
                            "rol",
                            "Cliente"
                        )
                    )

                    usuarios.append(usuario)

                except KeyError as error:
                    print(
                        "Advertencia: se omitió un usuario "
                        f"porque falta la clave {error}."
                    )

                except (TypeError, ValueError) as error:
                    print(
                        "Advertencia: se omitió un usuario "
                        f"con datos inválidos: {error}"
                    )

        except FileNotFoundError:
            print(
                "Información: usuarios.json todavía no existe."
            )

        except json.JSONDecodeError:
            print(
                "Error: usuarios.json no contiene "
                "un JSON válido."
            )

        except PermissionError:
            print(
                "Error: no existen permisos para leer "
                "usuarios.json."
            )

        except OSError as error:
            print(
                f"Error al leer usuarios.json: {error}"
            )

        return usuarios

    # ==========================================================
    # VENTAS
    # ==========================================================

    def guardar_ventas(
        self,
        ventas: list[Venta]
    ) -> bool:
        """Guarda las ventas en formato JSON."""

        datos = [
            venta.to_dict()
            for venta in ventas
        ]

        try:
            with open(
                self.ruta_ventas,
                "w",
                encoding="utf-8"
            ) as archivo:
                json.dump(
                    datos,
                    archivo,
                    indent=4,
                    ensure_ascii=False
                )

            return True

        except PermissionError:
            print(
                "Error: no existen permisos para escribir "
                "el archivo de ventas."
            )
            return False

        except OSError as error:
            print(
                f"Error al guardar las ventas: {error}"
            )
            return False

    def cargar_ventas(self) -> list[Venta]:
        """Carga y reconstruye las ventas desde JSON."""

        ventas: list[Venta] = []

        try:
            with open(
                self.ruta_ventas,
                "r",
                encoding="utf-8"
            ) as archivo:
                datos = json.load(archivo)

            if not isinstance(datos, list):
                print(
                    "Error: ventas.json debe contener "
                    "una lista."
                )
                return ventas

            for registro in datos:
                try:
                    venta = Venta(
                        usuario_id=registro["usuario_id"],
                        producto_codigo=registro[
                            "producto_codigo"
                        ],
                        cantidad=int(
                            registro["cantidad"]
                        ),
                        fecha=registro.get(
                            "fecha",
                            "Registro anterior"
                        )
                    )

                    ventas.append(venta)

                except KeyError as error:
                    print(
                        "Advertencia: se omitió una venta "
                        f"porque falta la clave {error}."
                    )

                except (TypeError, ValueError) as error:
                    print(
                        "Advertencia: se omitió una venta "
                        f"con datos inválidos: {error}"
                    )

        except FileNotFoundError:
            print(
                "Información: ventas.json todavía no existe."
            )

        except json.JSONDecodeError:
            print(
                "Error: ventas.json no contiene "
                "un JSON válido."
            )

        except PermissionError:
            print(
                "Error: no existen permisos para leer "
                "ventas.json."
            )

        except OSError as error:
            print(
                f"Error al leer ventas.json: {error}"
            )

        return ventas