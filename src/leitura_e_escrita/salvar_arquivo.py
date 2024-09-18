import pandas as pd
import os
def salvar_excel(df, flag):
    if not os.path.exists("dados_excel.xlsx"):
        writer = pd.ExcelWriter("dados_excel.xlsx", engine="openpyxl", mode="w")
    else:
        writer = pd.ExcelWriter("dados_excel.xlsx", engine="openpyxl", if_sheet_exists="replace", mode="a")

    if flag == "mms":
        df.to_excel(excel_writer = writer, sheet_name = "MAXIM MMS")
    if flag == "mme":
        df.to_excel(excel_writer = writer, sheet_name = "MAXIM MME")
    writer.close()
