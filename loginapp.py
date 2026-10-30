from datetime import datetime
import hashlib
import sqlite3
from tkinter import *
from tkinter import messagebox, ttk


# ==========================================
# 1. EXCEPCIONES PERSONALIZADAS
# ==========================================
class MenorEdadException(Exception):
  """Excepción lanzada si el usuario es menor de edad."""

  pass


class UsuarioBloqueadoException(Exception):
  """Excepción lanzada si el usuario está bloqueado."""

  pass


# ==========================================
# 2. CONFIGURACIÓN Y RELLENO DE LA BASE DE DATOS
# ==========================================
DB_FILE = "db_user.db"


def inicializar_db():
  conn = sqlite3.connect(DB_FILE)
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            codigo INTEGER PRIMARY KEY AUTOINCREMENT,
            nickname TEXT UNIQUE,
            birthday TEXT,
            passw TEXT,
            blocked INTEGER
        )
    """)

  # Rellenar con los usuarios de prueba si la tabla está vacía
  cursor.execute("SELECT COUNT(*) FROM users")
  if cursor.fetchone()[0] == 0:
    p_pepe = hashlib.md5("pepepassw".encode()).hexdigest()
    p_sara = hashlib.md5("sarapassw".encode()).hexdigest()
    p_mario = hashlib.md5("mariopassw".encode()).hexdigest()
    p_lola = hashlib.md5("lolapassw".encode()).hexdigest()
    p_jorge = hashlib.md5("jorgepassw".encode()).hexdigest()
    p_aleja = hashlib.md5("alejopassw".encode()).hexdigest()

    usuarios_iniciales = [
        ("pepeuser", "2020-11-15", p_pepe, 0),  # Menor de edad
        ("sarauser", "2000-11-15", p_sara, 0),  # Activa / Mayor de edad
        ("mariouser", "2010-11-15", p_mario, 0),  # Menor de edad
        ("lolauser", "2005-11-15", p_lola, 0),  # Activa / Mayor de edad
        ("jorgeuser", "2000-11-15", p_jorge, 1),  # BLOQUEADO (blocked = 1)
        ("alejauser", "2015-11-15", p_aleja, 1),  # BLOQUEADO (blocked = 1)
    ]

    cursor.executemany(
        """
            INSERT OR IGNORE INTO users (nickname, birthday, passw, blocked) 
            VALUES (?, ?, ?, ?)
        """,
        usuarios_iniciales,
    )

  conn.commit()
  conn.close()


# ==========================================
# 3. INTERFAZ GRÁFICA (TKINTER)
# ==========================================
class AppLogin:

  def __init__(self, window):
    self.window = window
    self.window.title("Ventana de Acceso")
    self.window.geometry("400x400")
    self.window.resizable(0, 0)

    inicializar_db()

    # Encabezado
    Label(
        window, text="INICIAR SESIÓN", font=("Comic Sans MS", 16, "bold")
    ).pack(pady=20)

    # Formulario
    frame_form = LabelFrame(window, text=" Credenciales ", font=("Comic Sans", 11))
    frame_form.pack(padx=20, pady=10, fill="both")

    Label(frame_form, text="Usuario:", font=("Comic Sans", 11)).grid(
        row=0, column=0, padx=10, pady=10, sticky="e"
    )
    self.user_input = Entry(frame_form, width=20, font=("Comic Sans", 11))
    self.user_input.grid(row=0, column=1, padx=10, pady=10)
    self.user_input.focus()

    Label(frame_form, text="Contraseña:", font=("Comic Sans", 11)).grid(
        row=1, column=0, padx=10, pady=10, sticky="e"
    )
    self.pass_input = Entry(
        frame_form, width=20, font=("Comic Sans", 11), show="*"
    )
    self.pass_input.grid(row=1, column=1, padx=10, pady=10)

    # Mostrar contraseña
    self.ver_pass = IntVar()
    Checkbutton(
        frame_form,
        text="Mostrar contraseña",
        variable=self.ver_pass,
        command=self.toggle_password,
        font=("Comic Sans", 9),
    ).grid(row=2, column=1, sticky="w", padx=10)

    # Botones
    frame_btns = Frame(window)
    frame_btns.pack(pady=20)

    Button(
        frame_btns,
        text="Acceder",
        command=self.login_user,
        bg="black",
        fg="white",
        width=10,
        font=("Comic Sans", 11),
    ).grid(row=0, column=0, padx=10)
    Button(
        frame_btns,
        text="Registrarse",
        command=self.abrir_registro,
        bg="#333333",
        fg="white",
        width=10,
        font=("Comic Sans", 11),
    ).grid(row=0, column=1, padx=10)

  def toggle_password(self):
    if self.ver_pass.get() == 1:
      self.pass_input.config(show="")
    else:
      self.pass_input.config(show="*")

  def login_user(self):
    usuario = self.user_input.get().strip()
    password = self.pass_input.get().strip()

    if not usuario or not password:
      messagebox.showwarning(
          "Campos vacíos", "Por favor, introduce usuario y contraseña."
      )
      return

    # Hashear contraseña con hashlib
    pass_hash = hashlib.md5(password.encode()).hexdigest()

    try:
      conn = sqlite3.connect(DB_FILE)
      cursor = conn.cursor()
      cursor.execute(
          "SELECT nickname, birthday, blocked FROM users WHERE nickname=? AND"
          " passw=?",
          (usuario, pass_hash),
      )
      user_data = cursor.fetchone()
      conn.close()

      if user_data:
        nickname, birthday_str, blocked = user_data
        # ¡Login correcto! Pasamos directamente a abrir la ventana/contenido
        messagebox.showinfo("Éxito", f"Login correcto. Bienvenido, {nickname}")
        self.abrir_ventana_principal(nickname, birthday_str, blocked)
      else:
        messagebox.showerror(
            "Error", "Usuario o contraseña incorrectos."
        )

    except Exception as e:
      messagebox.showerror("Error", f"Error en la base de datos: {e}")

  def abrir_ventana_principal(self, nickname, birthday_str, blocked):
    """Ventana de contenido. Aquí es donde se evalúan las excepciones al acceder."""
    self.window.destroy()
    main_win = Tk()
    main_win.title("Panel Principal - Contenido")
    main_win.geometry("450x300")
    main_win.resizable(0, 0)

    try:
      # 1. Comprobar si está bloqueado (Lanza excepción personalizada)
      if blocked == 1:
        raise UsuarioBloqueadoException(
            "Acceso no permitido al contenido: Su cuenta se encuentra"
            " bloqueada."
        )

      # 2. Comprobar si es menor de edad (Lanza excepción personalizada)
      f_nacimiento = datetime.strptime(birthday_str, "%Y-%m-%d")
      hoy = datetime.now()
      edad = (
          hoy.year
          - f_nacimiento.year
          - ((hoy.month, hoy.day) < (f_nacimiento.month, f_nacimiento.day))
      )

      if edad < 18:
        raise MenorEdadException(
            f"Acceso restringido al contenido: Es menor de edad ({edad} años)."
        )

      # ==========================================
      # SI PASA TODO: Contenido exclusivo para mayores activos
      # ==========================================
      Label(
          main_win,
          text=f"¡Bienvenido al sistema, {nickname}!",
          font=("Comic Sans", 15, "bold"),
      ).pack(pady=30)
      Label(
          main_win,
          text="Has accedido correctamente al contenido de la aplicación.",
          font=("Comic Sans", 11),
      ).pack(pady=10)

      Button(
          main_win,
          text="Cerrar Sesión",
          command=main_win.destroy,
          bg="red",
          fg="white",
          font=("Comic Sans", 10),
      ).pack(pady=20)

    except UsuarioBloqueadoException as e:
      messagebox.showerror("Acceso Denegado", str(e))
      main_win.destroy()  # Cierra la ventana de contenido al saltar la excepción
    except MenorEdadException as e:
      messagebox.showwarning("Restricción de Edad", str(e))
      main_win.destroy()  # Cierra la ventana de contenido al saltar la excepción

    main_win.mainloop()

  def abrir_registro(self):
    """Ventana de registro de nuevo usuario"""
    ven_reg = Toplevel(self.window)
    ven_reg.title("Registro de Nuevo Usuario")
    ven_reg.geometry("350x380")
    ven_reg.resizable(0, 0)

    Label(
        ven_reg, text="NUEVO USUARIO", font=("Comic Sans MS", 13, "bold")
    ).pack(pady=15)

    Label(ven_reg, text="Nickname (Único):", font=("Comic Sans", 10)).pack()
    reg_user = Entry(ven_reg, width=25, font=("Comic Sans", 10))
    reg_user.pack(pady=5)

    Label(
        ven_reg,
        text="Fecha Nacimiento (YYYY-MM-DD):",
        font=("Comic Sans", 10),
    ).pack()
    reg_bday = Entry(ven_reg, width=25, font=("Comic Sans", 10))
    reg_bday.pack(pady=5)

    Label(ven_reg, text="Contraseña:", font=("Comic Sans", 10)).pack()
    reg_pass = Entry(ven_reg, width=25, font=("Comic Sans", 10), show="*")
    reg_pass.pack(pady=5)

    def guardar_registro():
      u = reg_user.get().strip()
      b = reg_bday.get().strip()
      p = reg_pass.get().strip()

      if not u or not b or not p:
        messagebox.showwarning(
            "Advertencia", "Todos los campos son obligatorios."
        )
        return

      try:
        datetime.strptime(b, "%Y-%m-%d")
      except ValueError:
        messagebox.showerror(
            "Error", "Formato de fecha inválido. Usa YYYY-MM-DD (ej: 2000-05-12)"
        )
        return

      p_hash = hashlib.md5(p.encode()).hexdigest()

      try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (nickname, birthday, passw, blocked) VALUES"
            " (?, ?, ?, ?)",
            (u, b, p_hash, 0),
        )
        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Éxito", "Usuario registrado correctamente. ¡Iniciando sesión!"
        )
        ven_reg.destroy()

        # Autologin tras el registro (entra al contenido evaluando su edad)
        self.abrir_ventana_principal(u, b, 0)

      except sqlite3.IntegrityError:
        messagebox.showerror(
            "Error",
            "El nickname ya existe en la base de datos. Elige otro.",
        )

    Button(
        ven_reg,
        text="Guardar y Registrarse",
        bg="green",
        fg="white",
        font=("ComicSans", 10),
        command=guardar_registro,
    ).pack(pady=15)


if __name__ == "__main__":
  root = Tk()
  app = AppLogin(root)
  root.mainloop()