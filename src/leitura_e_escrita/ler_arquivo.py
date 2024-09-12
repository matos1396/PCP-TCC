import pandas as pd


def carrega_excel(caminho):
    dataframe = pd.read_excel(caminho)
    return dataframe


# TODO: Arrumar para ler de forma universal separador numérico "," e "."
def carrega_csv(caminho):
    dataframe = pd.read_csv(caminho, sep=";", header=0, dtype={
    "Periodo": "int64",
    "Colmeia": "float64",
    "Piquet": "float64",
    "Maxim": "float64",})
    return dataframe
