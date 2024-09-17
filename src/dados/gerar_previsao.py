import pandas as pd
import numpy as np
from src.leitura_e_escrita.ler_arquivo import carrega_csv



def gerar_df_prev_media_movel(df_dados_, n):

    df_dados = df_dados_.drop(labels= ["Colmeia", "Piquet"], axis=1)
    df_dados.loc[max(df_dados.index)+1, :] = None
    df_dados.iloc[-1, 0] = df_dados.iloc[-2, 0]+1

    # Média móvel simples com N = n
    df_dados["Previsão"] = df_dados["Maxim"].rolling(n).mean().shift(1)
    df_dados["Erro"] = df_dados["Maxim"].sub(df_dados["Previsão"])
    df_dados["Erro ABS"] = df_dados["Erro"].abs()
    df_dados["MAPE"] = df_dados["Erro ABS"].div(df_dados["Previsão"])
    #df_dados.set_index("Periodo", inplace=True)

    # Erro Acumulado
    erro_acumulado = round(df_dados["Erro"].sum(skipna=True), 3)
    # MAD
    mad = round(df_dados["Erro ABS"].mean(skipna=True), 3)
    # MAPE
    mape = round(df_dados["MAPE"].sum(skipna=True)/(df_dados["Previsão"].count() - 1), 3)

    lista_nome_colunas = list(df_dados.columns.values)
    dici_resultados = {"Erro Acumulado": erro_acumulado,
                       "MAD": mad,
                       "MAPE": mape,
                       "Lista_Colunas": lista_nome_colunas}



    ## DEBUG
    # print(n)
    # print(caminho)
    # print(df_dados)
    # print(erro_acumulado, mad, mape)

    return dici_resultados, df_dados

def gerar_df_prev_expo_movel(df_, alfa):

    df = df_.drop(labels= ["Colmeia", "Piquet"], axis=1)
    df.loc[max(df.index)+1, :] = None
    df.iloc[-1, 0] = df.iloc[-2, 0]+1

    df["Previsão"] = np.nan
    df["Erro"] = np.nan
    #df["Erro"] = df["Maxim"].sub(df["Previsão"])
    df.at[1, "Previsão"] = (alfa*(df.at[1, "Maxim"] - df.at[0, "Maxim"])) + df.at[0, "Maxim"]

    #print(df.loc[1:]["Previsão"])

    for row in range(len(df.index)):
        row = row+1
        # print(row)

        df.loc[row, "Erro"] = df.loc[row, "Maxim"] - df.loc[row, "Previsão"] 
        df.loc[row+1, "Previsão"] = df.loc[row, "Previsão"] + df.loc[row, "Erro"]*alfa
        print("ERRO =   ", df.loc[row, "Previsão"] - df.loc[row, "Maxim"])
        print("PREVISÃO =   ", df.loc[row, "Previsão"] + df.loc[row, "Erro"]*alfa)

    df["Erro ABS"] = df["Erro"].abs()
    df["MAPE"] = df["Erro ABS"].div(df["Previsão"])

    mad = round(df["Erro ABS"].mean(skipna=True), 3)

    # Erro Acumulado
    erro_acumulado = round(df["Erro"].sum(skipna=True), 3)
    # MAD
    mad = round(df["Erro ABS"].mean(skipna=True), 3)
    # MAPE
    mape = round(df["MAPE"].sum(skipna=True)/(df["Previsão"].count() - 1), 3)
    lista_nome_colunas = list(df.columns.values)
    dici_resultados = {"Erro Acumulado": erro_acumulado,
                       "MAD": mad,
                       "MAPE": mape,
                       "Lista_Colunas": lista_nome_colunas}

    df = df.drop(df.tail(2).index)
    return dici_resultados, df
