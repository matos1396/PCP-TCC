import customtkinter
from src.leitura_e_escrita.salvar_arquivo import salvar_excel

class Tab_mms(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.df = None

        # Tabview Configuração
        self.grid(row=0, column=0, padx=(20, 20), pady=(0, 0), sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.add("Gráfico Demanda Real x Prevista")
        self.add("Gráfico Erro")
        self.add("Resultados - Valores")

        self.tab("Gráfico Demanda Real x Prevista").grid_columnconfigure(0, weight=1)
        self.tab("Gráfico Erro").grid_columnconfigure(0, weight=1)
        self.tab("Resultados - Valores").grid_columnconfigure(0, weight=1)

        # Label resultados
        self.frame_resultados = customtkinter.CTkFrame(master=self.tab("Resultados - Valores"), corner_radius=0)
        self.frame_resultados.grid(row=1, column=0)
        self.label_mad = customtkinter.CTkLabel(master = self.frame_resultados, text = "MAD = ")
        self.label_mape = customtkinter.CTkLabel(master = self.frame_resultados, text = "MAPE = ")
        self.label_erro_acumulado = customtkinter.CTkLabel(master = self.frame_resultados, text = "Erro Acumulado = ")
        self.label_mad.grid(row=1, column=0, stick= "NSEW")
        self.label_mape.grid(row=2, column=0, stick= "NSEW")
        self.label_erro_acumulado.grid(row=3, column=0, stick= "NSEW")

        # Botão Salvar
        self.salvar_dados = customtkinter.CTkButton(self.tab("Resultados - Valores"), text="Exportar Dados", command=self.exportar_dados)
        self.salvar_dados.grid(row=3, column=0, stick = "SE")

    def set_df(self, df):
        self.df = df
    def get_df(self):
        return self.df

    def exportar_dados(self):
        salvar_excel(self.df, "mms")
        print("DADOS SALVOS")


    def set_labels(self, dici):
        valor_erro_acumulado = dici["Erro Acumulado"]
        valor_mad = dici["MAD"]
        valor_mape = dici["MAPE"]
        self.label_mad.configure(text = f"MAD = {valor_mad}")
        self.label_erro_acumulado.configure(text = f"Erro Acumulado = {valor_erro_acumulado}")
        self.label_mape.configure(text = f"MAPE = {valor_mape}")