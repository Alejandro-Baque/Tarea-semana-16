import tkinter as tk

from modelos.usuario import Usuario
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView


class RestauranteApp:
    """
    Clase principal de restaurante_app.

    Coordina la creación de la ventana, el servicio principal
    y la navegación entre LoginView y MainView.
    """

    def __init__(self) -> None:
        self.root = tk.Tk()

        self.root.title("Restaurante App")
        self.root.geometry("620x480")

        # Servicio único compartido por toda la aplicación.
        self.restaurante_servicio = RestauranteServicio()

        self.vista_actual = None

        self._mostrar_login()

    # ==========================================================
    # NAVEGACIÓN
    # ==========================================================

    def _limpiar_vista_actual(self) -> None:
        """
        Elimina la vista actual antes de mostrar otra.
        """
        if self.vista_actual is not None:
            self.vista_actual.destroy()
            self.vista_actual = None

    def _mostrar_login(self) -> None:
        """
        Muestra la pantalla de inicio de sesión.
        """
        self._limpiar_vista_actual()

        self.vista_actual = LoginView(
            master=self.root,
            restaurante_servicio=self.restaurante_servicio,
            on_login_success=self._mostrar_main
        )

    def _mostrar_main(
        self,
        usuario: Usuario
    ) -> None:
        """
        Muestra la interfaz principal después
        de un inicio de sesión correcto.
        """
        self._limpiar_vista_actual()

        self.vista_actual = MainView(
            master=self.root,
            restaurante_servicio=self.restaurante_servicio,
            usuario_actual=usuario,
            on_logout=self._cerrar_sesion
        )

    def _cerrar_sesion(self) -> None:
        """
        Regresa a la pantalla de inicio de sesión.
        """
        self._mostrar_login()

    # ==========================================================
    # EJECUCIÓN
    # ==========================================================

    def ejecutar(self) -> None:
        """
        Inicia el ciclo principal de Tkinter.
        """
        self.root.mainloop()


if __name__ == "__main__":
    aplicacion = RestauranteApp()
    aplicacion.ejecutar()