import customtkinter
from src.gui import barra_lateral, tabela, tabs, graficos

# APP
class App(customtkinter.CTk):
    def __init__(self, db):
        super().__init__()

        self.db = db
        self.resultados = None
        self.path_dados = None
        self.dici = {}
        self.df_lista = []
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
        self.tabela.set_tabela_media_simples(self.df_lista[0], self.dici["dici_media_movel"])
        self.tabview.set_labels(self.dici["dici_media_movel"])

        for _idx, row in self.df_lista[0].iterrows():
            # print(row)
            self.db.inserir_data(
                """
                INSERT INTO resultados_maxim_MMS (periodo, demanda_real, previsao_media_movel, erro, erro_abs, mape_previsao)
                VALUES (?,?,?,?,?,?)
                """,
                (row.loc["Periodo"],
                row.loc["Maxim"],
                row.loc["Previsão"],
                row.loc["Erro"],
                row.loc["Erro ABS"],
                row.loc["MAPE"]),
                "resultados_maxim_MMS"
            )


        for _idx, row in self.df_lista[1].iterrows():
            # print(row)
            self.db.inserir_data(
                """
                INSERT INTO resultados_maxim_MME (periodo, demanda_real, previsao_media_movel, erro, erro_abs, mape_previsao)
                VALUES (?,?,?,?,?,?)
                """,
                (row.loc["Periodo"],
                row.loc["Maxim"],
                row.loc["Previsão"],
                row.loc["Erro"],
                row.loc["Erro ABS"],
                row.loc["MAPE"]),
                "resultados_maxim_MME"
            )


        figura = graficos.gerar_fig_demanda(self.df_lista[0])
        figura2 = graficos.gerar_fig_erro(self.df_lista[0], self.dici["dici_media_movel"])
        figura3 = graficos.gerar_fig_demanda(self.df_lista[1])
        figura4 = graficos.gerar_fig_erro(self.df_lista[1], self.dici["dici_expo_movel"])

        if self.grafico == None:
            self.grafico = graficos.Grafico(self.tabview.tab("Gráfico Demanda Real x Prevista"), figura)
            self.grafico2 = graficos.Grafico(self.tabview.tab("Gráfico Erro"), figura2)
            self.grafico3 = graficos.Grafico(self.tabview.tab("Gráfico Demanda Real x Prevista - MME"), figura3)
            self.grafico4 = graficos.Grafico(self.tabview.tab("Gráfico Erro - MME"), figura4)

        else:
            self.grafico.update_grafico(self.tabview.tab("Gráfico Demanda Real x Prevista"), figura)
            self.grafico2.update_grafico(self.tabview.tab("Gráfico Erro"), figura2)
            self.grafico3.update_grafico(self.tabview.tab("Gráfico Demanda Real x Prevista - MME"), figura3)
            self.grafico4.update_grafico(self.tabview.tab("Gráfico Erro - MME"), figura4)
