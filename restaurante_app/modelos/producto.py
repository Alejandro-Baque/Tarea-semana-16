class Producto:
    """
    Representa un producto disponible en el restaurante.
    """

    def __init__(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: float,
        stock: int
    ) -> None:
        self.codigo = codigo
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.stock = stock

    @property
    def codigo(self) -> str:
        return self._codigo

    @codigo.setter
    def codigo(self, codigo: str) -> None:
        if not codigo.strip():
            raise ValueError("El código no puede estar vacío.")

        self._codigo = codigo.strip()

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, nombre: str) -> None:
        if not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")

        self._nombre = nombre.strip()

    @property
    def categoria(self) -> str:
        return self._categoria

    @categoria.setter
    def categoria(self, categoria: str) -> None:
        if not categoria.strip():
            raise ValueError("La categoría no puede estar vacía.")

        self._categoria = categoria.strip()

    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, precio: float) -> None:
        if precio <= 0:
            raise ValueError("El precio debe ser mayor que cero.")

        self._precio = precio

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, stock: int) -> None:
        if stock < 0:
            raise ValueError(
                "El stock no puede ser negativo."
            )

        self._stock = stock

    def vender(self, cantidad: int) -> None:
        """
        Disminuye el stock del producto después de una venta válida.
        """
        if cantidad <= 0:
            raise ValueError(
                "La cantidad vendida debe ser mayor que cero."
            )

        if cantidad > self.stock:
            raise ValueError(
                "No existe stock suficiente para realizar la venta."
            )

        self.stock -= cantidad

    def to_dict(self) -> dict[str, str | float | int]:
        """
        Convierte el objeto Producto en un diccionario
        compatible con JSON.
        """
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "stock": self.stock
        }

    def __str__(self) -> str:
        return (
            f"Código: {self.codigo} | "
            f"Nombre: {self.nombre} | "
            f"Categoría: {self.categoria} | "
            f"Precio: ${self.precio:.2f} | "
            f"Stock: {self.stock}"
        )