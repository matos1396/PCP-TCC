import customtkinter
from src.gui.tab_mms import Tab_mms
from src.gui.tab_mme import Tab_mme

class Tabview(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.master = master

        # Tabview Configuração
        self.configure(width=250)
        self.grid(row=0, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.add("MAXIM Média Móvel Simples")
        self.add("MAXIM Média Móvel Exponencial")

        # Configucação abas inicial
        self.tab("MAXIM Média Móvel Simples").grid_columnconfigure(0, weight=1)
        self.tab("MAXIM Média Móvel Exponencial").grid_columnconfigure(0, weight=1)

        # Adicionar as abas
        self.tab_mms = Tab_mms(master = self.tab("MAXIM Média Móvel Simples"))
        self.tab_mme = Tab_mme(master = self.tab("MAXIM Média Móvel Exponencial"))


