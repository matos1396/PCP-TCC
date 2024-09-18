import tkinter.messagebox
import customtkinter
import tkinter
from src.dados import gerar_previsao
from src.leitura_e_escrita.ler_arquivo import carrega_csv

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
        self.sidebar_gerar.grid(row=4, column=0, padx=20, pady=20)

        # Seletor N
        self.n_botoes_frame = customtkinter.CTkFrame(self)
        self.n_botoes_frame.grid(row=2, column=0 , padx=(20, 20), pady=(10, 0), sticky="nsew")
        self.n_botoes_titulo = customtkinter.CTkLabel(master=self.n_botoes_frame, text="Número de Períodos N:")
        self.n_botoes_titulo.grid(row=0, column=0, sticky="")

        self.n_valor = tkinter.IntVar(value=4)
        self.n_botao_1 = customtkinter.CTkRadioButton(master=self.n_botoes_frame, variable=self.n_valor, text="N=2",value=2)
        self.n_botao_1.grid(row=1, column=0, pady=10, padx=10, sticky="n")
        self.n_botao_2 = customtkinter.CTkRadioButton(master=self.n_botoes_frame, variable=self.n_valor, text="N=3",value=3)
        self.n_botao_2.grid(row=2, column=0, pady=10, padx=10, sticky="n")
        self.n_botao_3 = customtkinter.CTkRadioButton(master=self.n_botoes_frame, variable=self.n_valor, text="N=4",value=4)
        self.n_botao_3.grid(row=3, column=0, pady=10, padx=10, sticky="n")

        # Alfa input
        self.alfa_frame = customtkinter.CTkFrame(self)
        self.alfa_frame.grid(row=3, column=0 , padx=(20, 20), pady=(10, 0), sticky="nsew")
        self.alfa_titulo = customtkinter.CTkLabel(master=self.alfa_frame, text="Valor do alfa:")
        self.alfa_titulo.grid(row=0, column=0)

        self.alfa = tkinter.StringVar(value = "0.5")
        self.alfa_entry = customtkinter.CTkEntry(self.alfa_frame, textvariable=self.alfa)
        self.alfa_entry.grid(row=1, column=0 , padx=(20, 20), pady=(10, 10), sticky="nsew")


    def botao_carregar_dados(self):
        self.master.path_dados = customtkinter.filedialog.askopenfilename()
        df_input = carrega_csv(self.master.path_dados)
        self.master.db.insert_input(df_input)

    def get_gerar_resultado(self):

        if self.master.path_dados == None:
            tkinter.messagebox.showerror("Erro", "Carregue os dados antes de continuar")
            return

        self.alfa_float = float(self.alfa.get())
        df_input = carrega_csv(self.master.path_dados)
        dici_1, df_1 = gerar_previsao.gerar_df_prev_media_movel(df_input, self.n_valor.get())
        dici_2, df_2 = gerar_previsao.gerar_df_prev_expo_movel(df_input, alfa = self.alfa_float) #TODO: adicionar input pro alfa

        self.master.dici = {"dici_media_movel": dici_1,
                            "dici_expo_movel": dici_2}
        if len(self.master.df_lista) != 0:
            self.master.df_lista.clear()
            self.master.df_lista.extend([df_1, df_2])
        else:
            self.master.df_lista.extend([df_1, df_2])
        self.master.set_resultados()