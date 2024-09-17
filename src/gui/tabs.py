import customtkinter


class Tabview(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.master = master

        # Tabview Configuração
        self.configure(width=250)
        self.grid(row=0, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")
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


    def set_graficos(self, grafico):
        pass

    def set_labels(self, dici):
        valor_erro_acumulado = dici["Erro Acumulado"]
        valor_mad = dici["MAD"]
        valor_mape = dici["MAPE"]
        self.label_mad.configure(text = f"MAD = {valor_mad}")
        self.label_erro_acumulado.configure(text = f"Erro Acumulado = {valor_erro_acumulado}")
        self.label_mape.configure(text = f"MAPE = {valor_mape}")
