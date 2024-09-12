import sqlite3
from pathlib import Path

class DatabaseManagement():
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.db_path = Path("db/" + db_name)
        print(self.db_path)

    def abrir_conn(self):
        self.conn = sqlite3.connect(self.db_path)
        print(f"Conexão aberta com {self.db_name}")

    def fechar_conn(self):
        if self.conn:
            self.conn.close()
            print("Conexão fechada")

    def criar_tabela(self, create_table_sql):
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
            print("Tabela criada com sucesso")
        except sqlite3.Error as e:
            print(f"Erro ao criar tabela: {e}")

    def inserir_data(self, insert_sql, data, nome_tabela = None):
        try:
            if self.check_if_exists(data[0], nome_tabela) == False:
                c = self.conn.cursor()
                c.execute(insert_sql, data)
                self.conn.commit()
                print("Dados inseridos com sucesso")
                print(data)
            else:
                print("Dados já foram inseridos")
        except sqlite3.Error as e:
            print(f"Erro ao inserir dados: {e}")

    def query_data(self, query):
        try:
            c = self.conn.cursor()
            c.execute(query)
            results = c.fetchall()
            print("Dados consultados com sucesso")
            return results
        except sqlite3.Error as e:
            print(f"Erro na consulta: {e}")
            return None

    def delete_data(self, delete_sql):
        try:
            c = self.conn.cursor()
            c.execute(delete_sql)
            self.conn.commit()
            print("Dados deletados com sucesso")
        except sqlite3.Error as e:
            print(f"Erro ao deletar dados: {e}")

    def check_if_exists(self, periodo, nome_tabela):
        if nome_tabela == None:
            return False
        if self.query_data(f"SELECT {periodo} FROM {nome_tabela}") != None:
            # print(periodo)
            # print(nome_tabela)
            return True
        else:
            return False