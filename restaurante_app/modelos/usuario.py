from dataclasses import dataclass


@dataclass
class Usuario:
    """
    Representa a una persona registrada en el sistema.
    """

    identificacion: str
    nombre: str
    correo: str
    usuario: str = ""
    rol: str = "Cliente"

    ROLES_VALIDOS = (
        "Administrador",
        "Empleado",
        "Cliente"
    )

    def __post_init__(self) -> None:
        self.identificacion = self.identificacion.strip()
        self.nombre = self.nombre.strip()
        self.correo = self.correo.strip()
        self.usuario = self.usuario.strip()
        self.rol = self.rol.strip()

        if not self.identificacion:
            raise ValueError(
                "La identificación no puede estar vacía."
            )

        if not self.nombre:
            raise ValueError(
                "El nombre no puede estar vacío."
            )

        if not self.correo:
            raise ValueError(
                "El correo no puede estar vacío."
            )

        if not self.usuario:
            # Compatibilidad con usuarios anteriores.
            self.usuario = self.correo.split("@")[0]

        if self.rol not in self.ROLES_VALIDOS:
            raise ValueError(
                "El rol debe ser Administrador, Empleado o Cliente."
            )

    def es_administrador(self) -> bool:
        """
        Indica si el usuario tiene permisos administrativos.
        """
        return self.rol == "Administrador"

    def to_dict(self) -> dict[str, str]:
        """
        Convierte el usuario a un diccionario compatible con JSON.
        """
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "correo": self.correo,
            "usuario": self.usuario,
            "rol": self.rol
        }

    def __str__(self) -> str:
        return (
            f"ID: {self.identificacion} | "
            f"Nombre: {self.nombre} | "
            f"Usuario: {self.usuario} | "
            f"Correo: {self.correo} | "
            f"Rol: {self.rol}"
        )