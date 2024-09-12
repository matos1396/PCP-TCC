import customtkinter
from src.gui import barra_lateral, tabela, tabs, graficos

# APP
class App(customtkinter.CTk):
    def __init__(self, db):
        super().__init__()

        self.db = db
        self.resultados = None
        self.path_dados = None
        self.dici = None
        self.df = None
        self.grafico = None
        self.grafico2 = None


        # Configuração da janela principal
        self.title("Média Móvel Simples")
        self.geometry(f"{1100}x{580}")

        # Configuração do grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Barra Lateral
        self.barra_lateral = barra_lateral.BarraLateral(self)

        # Tabview
        self.tabview = tabs.Tabview(self)

        # Tabela - Instanciando Limpa
        self.tabela = tabela.TabelaFrame(self.tabview.tab("Resultados - Valores"))

        # Barra
        self.barra_scroll = customtkinter.CTkScrollbar(self.tabview.tab("Resultados - Valores"), command=self.tabela.yview)
        self.barra_scroll.grid(row=0, column=1, sticky="ns")
        self.tabela.configure(yscrollcommand=self.barra_scroll.set)


    def set_resultados(self):
        self.tabela.set_tabela(self.df, self.dici)
        # self.tabela["show"] = "headings"
        # self.tabela.grid(sticky="NSEW")
        self.tabview.set_labels(self.dici)


        for idx, row in self.df.iterrows():
            self.db.inserir_data(
                """
                INSERT INTO resultados_maxim (periodo, demanda_real, previsao_media_movel, erro, erro_abs, mape_previsao)
                VALUES (?,?,?,?,?,?)
                """,
                (row.loc["Periodo"],
                row.loc["Maxim"],
                row.loc["Previsão"],
                row.loc["Erro"],
                row.loc["Erro ABS"],
                row.loc["MAPE"])
            )

        x = self.db.query_data("SELECT * FROM resultados_maxim")

        for row in x:
            print(row)


        figura = graficos.gerar_fig_demanda(self.df)
        figura2 = graficos.gerar_fig_erro(self.df, self.dici)

        if self.grafico == None:
            self.grafico = graficos.Grafico(self.tabview.tab("Gráfico Demanda Real x Prevista"), figura)
            self.grafico2 = graficos.Grafico(self.tabview.tab("Gráfico Erro"), figura2)

        else:
            self.grafico.update_grafico(self.tabview.tab("Gráfico Demanda Real x Prevista"), figura)
            self.grafico2.update_grafico(self.tabview.tab("Gráfico Erro"), figura2)
