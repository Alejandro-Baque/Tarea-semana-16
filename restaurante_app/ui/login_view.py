import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable

from modelos.usuario import Usuario
from servicios.restaurante_servicio import RestauranteServicio


class LoginView(ttk.Frame):
    """
    Vista encargada del inicio de sesión del sistema.

    La interfaz obtiene los datos ingresados por el usuario
    y delega la validación a RestauranteServicio.
    """

    def __init__(
        self,
        master: tk.Tk,
        restaurante_servicio: RestauranteServicio,
        on_login_success: Callable[[Usuario], None]
    ) -> None:
        super().__init__(master)

        self.master = master
        self.restaurante_servicio = restaurante_servicio
        self.on_login_success = on_login_success

        self.identificacion_var = tk.StringVar()
        self.correo_var = tk.StringVar()

        self._configurar_ventana()
        self._crear_estilos()
        self._crear_interfaz()

    # ==========================================================
    # CONFIGURACIÓN
    # ==========================================================

    def _configurar_ventana(self) -> None:
        """Configura la ventana de inicio de sesión."""

        self.master.title(
            "Restaurante App - Inicio de sesión"
        )

        self.master.geometry("620x480")
        self.master.minsize(560, 430)

        self.master.configure(
            background="#f4f4f4"
        )

        self.pack(
            fill="both",
            expand=True
        )

    def _crear_estilos(self) -> None:
        """Configura estilos visuales para la interfaz."""

        estilo = ttk.Style()

        estilo.configure(
            "Titulo.TLabel",
            font=("Segoe UI", 22, "bold")
        )

        estilo.configure(
            "Subtitulo.TLabel",
            font=("Segoe UI", 11)
        )

        estilo.configure(
            "Campo.TLabel",
            font=("Segoe UI", 10, "bold")
        )

        estilo.configure(
            "Accion.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=10
        )

    # ==========================================================
    # INTERFAZ
    # ==========================================================

    def _crear_interfaz(self) -> None:
        """Construye los componentes visuales del login."""

        contenedor = ttk.Frame(
            self,
            padding=35
        )

        contenedor.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        titulo = ttk.Label(
            contenedor,
            text="Restaurante App",
            style="Titulo.TLabel"
        )

        titulo.grid(
            row=0,
            column=0,
            columnspan=2,
            pady=(0, 8)
        )

        subtitulo = ttk.Label(
            contenedor,
            text="Inicio de sesión",
            style="Subtitulo.TLabel"
        )

        subtitulo.grid(
            row=1,
            column=0,
            columnspan=2,
            pady=(0, 28)
        )

        etiqueta_identificacion = ttk.Label(
            contenedor,
            text="Identificación:",
            style="Campo.TLabel"
        )

        etiqueta_identificacion.grid(
            row=2,
            column=0,
            sticky="w",
            pady=(0, 6)
        )

        entrada_identificacion = ttk.Entry(
            contenedor,
            textvariable=self.identificacion_var,
            width=35
        )

        entrada_identificacion.grid(
            row=3,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(0, 18)
        )

        etiqueta_correo = ttk.Label(
            contenedor,
            text="Correo electrónico:",
            style="Campo.TLabel"
        )

        etiqueta_correo.grid(
            row=4,
            column=0,
            sticky="w",
            pady=(0, 6)
        )

        entrada_correo = ttk.Entry(
            contenedor,
            textvariable=self.correo_var,
            width=35
        )

        entrada_correo.grid(
            row=5,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(0, 25)
        )

        boton_ingresar = ttk.Button(
            contenedor,
            text="Iniciar sesión",
            command=self._iniciar_sesion,
            style="Accion.TButton"
        )

        boton_ingresar.grid(
            row=6,
            column=0,
            columnspan=2,
            sticky="ew"
        )

        mensaje = ttk.Label(
            contenedor,
            text=(
                "Ingrese la identificación y el correo "
                "de un usuario registrado."
            ),
            style="Subtitulo.TLabel",
            wraplength=360,
            justify="center"
        )

        mensaje.grid(
            row=7,
            column=0,
            columnspan=2,
            pady=(22, 0)
        )

        contenedor.columnconfigure(
            0,
            weight=1
        )

        contenedor.columnconfigure(
            1,
            weight=1
        )

        entrada_identificacion.focus_set()

    # ==========================================================
    # CALLBACK
    # ==========================================================

    def _iniciar_sesion(self) -> None:
        """
        Callback asociado al botón Iniciar sesión.

        Obtiene los datos de la interfaz y solicita
        la validación a RestauranteServicio.
        """

        identificacion = (
            self.identificacion_var.get().strip()
        )

        correo = (
            self.correo_var.get().strip()
        )

        if not identificacion:
            messagebox.showwarning(
                "Datos incompletos",
                "Ingrese la identificación."
            )
            return

        if not correo:
            messagebox.showwarning(
                "Datos incompletos",
                "Ingrese el correo electrónico."
            )
            return

        usuario = (
            self.restaurante_servicio.validar_login(
                identificacion,
                correo
            )
        )

        if usuario is None:
            messagebox.showerror(
                "Acceso denegado",
                (
                    "La identificación o el correo "
                    "no son correctos."
                )
            )
            return

        messagebox.showinfo(
            "Bienvenido",
            f"Bienvenido, {usuario.nombre}."
        )

        self.on_login_success(usuario)