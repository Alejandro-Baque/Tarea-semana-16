import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk
from typing import Callable

from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.restaurante_servicio import RestauranteServicio


class MainView(ttk.Frame):
    """
    Vista principal de restaurante_app.

    Coordina la interacción gráfica y delega las operaciones
    de negocio y persistencia a RestauranteServicio.
    """

    def __init__(
        self,
        master: tk.Tk,
        restaurante_servicio: RestauranteServicio,
        usuario_actual: Usuario,
        on_logout: Callable[[], None]
    ) -> None:
        super().__init__(master)

        self.master = master
        self.restaurante_servicio = restaurante_servicio
        self.usuario_actual = usuario_actual
        self.on_logout = on_logout

        # Variables del formulario de productos.
        self.codigo_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.categoria_var = tk.StringVar()
        self.precio_var = tk.StringVar()
        self.stock_var = tk.StringVar()

        # Variables del formulario de usuarios.
        self.usuario_id_var = tk.StringVar()
        self.usuario_nombre_var = tk.StringVar()
        self.usuario_usuario_var = tk.StringVar()
        self.usuario_correo_var = tk.StringVar()
        self.usuario_rol_var = tk.StringVar(value="Cliente")
        self.usuario_evento_var = tk.StringVar(
            value="Seleccione o registre un usuario."
        )
        self._usuario_seleccionado_id: str | None = None

        # Variables del formulario de ventas.
        self.usuario_venta_var = tk.StringVar()
        self.producto_venta_var = tk.StringVar()
        self.cantidad_venta_var = tk.StringVar(value="1")

        # Relación entre texto mostrado en Combobox y claves reales.
        self._usuarios_combo: dict[str, str] = {}
        self._productos_combo: dict[str, str] = {}

        # Recursos gráficos cargados desde assets/.
        self.logo_imagen: tk.PhotoImage | None = None
        self.icon_productos: tk.PhotoImage | None = None
        self.icon_usuarios: tk.PhotoImage | None = None
        self.icon_ventas: tk.PhotoImage | None = None

        self._configurar_ventana()
        self._crear_estilos()
        self._cargar_recursos()
        self._crear_interfaz()
        self._configurar_eventos_generales()
        self._actualizar_todo()

    # ==========================================================
    # CONFIGURACIÓN GENERAL
    # ==========================================================

    def _configurar_ventana(self) -> None:
        """Configura la ventana principal."""
        self.master.title("Restaurante App - Sistema de Gestión")
        self.master.geometry("1120x780")
        self.master.minsize(1000, 700)

        self.pack(
            fill="both",
            expand=True
        )

    def _crear_estilos(self) -> None:
        """Configura estilos generales de la aplicación."""
        estilo = ttk.Style()

        estilo.configure(
            "Titulo.TLabel",
            font=("Segoe UI", 20, "bold")
        )

        estilo.configure(
            "Subtitulo.TLabel",
            font=("Segoe UI", 11)
        )

        estilo.configure(
            "Seccion.TLabel",
            font=("Segoe UI", 14, "bold")
        )

        estilo.configure(
            "Campo.TLabel",
            font=("Segoe UI", 10, "bold")
        )

        estilo.configure(
            "Ayuda.TLabel",
            font=("Segoe UI", 9)
        )

        estilo.configure(
            "Accion.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=8
        )

        estilo.configure(
            "Treeview",
            rowheight=28,
            font=("Segoe UI", 10)
        )

        estilo.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold")
        )

    def _cargar_recursos(self) -> None:
        """
        Carga el logo y los íconos almacenados
        en la carpeta assets.
        """
        ruta_base = Path(__file__).resolve().parent.parent
        ruta_assets = ruta_base / "assets"

        try:
            ruta_logo = ruta_assets / "logo.png"
            if ruta_logo.exists():
                self.logo_imagen = tk.PhotoImage(
                    file=str(ruta_logo)
                ).subsample(3, 3)

            ruta_productos = ruta_assets / "icon_productos.png"
            if ruta_productos.exists():
                self.icon_productos = tk.PhotoImage(
                    file=str(ruta_productos)
                ).subsample(2, 2)

            ruta_usuarios = ruta_assets / "icon_usuarios.png"
            if ruta_usuarios.exists():
                self.icon_usuarios = tk.PhotoImage(
                    file=str(ruta_usuarios)
                ).subsample(2, 2)

            ruta_ventas = ruta_assets / "icon_ventas.png"
            if ruta_ventas.exists():
                self.icon_ventas = tk.PhotoImage(
                    file=str(ruta_ventas)
                ).subsample(2, 2)

        except tk.TclError:
            self.logo_imagen = None
            self.icon_productos = None
            self.icon_usuarios = None
            self.icon_ventas = None

    def _configurar_eventos_generales(self) -> None:
        """
        Asocia los eventos de teclado requeridos en Semana 16.
        """
        self.master.bind(
            "<Return>",
            self._evento_return
        )

        self.master.bind(
            "<Escape>",
            self._evento_escape
        )

    # ==========================================================
    # INTERFAZ PRINCIPAL
    # ==========================================================

    def _crear_interfaz(self) -> None:
        """Construye la interfaz principal."""
        self._crear_encabezado()

        self.notebook = ttk.Notebook(self)

        self.notebook.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=(0, 18)
        )

        self.frame_productos = ttk.Frame(
            self.notebook,
            padding=18
        )

        self.frame_usuarios = ttk.Frame(
            self.notebook,
            padding=18
        )

        self.frame_ventas = ttk.Frame(
            self.notebook,
            padding=18
        )

        self.notebook.add(
            self.frame_productos,
            text=" Productos",
            image=self.icon_productos if self.icon_productos else "",
            compound="left"
        )

        self.notebook.add(
            self.frame_usuarios,
            text=" Usuarios",
            image=self.icon_usuarios if self.icon_usuarios else "",
            compound="left"
        )

        self.notebook.add(
            self.frame_ventas,
            text=" Ventas",
            image=self.icon_ventas if self.icon_ventas else "",
            compound="left"
        )

        self._crear_seccion_productos()
        self._crear_seccion_usuarios()
        self._crear_seccion_ventas()

        # Solo un Administrador puede acceder a la gestión
        # administrativa de usuarios.
        if not self.restaurante_servicio.puede_gestionar_usuarios(
            self.usuario_actual
        ):
            self.notebook.tab(
                self.frame_usuarios,
                state="disabled"
            )

    # ==========================================================
    # ENCABEZADO
    # ==========================================================

    def _crear_encabezado(self) -> None:
        """Crea el encabezado principal."""
        encabezado = ttk.Frame(
            self,
            padding=(20, 14)
        )

        encabezado.pack(fill="x")

        columna_titulo = 0

        if self.logo_imagen is not None:
            etiqueta_logo = ttk.Label(
                encabezado,
                image=self.logo_imagen
            )

            etiqueta_logo.grid(
                row=0,
                column=0,
                rowspan=2,
                padx=(0, 14)
            )

            columna_titulo = 1

        titulo = ttk.Label(
            encabezado,
            text="Restaurante App",
            style="Titulo.TLabel"
        )

        titulo.grid(
            row=0,
            column=columna_titulo,
            sticky="w"
        )

        usuario_label = ttk.Label(
            encabezado,
            text=(
                f"Sesión iniciada: {self.usuario_actual.nombre} "
                f"| Rol: {self.usuario_actual.rol}"
            ),
            style="Subtitulo.TLabel"
        )

        usuario_label.grid(
            row=1,
            column=columna_titulo,
            sticky="w"
        )

        boton_salir = ttk.Button(
            encabezado,
            text="Cerrar sesión",
            command=self._cerrar_sesion
        )

        boton_salir.grid(
            row=0,
            column=columna_titulo + 1,
            rowspan=2,
            padx=(20, 0)
        )

        encabezado.columnconfigure(
            columna_titulo,
            weight=1
        )

    # ==========================================================
    # PRODUCTOS
    # ==========================================================

    def _crear_seccion_productos(self) -> None:
        """Construye la gestión visual de productos."""
        titulo = ttk.Label(
            self.frame_productos,
            text="Gestión de productos",
            style="Seccion.TLabel"
        )

        titulo.pack(
            anchor="w",
            pady=(0, 15)
        )

        contenido = ttk.Frame(self.frame_productos)

        contenido.pack(
            fill="both",
            expand=True
        )

        formulario = ttk.LabelFrame(
            contenido,
            text="Datos del producto",
            padding=15
        )

        formulario.pack(
            side="left",
            fill="y",
            padx=(0, 15)
        )

        self._crear_campo_producto(
            formulario,
            "Código:",
            self.codigo_var,
            0
        )

        self._crear_campo_producto(
            formulario,
            "Nombre:",
            self.nombre_var,
            1
        )

        self._crear_campo_producto(
            formulario,
            "Categoría:",
            self.categoria_var,
            2
        )

        self._crear_campo_producto(
            formulario,
            "Precio:",
            self.precio_var,
            3
        )

        self._crear_campo_producto(
            formulario,
            "Stock:",
            self.stock_var,
            4
        )

        botones = ttk.Frame(formulario)

        botones.grid(
            row=10,
            column=0,
            sticky="ew",
            pady=(15, 0)
        )

        ttk.Button(
            botones,
            text="Registrar",
            command=self._registrar_producto,
            style="Accion.TButton"
        ).pack(
            fill="x",
            pady=3
        )

        ttk.Button(
            botones,
            text="Cargar seleccionado",
            command=self._cargar_producto_seleccionado
        ).pack(
            fill="x",
            pady=3
        )

        ttk.Button(
            botones,
            text="Actualizar",
            command=self._actualizar_producto
        ).pack(
            fill="x",
            pady=3
        )

        ttk.Button(
            botones,
            text="Eliminar",
            command=self._eliminar_producto
        ).pack(
            fill="x",
            pady=3
        )

        ttk.Button(
            botones,
            text="Limpiar formulario",
            command=self._limpiar_formulario_producto
        ).pack(
            fill="x",
            pady=3
        )

        tabla_frame = ttk.Frame(contenido)

        tabla_frame.pack(
            side="left",
            fill="both",
            expand=True
        )

        columnas = (
            "codigo",
            "nombre",
            "categoria",
            "precio",
            "stock"
        )

        self.tabla_productos = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings"
        )

        self.tabla_productos.heading("codigo", text="Código")
        self.tabla_productos.heading("nombre", text="Nombre")
        self.tabla_productos.heading("categoria", text="Categoría")
        self.tabla_productos.heading("precio", text="Precio")
        self.tabla_productos.heading("stock", text="Stock")

        self.tabla_productos.column(
            "codigo",
            width=100,
            anchor="center"
        )

        self.tabla_productos.column(
            "nombre",
            width=180
        )

        self.tabla_productos.column(
            "categoria",
            width=140
        )

        self.tabla_productos.column(
            "precio",
            width=100,
            anchor="center"
        )

        self.tabla_productos.column(
            "stock",
            width=80,
            anchor="center"
        )

        scrollbar = ttk.Scrollbar(
            tabla_frame,
            orient="vertical",
            command=self.tabla_productos.yview
        )

        self.tabla_productos.configure(
            yscrollcommand=scrollbar.set
        )

        self.tabla_productos.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

    def _crear_campo_producto(
        self,
        contenedor: ttk.LabelFrame,
        texto: str,
        variable: tk.StringVar,
        fila: int
    ) -> None:
        """Crea un campo del formulario de productos."""
        ttk.Label(
            contenedor,
            text=texto,
            style="Campo.TLabel"
        ).grid(
            row=fila * 2,
            column=0,
            sticky="w",
            pady=(4, 2)
        )

        ttk.Entry(
            contenedor,
            textvariable=variable,
            width=28
        ).grid(
            row=(fila * 2) + 1,
            column=0,
            sticky="ew",
            pady=(0, 5)
        )

    def _registrar_producto(self) -> None:
        """Callback del botón Registrar producto."""
        try:
            producto = Producto(
                codigo=self.codigo_var.get(),
                nombre=self.nombre_var.get(),
                categoria=self.categoria_var.get(),
                precio=float(self.precio_var.get()),
                stock=int(self.stock_var.get())
            )

        except ValueError as error:
            messagebox.showerror(
                "Datos inválidos",
                str(error)
            )
            return

        resultado = self.restaurante_servicio.registrar_producto(
            producto
        )

        if not resultado:
            messagebox.showerror(
                "No se pudo registrar",
                (
                    "Ya existe un producto con ese código "
                    "o no fue posible guardar la información."
                )
            )
            return

        messagebox.showinfo(
            "Producto registrado",
            "El producto fue registrado correctamente."
        )

        self._limpiar_formulario_producto()
        self._actualizar_productos()
        self._actualizar_combobox_ventas()

    def _cargar_producto_seleccionado(self) -> None:
        """Carga en el formulario el producto seleccionado."""
        seleccion = self.tabla_productos.selection()

        if not seleccion:
            messagebox.showwarning(
                "Selección requerida",
                "Seleccione un producto de la tabla."
            )
            return

        valores = self.tabla_productos.item(
            seleccion[0],
            "values"
        )

        if not valores:
            return

        self.codigo_var.set(valores[0])
        self.nombre_var.set(valores[1])
        self.categoria_var.set(valores[2])

        precio = str(valores[3]).replace("$", "")
        self.precio_var.set(precio)

        self.stock_var.set(valores[4])

    def _actualizar_producto(self) -> None:
        """Callback para actualizar un producto existente."""
        codigo = self.codigo_var.get().strip()

        if not codigo:
            messagebox.showwarning(
                "Datos incompletos",
                "Ingrese o cargue el código del producto."
            )
            return

        try:
            precio = float(self.precio_var.get())
            stock = int(self.stock_var.get())

        except ValueError:
            messagebox.showerror(
                "Datos inválidos",
                "Precio y stock deben contener valores válidos."
            )
            return

        resultado = self.restaurante_servicio.actualizar_producto(
            codigo=codigo,
            nombre=self.nombre_var.get(),
            categoria=self.categoria_var.get(),
            precio=precio,
            stock=stock
        )

        if not resultado:
            messagebox.showerror(
                "No se pudo actualizar",
                (
                    "Verifique los datos del producto "
                    "e intente nuevamente."
                )
            )
            return

        messagebox.showinfo(
            "Producto actualizado",
            "Los datos fueron actualizados correctamente."
        )

        self._limpiar_formulario_producto()
        self._actualizar_productos()
        self._actualizar_combobox_ventas()

    def _eliminar_producto(self) -> None:
        """Callback para eliminar un producto."""
        codigo = self.codigo_var.get().strip()

        if not codigo:
            messagebox.showwarning(
                "Selección requerida",
                (
                    "Seleccione un producto y utilice "
                    "'Cargar seleccionado'."
                )
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Desea eliminar el producto {codigo}?"
        )

        if not confirmar:
            return

        resultado = self.restaurante_servicio.eliminar_producto(
            codigo
        )

        if not resultado:
            messagebox.showerror(
                "Error",
                "No fue posible eliminar el producto."
            )
            return

        messagebox.showinfo(
            "Producto eliminado",
            "El producto fue eliminado correctamente."
        )

        self._limpiar_formulario_producto()
        self._actualizar_productos()
        self._actualizar_combobox_ventas()

    def _limpiar_formulario_producto(self) -> None:
        """Limpia los campos del formulario."""
        self.codigo_var.set("")
        self.nombre_var.set("")
        self.categoria_var.set("")
        self.precio_var.set("")
        self.stock_var.set("")

    def _actualizar_productos(self) -> None:
        """Actualiza la tabla de productos."""
        for elemento in self.tabla_productos.get_children():
            self.tabla_productos.delete(elemento)

        productos = self.restaurante_servicio.listar_productos()

        for producto in productos:
            self.tabla_productos.insert(
                "",
                "end",
                values=(
                    producto.codigo,
                    producto.nombre,
                    producto.categoria,
                    f"${producto.precio:.2f}",
                    producto.stock
                )
            )

    # ==========================================================
    # USUARIOS - SEMANA 16
    # ==========================================================

    def _crear_seccion_usuarios(self) -> None:
        """
        Construye la gestión administrativa de usuarios.
        """
        ttk.Label(
            self.frame_usuarios,
            text="Gestión de usuarios",
            style="Seccion.TLabel"
        ).pack(
            anchor="w",
            pady=(0, 6)
        )

        ttk.Label(
            self.frame_usuarios,
            text=(
                "Seleccione una fila para cargar sus datos. "
                "Enter registra y Escape limpia el formulario."
            ),
            style="Ayuda.TLabel"
        ).pack(
            anchor="w",
            pady=(0, 14)
        )

        contenido = ttk.Frame(
            self.frame_usuarios
        )

        contenido.pack(
            fill="both",
            expand=True
        )

        formulario = ttk.LabelFrame(
            contenido,
            text="Datos del usuario",
            padding=15
        )

        formulario.pack(
            side="left",
            fill="y",
            padx=(0, 15)
        )

        ttk.Label(
            formulario,
            text="Identificación:",
            style="Campo.TLabel"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=(3, 2)
        )

        self.entry_usuario_id = ttk.Entry(
            formulario,
            textvariable=self.usuario_id_var,
            width=30
        )

        self.entry_usuario_id.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, 7)
        )

        ttk.Label(
            formulario,
            text="Nombre:",
            style="Campo.TLabel"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=(3, 2)
        )

        self.entry_usuario_nombre = ttk.Entry(
            formulario,
            textvariable=self.usuario_nombre_var,
            width=30
        )

        self.entry_usuario_nombre.grid(
            row=3,
            column=0,
            sticky="ew",
            pady=(0, 7)
        )

        ttk.Label(
            formulario,
            text="Usuario:",
            style="Campo.TLabel"
        ).grid(
            row=4,
            column=0,
            sticky="w",
            pady=(3, 2)
        )

        self.entry_nombre_usuario = ttk.Entry(
            formulario,
            textvariable=self.usuario_usuario_var,
            width=30
        )

        self.entry_nombre_usuario.grid(
            row=5,
            column=0,
            sticky="ew",
            pady=(0, 7)
        )

        ttk.Label(
            formulario,
            text="Correo electrónico:",
            style="Campo.TLabel"
        ).grid(
            row=6,
            column=0,
            sticky="w",
            pady=(3, 2)
        )

        self.entry_usuario_correo = ttk.Entry(
            formulario,
            textvariable=self.usuario_correo_var,
            width=30
        )

        self.entry_usuario_correo.grid(
            row=7,
            column=0,
            sticky="ew",
            pady=(0, 7)
        )

        ttk.Label(
            formulario,
            text="Rol:",
            style="Campo.TLabel"
        ).grid(
            row=8,
            column=0,
            sticky="w",
            pady=(3, 2)
        )

        self.combo_rol = ttk.Combobox(
            formulario,
            textvariable=self.usuario_rol_var,
            values=Usuario.ROLES_VALIDOS,
            state="readonly",
            width=27
        )

        self.combo_rol.grid(
            row=9,
            column=0,
            sticky="ew",
            pady=(0, 7)
        )

        # Evento obligatorio: <<ComboboxSelected>> mediante bind().
        self.combo_rol.bind(
            "<<ComboboxSelected>>",
            self._al_cambiar_rol
        )

        ttk.Label(
            formulario,
            textvariable=self.usuario_evento_var,
            style="Ayuda.TLabel",
            wraplength=250
        ).grid(
            row=10,
            column=0,
            sticky="w",
            pady=(4, 10)
        )

        botones = ttk.Frame(
            formulario
        )

        botones.grid(
            row=11,
            column=0,
            sticky="ew"
        )

        # Las acciones principales conservan command=.
        ttk.Button(
            botones,
            text="Registrar",
            command=self._registrar_usuario,
            style="Accion.TButton"
        ).pack(
            fill="x",
            pady=2
        )

        ttk.Button(
            botones,
            text="Actualizar",
            command=self._actualizar_usuario
        ).pack(
            fill="x",
            pady=2
        )

        ttk.Button(
            botones,
            text="Eliminar",
            command=self._eliminar_usuario
        ).pack(
            fill="x",
            pady=2
        )

        ttk.Button(
            botones,
            text="Limpiar",
            command=self._limpiar_formulario_usuario
        ).pack(
            fill="x",
            pady=2
        )

        tabla_frame = ttk.Frame(
            contenido
        )

        tabla_frame.pack(
            side="left",
            fill="both",
            expand=True
        )

        columnas = (
            "identificacion",
            "nombre",
            "usuario",
            "rol"
        )

        self.tabla_usuarios = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings",
            selectmode="browse"
        )

        self.tabla_usuarios.heading(
            "identificacion",
            text="Identificación"
        )

        self.tabla_usuarios.heading(
            "nombre",
            text="Nombre"
        )

        self.tabla_usuarios.heading(
            "usuario",
            text="Usuario"
        )

        self.tabla_usuarios.heading(
            "rol",
            text="Rol"
        )

        self.tabla_usuarios.column(
            "identificacion",
            width=145,
            anchor="center"
        )

        self.tabla_usuarios.column(
            "nombre",
            width=230
        )

        self.tabla_usuarios.column(
            "usuario",
            width=190
        )

        self.tabla_usuarios.column(
            "rol",
            width=130,
            anchor="center"
        )

        scrollbar = ttk.Scrollbar(
            tabla_frame,
            orient="vertical",
            command=self.tabla_usuarios.yview
        )

        self.tabla_usuarios.configure(
            yscrollcommand=scrollbar.set
        )

        self.tabla_usuarios.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # Evento obligatorio: <<TreeviewSelect>> mediante bind().
        self.tabla_usuarios.bind(
            "<<TreeviewSelect>>",
            self._al_seleccionar_usuario
        )

    def _al_seleccionar_usuario(self, event) -> None:
        """
        Callback de <<TreeviewSelect>>.

        Obtiene la identificación de la fila y consulta el objeto
        completo mediante RestauranteServicio.
        """
        seleccion = self.tabla_usuarios.selection()

        if not seleccion:
            return

        valores = self.tabla_usuarios.item(
            seleccion[0],
            "values"
        )

        if not valores:
            return

        identificacion = str(
            valores[0]
        )

        usuario = self.restaurante_servicio.buscar_usuario(
            identificacion
        )

        if usuario is None:
            messagebox.showerror(
                "Usuario no encontrado",
                "No fue posible recuperar el usuario seleccionado."
            )
            return

        self._usuario_seleccionado_id = usuario.identificacion

        self.usuario_id_var.set(
            usuario.identificacion
        )

        self.usuario_nombre_var.set(
            usuario.nombre
        )

        self.usuario_usuario_var.set(
            usuario.usuario
        )

        self.usuario_correo_var.set(
            usuario.correo
        )

        self.usuario_rol_var.set(
            usuario.rol
        )

        self.usuario_evento_var.set(
            f"Usuario seleccionado: {usuario.usuario}"
        )

        # La identificación funciona como clave y no se edita.
        self.entry_usuario_id.configure(
            state="disabled"
        )

    def _al_cambiar_rol(self, event) -> None:
        """
        Callback de <<ComboboxSelected>>.
        """
        rol = self.usuario_rol_var.get()

        self.usuario_evento_var.set(
            f"Rol seleccionado: {rol}"
        )

    def _es_pestana_usuarios_activa(self) -> bool:
        """
        Indica si la pestaña Usuarios está activa.
        """
        try:
            return (
                self.notebook.select()
                == str(self.frame_usuarios)
            )
        except tk.TclError:
            return False

    def _evento_return(self, event) -> None:
        """
        Callback de <Return>.

        Reutiliza _registrar_usuario() para no duplicar lógica.
        """
        if not self._es_pestana_usuarios_activa():
            return

        if not self.restaurante_servicio.puede_gestionar_usuarios(
            self.usuario_actual
        ):
            return

        self._registrar_usuario()

    def _evento_escape(self, event) -> None:
        """
        Callback de <Escape>.

        Limpia el formulario y cancela la selección.
        """
        if not self._es_pestana_usuarios_activa():
            return

        self._limpiar_formulario_usuario()

    def _registrar_usuario(self) -> None:
        """
        Registra un usuario delegando la operación al servicio.
        """
        if not self.restaurante_servicio.puede_gestionar_usuarios(
            self.usuario_actual
        ):
            messagebox.showerror(
                "Acceso denegado",
                "Solo un Administrador puede gestionar usuarios."
            )
            return

        if self._usuario_seleccionado_id is not None:
            messagebox.showwarning(
                "Formulario en edición",
                (
                    "Hay un usuario seleccionado. Use Actualizar "
                    "o presione Escape para limpiar."
                )
            )
            return

        rol = self.usuario_rol_var.get().strip()

        if rol not in ("Empleado", "Cliente"):
            messagebox.showwarning(
                "Rol no permitido",
                (
                    "Los nuevos usuarios deben registrarse "
                    "como Empleado o Cliente."
                )
            )
            return

        try:
            nuevo_usuario = Usuario(
                identificacion=self.usuario_id_var.get(),
                nombre=self.usuario_nombre_var.get(),
                correo=self.usuario_correo_var.get(),
                usuario=self.usuario_usuario_var.get(),
                rol=rol
            )

        except ValueError as error:
            messagebox.showerror(
                "Datos inválidos",
                str(error)
            )
            return

        exito, mensaje = self.restaurante_servicio.registrar_usuario(
            nuevo_usuario,
            self.usuario_actual
        )

        if not exito:
            messagebox.showerror(
                "Usuario no registrado",
                mensaje
            )
            return

        messagebox.showinfo(
            "Usuario registrado",
            mensaje
        )

        self._actualizar_usuarios()
        self._actualizar_combobox_ventas()
        self._limpiar_formulario_usuario()

    def _actualizar_usuario(self) -> None:
        """
        Actualiza el usuario seleccionado mediante el servicio.
        """
        if self._usuario_seleccionado_id is None:
            messagebox.showwarning(
                "Selección requerida",
                "Seleccione primero un usuario de la tabla."
            )
            return

        usuario_objetivo = self.restaurante_servicio.buscar_usuario(
            self._usuario_seleccionado_id
        )

        if usuario_objetivo is None:
            messagebox.showerror(
                "Usuario no encontrado",
                "El usuario seleccionado ya no existe."
            )
            self._limpiar_formulario_usuario()
            return

        rol = self.usuario_rol_var.get().strip()

        # La cuenta Administrador autenticada conserva su rol.
        if (
            usuario_objetivo.identificacion.strip().lower()
            == self.usuario_actual.identificacion.strip().lower()
        ):
            rol = "Administrador"
            self.usuario_rol_var.set(
                "Administrador"
            )

        elif rol not in ("Empleado", "Cliente"):
            messagebox.showwarning(
                "Rol no permitido",
                (
                    "Los usuarios administrados desde esta sección "
                    "deben ser Empleado o Cliente."
                )
            )
            return

        exito, mensaje = self.restaurante_servicio.actualizar_usuario(
            identificacion=self._usuario_seleccionado_id,
            nombre=self.usuario_nombre_var.get(),
            correo=self.usuario_correo_var.get(),
            nombre_usuario=self.usuario_usuario_var.get(),
            rol=rol,
            usuario_actual=self.usuario_actual
        )

        if not exito:
            messagebox.showerror(
                "Usuario no actualizado",
                mensaje
            )
            return

        messagebox.showinfo(
            "Usuario actualizado",
            mensaje
        )

        self._actualizar_usuarios()
        self._actualizar_combobox_ventas()
        self._limpiar_formulario_usuario()

    def _eliminar_usuario(self) -> None:
        """
        Elimina el usuario seleccionado con confirmación previa.
        """
        if self._usuario_seleccionado_id is None:
            messagebox.showwarning(
                "Selección requerida",
                "Seleccione primero un usuario de la tabla."
            )
            return

        usuario = self.restaurante_servicio.buscar_usuario(
            self._usuario_seleccionado_id
        )

        if usuario is None:
            messagebox.showerror(
                "Usuario no encontrado",
                "El usuario seleccionado ya no existe."
            )
            self._limpiar_formulario_usuario()
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            (
                f"¿Desea eliminar al usuario "
                f"{usuario.nombre} ({usuario.usuario})?"
            )
        )

        if not confirmar:
            return

        exito, mensaje = self.restaurante_servicio.eliminar_usuario(
            identificacion=usuario.identificacion,
            usuario_actual=self.usuario_actual
        )

        if not exito:
            messagebox.showerror(
                "Usuario no eliminado",
                mensaje
            )
            return

        messagebox.showinfo(
            "Usuario eliminado",
            mensaje
        )

        self._actualizar_usuarios()
        self._actualizar_combobox_ventas()
        self._limpiar_formulario_usuario()

    def _limpiar_formulario_usuario(self) -> None:
        """
        Limpia el formulario y cancela la selección del Treeview.
        """
        self._usuario_seleccionado_id = None

        self.entry_usuario_id.configure(
            state="normal"
        )

        self.usuario_id_var.set("")
        self.usuario_nombre_var.set("")
        self.usuario_usuario_var.set("")
        self.usuario_correo_var.set("")
        self.usuario_rol_var.set("Cliente")

        for item in self.tabla_usuarios.selection():
            self.tabla_usuarios.selection_remove(item)

        self.usuario_evento_var.set(
            "Formulario limpio. Puede registrar un nuevo usuario."
        )

        self.entry_usuario_id.focus_set()

    def _actualizar_usuarios(self) -> None:
        """
        Actualiza el Treeview de usuarios.
        """
        for elemento in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(elemento)

        usuarios = self.restaurante_servicio.listar_usuarios()

        for usuario in usuarios:
            self.tabla_usuarios.insert(
                "",
                "end",
                values=(
                    usuario.identificacion,
                    usuario.nombre,
                    usuario.usuario,
                    usuario.rol
                )
            )

    # ==========================================================
    # VENTAS
    # ==========================================================

    def _crear_seccion_ventas(self) -> None:
        """Construye la sección visual de ventas."""
        ttk.Label(
            self.frame_ventas,
            text="Registro de ventas",
            style="Seccion.TLabel"
        ).pack(
            anchor="w",
            pady=(0, 15)
        )

        formulario = ttk.LabelFrame(
            self.frame_ventas,
            text="Nueva venta",
            padding=15
        )

        formulario.pack(
            fill="x",
            pady=(0, 15)
        )

        ttk.Label(
            formulario,
            text="Usuario:",
            style="Campo.TLabel"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 8)
        )

        self.combo_usuario = ttk.Combobox(
            formulario,
            textvariable=self.usuario_venta_var,
            state="readonly",
            width=32
        )

        self.combo_usuario.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(0, 12),
            pady=(3, 0)
        )

        ttk.Label(
            formulario,
            text="Producto:",
            style="Campo.TLabel"
        ).grid(
            row=0,
            column=1,
            sticky="w",
            padx=(0, 8)
        )

        self.combo_producto = ttk.Combobox(
            formulario,
            textvariable=self.producto_venta_var,
            state="readonly",
            width=36
        )

        self.combo_producto.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=(0, 12),
            pady=(3, 0)
        )

        ttk.Label(
            formulario,
            text="Cantidad:",
            style="Campo.TLabel"
        ).grid(
            row=0,
            column=2,
            sticky="w"
        )

        self.spin_cantidad = ttk.Spinbox(
            formulario,
            from_=1,
            to=100,
            textvariable=self.cantidad_venta_var,
            width=8
        )

        self.spin_cantidad.grid(
            row=1,
            column=2,
            sticky="w",
            padx=(0, 12),
            pady=(3, 0)
        )

        # Fundamento de eventos Semana 15:
        # acción del usuario -> botón -> command= -> callback
        # -> RestauranteServicio -> persistencia -> respuesta visual.
        boton_registrar = ttk.Button(
            formulario,
            text="Registrar venta",
            command=self._registrar_venta,
            style="Accion.TButton"
        )

        boton_registrar.grid(
            row=1,
            column=3,
            sticky="ew",
            pady=(3, 0)
        )

        formulario.columnconfigure(0, weight=1)
        formulario.columnconfigure(1, weight=1)

        ttk.Label(
            self.frame_ventas,
            text="Ventas registradas",
            style="Campo.TLabel"
        ).pack(
            anchor="w",
            pady=(0, 6)
        )

        columnas = (
            "fecha",
            "usuario",
            "producto",
            "cantidad"
        )

        self.tabla_ventas = ttk.Treeview(
            self.frame_ventas,
            columns=columnas,
            show="headings"
        )

        self.tabla_ventas.heading("fecha", text="Fecha")
        self.tabla_ventas.heading("usuario", text="Usuario")
        self.tabla_ventas.heading("producto", text="Producto")
        self.tabla_ventas.heading("cantidad", text="Cantidad")

        self.tabla_ventas.column(
            "fecha",
            width=175,
            anchor="center"
        )

        self.tabla_ventas.column(
            "usuario",
            width=250
        )

        self.tabla_ventas.column(
            "producto",
            width=250
        )

        self.tabla_ventas.column(
            "cantidad",
            width=90,
            anchor="center"
        )

        self.tabla_ventas.pack(
            fill="both",
            expand=True
        )

    def _registrar_venta(self) -> None:
        """
        Callback ejecutado mediante command=.

        Obtiene la información de la interfaz, delega la operación
        a RestauranteServicio y actualiza la vista.
        """
        usuario_texto = self.usuario_venta_var.get()
        producto_texto = self.producto_venta_var.get()

        if not usuario_texto:
            messagebox.showwarning(
                "Datos incompletos",
                "Seleccione un usuario."
            )
            return

        if not producto_texto:
            messagebox.showwarning(
                "Datos incompletos",
                "Seleccione un producto."
            )
            return

        try:
            cantidad = int(self.cantidad_venta_var.get())

        except ValueError:
            messagebox.showerror(
                "Cantidad inválida",
                "Ingrese una cantidad válida."
            )
            return

        identificacion = self._usuarios_combo.get(
            usuario_texto
        )

        codigo_producto = self._productos_combo.get(
            producto_texto
        )

        if identificacion is None:
            messagebox.showerror(
                "Usuario inválido",
                "No fue posible identificar al usuario."
            )
            return

        if codigo_producto is None:
            messagebox.showerror(
                "Producto inválido",
                "No fue posible identificar el producto."
            )
            return

        exito, mensaje = self.restaurante_servicio.registrar_venta(
            identificacion_usuario=identificacion,
            codigo_producto=codigo_producto,
            cantidad=cantidad
        )

        if not exito:
            messagebox.showerror(
                "Venta no registrada",
                mensaje
            )
            return

        messagebox.showinfo(
            "Venta registrada",
            mensaje
        )

        self.cantidad_venta_var.set("1")

        self._actualizar_ventas()
        self._actualizar_productos()
        self._actualizar_combobox_ventas()

    def _actualizar_combobox_ventas(self) -> None:
        """
        Actualiza usuarios y productos disponibles
        en los Combobox de venta.
        """
        self._usuarios_combo.clear()
        self._productos_combo.clear()

        usuarios = self.restaurante_servicio.listar_usuarios()

        valores_usuarios: list[str] = []

        for usuario in usuarios:
            texto = (
                f"{usuario.identificacion} - "
                f"{usuario.nombre}"
            )

            valores_usuarios.append(texto)
            self._usuarios_combo[texto] = usuario.identificacion

        self.combo_usuario["values"] = valores_usuarios

        productos = self.restaurante_servicio.listar_productos()

        valores_productos: list[str] = []

        for producto in productos:
            texto = (
                f"{producto.codigo} - "
                f"{producto.nombre} "
                f"(Stock: {producto.stock})"
            )

            valores_productos.append(texto)
            self._productos_combo[texto] = producto.codigo

        self.combo_producto["values"] = valores_productos

        if self.usuario_venta_var.get() not in self._usuarios_combo:
            self.usuario_venta_var.set("")

        if self.producto_venta_var.get() not in self._productos_combo:
            self.producto_venta_var.set("")

    def _actualizar_ventas(self) -> None:
        """Actualiza la tabla de ventas."""
        for elemento in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(elemento)

        ventas = self.restaurante_servicio.listar_ventas()

        for venta in ventas:
            nombre_usuario = (
                self.restaurante_servicio.obtener_nombre_usuario(
                    venta.usuario_id
                )
            )

            nombre_producto = (
                self.restaurante_servicio.obtener_nombre_producto(
                    venta.producto_codigo
                )
            )

            self.tabla_ventas.insert(
                "",
                "end",
                values=(
                    venta.fecha,
                    f"{nombre_usuario} ({venta.usuario_id})",
                    f"{nombre_producto} ({venta.producto_codigo})",
                    venta.cantidad
                )
            )

    # ==========================================================
    # ACTUALIZACIÓN GENERAL
    # ==========================================================

    def _actualizar_todo(self) -> None:
        """Actualiza la información visual del sistema."""
        self._actualizar_productos()
        self._actualizar_usuarios()
        self._actualizar_combobox_ventas()
        self._actualizar_ventas()

    # ==========================================================
    # SESIÓN
    # ==========================================================

    def _cerrar_sesion(self) -> None:
        """Solicita confirmación antes de cerrar la sesión."""
        confirmar = messagebox.askyesno(
            "Cerrar sesión",
            "¿Desea cerrar la sesión actual?"
        )

        if confirmar:
            self.on_logout()