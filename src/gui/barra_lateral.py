import customtkinter
import tkinter
from src.dados import gerar_previsao

class BarraLateral(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master
        self.configure(width=140, corner_radius = 0)

        ## Sidebar - Esquerda
        self.grid(row=0, column=0, rowspan=3, sticky="nsew")
        self.grid_rowconfigure(4, weight=1)

        # Texto titulo
        self.logo_label = customtkinter.CTkLabel(self, text="Opções", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Botoes
        self.sidebar_botao_imp_dados = customtkinter.CTkButton(self, text="Carregar Dados", command=self.botao_carregar_dados)
        self.sidebar_botao_imp_dados.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_gerar = customtkinter.CTkButton(self, text="Gerar", command=self.get_gerar_resultado)
        self.sidebar_gerar.grid(row=3, column=0, padx=20, pady=20)

        # Seletor N
        self.n_botoes_frame = customtkinter.CTkFrame(self)
        self.n_botoes_frame.grid(row=2, column=0 , padx=(20, 20), pady=(10, 0), sticky="nsew")
        self.n_botoes_titulo = customtkinter.CTkLabel(master=self.n_botoes_frame, text="Selecione o N")
        self.n_botoes_titulo.grid(row=0, column=0, sticky="")

        self.n_valor = tkinter.IntVar(value=4)
        self.n_botao_1 = customtkinter.CTkRadioButton(master=self.n_botoes_frame, variable=self.n_valor, text="N=2",value=2)
        self.n_botao_1.grid(row=1, column=0, pady=10, padx=10, sticky="n")
        self.n_botao_2 = customtkinter.CTkRadioButton(master=self.n_botoes_frame, variable=self.n_valor, text="N=3",value=3)
        self.n_botao_2.grid(row=2, column=0, pady=10, padx=10, sticky="n")
        self.n_botao_3 = customtkinter.CTkRadioButton(master=self.n_botoes_frame, variable=self.n_valor, text="N=4",value=4)
        self.n_botao_3.grid(row=3, column=0, pady=10, padx=10, sticky="n")

    def botao_carregar_dados(self):
        self.master.path_dados = customtkinter.filedialog.askopenfilename()
    def get_gerar_resultado(self):
        self.master.dici, self.master.df = gerar_previsao.gerar_df(self.master.path_dados, self.n_valor.get())
        self.master.set_resultados()