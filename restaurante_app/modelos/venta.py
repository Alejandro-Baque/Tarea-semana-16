from datetime import datetime


class Venta:
    """
    Representa una venta realizada por un usuario
    sobre un producto del restaurante.
    """

    def __init__(
        self,
        usuario_id: str,
        producto_codigo: str,
        cantidad: int,
        fecha: str | None = None
    ) -> None:
        if not usuario_id.strip():
            raise ValueError(
                "La identificación del usuario no puede estar vacía."
            )

        if not producto_codigo.strip():
            raise ValueError(
                "El código del producto no puede estar vacío."
            )

        if cantidad <= 0:
            raise ValueError(
                "La cantidad vendida debe ser mayor que cero."
            )

        self.usuario_id = usuario_id.strip()
        self.producto_codigo = producto_codigo.strip()
        self.cantidad = cantidad

        if fecha is None:
            self.fecha = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        else:
            self.fecha = fecha.strip()

    def to_dict(self) -> dict[str, str | int]:
        """
        Convierte la venta en un diccionario compatible con JSON.
        """
        return {
            "usuario_id": self.usuario_id,
            "producto_codigo": self.producto_codigo,
            "cantidad": self.cantidad,
            "fecha": self.fecha
        }

    def __str__(self) -> str:
        return (
            f"Usuario: {self.usuario_id} | "
            f"Producto: {self.producto_codigo} | "
            f"Cantidad: {self.cantidad} | "
            f"Fecha: {self.fecha}"
        )