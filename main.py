import tkinter
import tkinter.messagebox
import tkinter.ttk
import customtkinter
from src.gui import main_window
from src.database.db_utils import setup_db
import sys
import os
from src.leitura_e_escrita import ler_arquivo

# Config Inicial

    # Para funcionar com o banco de dados no executável
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


path_db = resource_path("db/teste.db")

# Aparencia
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")


# SETUP Database
db = setup_db(path_db)


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