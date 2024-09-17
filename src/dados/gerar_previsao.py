import pandas as pd
from src.leitura_e_escrita.ler_arquivo import carrega_csv

def gerar_df(caminho, n):

    df_dados = carrega_csv(caminho)
    df_dados.drop(labels= ["Colmeia", "Piquet"], axis=1, inplace=True)
    df_dados.loc[max(df_dados.index)+1, :] = None
    df_dados.iloc[-1, 0] = df_dados.iloc[-2, 0]+1

    # Média móvel simples com N = n
    df_dados["Previsão"] = df_dados["Maxim"].rolling(n).mean().shift(1)
    df_dados["Erro"] = df_dados["Maxim"].sub(df_dados["Previsão"])
    df_dados["Erro ABS"] = df_dados["Erro"].abs()
    df_dados["MAPE"] = round(df_dados["Erro ABS"].div(df_dados["Previsão"]), 3)
    #df_dados.set_index("Periodo", inplace=True)

    # Erro Acumulado
    erro_acumulado = df_dados["Erro"].sum(skipna=True)
    # MAD
    mad = df_dados["Erro ABS"].mean(skipna=True)
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
