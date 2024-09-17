import tkinter
import pandas as pd

# Para o gráfico
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler


class Grafico():
    def __init__(self, master, fig):


        # Renderizar Gráfico
        self.canvas = FigureCanvasTkAgg(fig, master=master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        # Menu matplot
        self.toolbar = NavigationToolbar2Tk(self.canvas, master)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    def update_grafico(self, master, fig):
        self.canvas.get_tk_widget().destroy()
        self.toolbar.destroy()

        self.canvas = FigureCanvasTkAgg(fig, master=master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        # Menu matplot
        self.toolbar = NavigationToolbar2Tk(self.canvas, master)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)



def gerar_fig_demanda(df):

    fig, ax = plt.subplots(clear = True)

    ax.plot(df["Periodo"], df["Maxim"], label= "Demanda Real", marker="o")
    ax.plot(df["Periodo"], df["Previsão"], label="Demanda Prevista", marker="x")

    ax.set_title("Demanda Real vs. Demanda Prevista")
    ax.set_xlabel("Período")
    ax.set_ylabel("Demanda")
    ax.legend()

    return fig


def gerar_fig_erro(df, dici):

    # Limite supf e inf 4xMAD
    limite_sup = pd.Series(data=[4*dici["MAD"]] * (df["Periodo"].count())) # +1
    limite_inf = pd.Series(data=[-4*dici["MAD"]] * (df["Periodo"].count())) # +1

    fig, ax = plt.subplots(clear = True)

    ax.plot(df["Periodo"], df["Erro"], label= "Erro", marker="o")

    ax.plot(df["Periodo"], limite_sup, label="Limite Superior", color="red", linestyle="--")
    ax.plot(df["Periodo"], limite_inf, label="Limite Inferior", color="green", linestyle="--")

    ax.set_title("Demanda Real vs. Demanda Prevista")
    ax.set_xlabel("Período")
    ax.set_ylabel("Erro")
    ax.legend()

    return fig