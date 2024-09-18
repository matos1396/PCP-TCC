import tkinter
import tkinter.messagebox
import tkinter.ttk
import customtkinter
from src.gui import main_window
from src.database.db_utils import setup_db

from src.leitura_e_escrita import ler_arquivo

# Config Inicial
# Aparencia
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

# SETUP Database
db = setup_db()


## Main loop
app = main_window.App(db)

app.protocol("WM_DELETE_WINDOW", app.quit)

# Estilo Tabela
style = tkinter.ttk.Style()

style.theme_use("default")
style.configure("Treeview",
                background="#2a2d2e",
                foreground="white",
                rowheight=25,
                fieldbackground="#343638",
                bordercolor="#343638",
                borderwidth=0)
style.map('Treeview', background=[('selected', '#22559b')])
style.configure("Treeview.Heading",
                background="#565b5e",
                foreground="white",
                relief="flat")
style.map("Treeview.Heading",
          background=[('active', '#3484F0')])


app.mainloop()