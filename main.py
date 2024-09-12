import tkinter
import tkinter.messagebox
import tkinter.ttk
import customtkinter
from src.gui import main_window
from src.database import db_utils

# Periodo   Maxim  Previsão    Erro  Erro ABS   MAPE

# Config Inicial
# Aparencia
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

# Database
db = db_utils.DatabaseManagement("teste.db")
db.abrir_conn()

#region  #### TESTE ####
from src.leitura_e_escrita import ler_arquivo

query1 = """
CREATE TABLE IF NOT EXISTS dados_input (
    periodo int PRIMARY KEY,
    colmeia float NOT NULL,
    piquet float NOT NULL,
    maxim float NOT NULL
);
"""
query2 = """
CREATE TABLE IF NOT EXISTS resultados_maxim (
    periodo int PRIMARY KEY,
    demanda_real float NOT NULL,
    previsao_media_movel float,
    erro float,
    erro_abs float,
    mape_previsao float
);
"""
db.criar_tabela(query1)
db.criar_tabela(query2)

dados_csv = ler_arquivo.carrega_csv("dados_csv.csv")
for row in dados_csv.itertuples():
    db.inserir_data(
        """
        INSERT INTO dados_input (periodo, colmeia, piquet, maxim)
        VALUES (?,?,?,?)
        """,
        (row.Periodo,
        row.Colmeia,
        row.Piquet,
        row.Maxim)
    )


dados = db.query_data("SELECT * FROM dados_input")

# for row in dados:
#     print(row)
#print(dados)

#endregion #### FIM TESTE ####

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