import tkinter.ttk
import tkinter
import tkinter.messagebox



class TabelaFrame(tkinter.ttk.Treeview):
    def __init__(self, master):
        super().__init__(master)

        self.master = master
        self.grid(column=0, row=0, padx=20, sticky="nsew")


    def set_tabela(self, df, dici):

        # Setar nome das colunas com base no df
        self.configure(columns = dici["Lista_Colunas"], show= "headings")
        self.column("#0", stretch=False)

        # Criando as colunas
        for column in df.columns:
            self.heading(
                column,
                text=column
            )

        df = df.fillna('') # Para a visualização apenas
        # Inserir os dados
        for i in self.get_children():
            self.delete(i)

        for index, row in df.iterrows():
            self.insert('', 'end', index)

            for column in row.index:
                self.set(index, column, row[column])