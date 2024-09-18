import customtkinter
from src.gui import barra_lateral, tabela, tabs, graficos
from src.database import db_utils

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
        self.geometry(f"{1300}x{800}")

        # Configuração do grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Barra Lateral
        self.barra_lateral = barra_lateral.BarraLateral(self)

        # Tabview
        self.tabview = tabs.Tabview(self)

        # Tabela - Instanciando Limpa
        self.tabela_mms = tabela.TabelaFrame(self.tabview.tab_mms.tab("Resultados - Valores"))
        self.tabela_mme = tabela.TabelaFrame(self.tabview.tab_mme.tab("Resultados - Valores"))


        # Barras de Scroll tabelas
        self.barra_scroll1 = customtkinter.CTkScrollbar(self.tabview.tab_mms.tab("Resultados - Valores"), command=self.tabela_mms.yview)
        self.barra_scroll1.grid(row=0, column=1, sticky="ns")
        self.tabela_mms.configure(yscrollcommand=self.barra_scroll1.set)
        self.barra_scroll2 = customtkinter.CTkScrollbar(self.tabview.tab_mme.tab("Resultados - Valores"), command=self.tabela_mme.yview)
        self.barra_scroll2.grid(row=0, column=1, sticky="ns")
        self.tabela_mme.configure(yscrollcommand=self.barra_scroll2.set)


    def set_resultados(self):
        # Setup Tabelas
        self.tabela_mms.set_tabela_media_simples(self.df_lista[0], self.dici["dici_media_movel"])
        self.tabela_mme.set_tabela_media_simples(self.df_lista[1], self.dici["dici_expo_movel"])
        self.tabview.tab_mms.set_df(df = self.df_lista[0])
        self.tabview.tab_mme.set_df(df = self.df_lista[1])
        self.tabview.tab_mms.set_labels(self.dici["dici_media_movel"])
        self.tabview.tab_mme.set_labels(self.dici["dici_expo_movel"])

        # Salvando resultados no banco de dados
        dados_para_db_1 = db_utils.preparar_dados_para_insercao(self.df_lista[0])
        dados_para_db_2 = db_utils.preparar_dados_para_insercao(self.df_lista[1])
        self.db.inserir_dados_resultados(tabela = "resultados_maxim_MMS", dados = dados_para_db_1)
        self.db.inserir_dados_resultados(tabela = "resultados_maxim_MME", dados = dados_para_db_2)


        # Para os graficos
        figura = graficos.gerar_fig_demanda(self.df_lista[0])
        figura2 = graficos.gerar_fig_erro(self.df_lista[0], self.dici["dici_media_movel"])
        figura3 = graficos.gerar_fig_demanda(self.df_lista[1])
        figura4 = graficos.gerar_fig_erro(self.df_lista[1], self.dici["dici_expo_movel"])

        if self.grafico == None:
            self.grafico = graficos.Grafico(self.tabview.tab_mms.tab("Gráfico Demanda Real x Prevista"), figura)
            self.grafico2 = graficos.Grafico(self.tabview.tab_mms.tab("Gráfico Erro"), figura2)
            self.grafico3 = graficos.Grafico(self.tabview.tab_mme.tab("Gráfico Demanda Real x Prevista"), figura3)
            self.grafico4 = graficos.Grafico(self.tabview.tab_mme.tab("Gráfico Erro"), figura4)

        else:
            self.grafico.update_grafico(self.tabview.tab_mms.tab("Gráfico Demanda Real x Prevista"), figura)
            self.grafico2.update_grafico(self.tabview.tab_mms.tab("Gráfico Erro"), figura2)
            self.grafico3.update_grafico(self.tabview.tab_mme.tab("Gráfico Demanda Real x Prevista"), figura3)
            self.grafico4.update_grafico(self.tabview.tab_mme.tab("Gráfico Erro"), figura4)



