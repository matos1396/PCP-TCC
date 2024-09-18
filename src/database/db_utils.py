import os
import sqlite3
from pathlib import Path

class DatabaseManagement():
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.db_path = Path(db_name)
        print(self.db_path)
        self.nome_colunas = {"resultados_maxim_MME": ["periodo", "demanda_real", "previsao_media_movel", "erro", "erro_abs", "mape_previsao"],
                             "resultados_maxim_MMS": ["periodo", "demanda_real", "previsao_media_movel", "erro", "erro_abs", "mape_previsao"]}

    def check_db_existe(self):
        db_path = os.path.exists(self.db_path)
        if db_path:
            print(f"O banco de dados '{self.db_path}' já existe.")
        else:
            print(f"O banco de dados '{self.db_path}' não existe.")
        return db_path

    def abrir_conn(self):
        if not self.check_db_existe():
            print("Criando novo banco de dados...")
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
            # if self.check_if_exists(data[0], nome_tabela) == False:
            c = self.conn.cursor()
            c.execute(insert_sql, data)
            self.conn.commit()
            print("Dados inseridos com sucesso")
            print(data)

            #    print("Dados já foram inseridos")
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

    # def check_if_exists(self, periodo, nome_tabela):
    #     if nome_tabela == None:
    #         return False
    #     if self.query_data(f"SELECT {periodo} FROM {nome_tabela}") != None:
    #         # print(periodo)
    #         # print(nome_tabela)
    #         return True
    #     else:
    #         return False


    def insert_input(self, dados_input):
        print("#### INSERINDO DADOS INPUT NA TABELA dados_input ####")
        for row in dados_input.itertuples():
            self.inserir_data(
                """
                INSERT OR IGNORE INTO dados_input (periodo, colmeia, piquet, maxim)
                VALUES (?,?,?,?)
                """,
                (row.Periodo,
                row.Colmeia,
                row.Piquet,
                row.Maxim)
            )

    def inserir_dados_resultados(self, tabela, dados):
        """
        Insere dados em uma tabela específica no banco de dados.

        Args:
        tabela (str): O nome da tabela onde os dados serão inseridos.
        dados (list of tuples): Uma lista de tuplas com os valores correspondentes às colunas.
        """

        if tabela == "resultados_maxim_MMS":
            colunas_str = ', '.join(self.nome_colunas["resultados_maxim_MMS"])
            placeholders = ', '.join(['?'] * len(self.nome_colunas["resultados_maxim_MMS"])) # Cria tantos "?" quanto o número de colunas


        if tabela == "resultados_maxim_MME":
            colunas_str = ', '.join(self.nome_colunas["resultados_maxim_MMS"])
            placeholders = ', '.join(['?'] * len(self.nome_colunas["resultados_maxim_MMS"])) # Cria tantos "?" quanto o número de colunas

        print()
        # SQL querry dinamica
        insert_sql = f"INSERT OR IGNORE INTO {tabela} ({colunas_str}) VALUES ({placeholders})"

        # Iterar pelos dados e inserir na tabela
        for data in dados:
            try:
                self.inserir_data(insert_sql, data, tabela)
                print(f"Dados inseridos na tabela {tabela} com sucesso!")
            except Exception as e:
                print(f"Erro ao inserir dados na tabela {tabela}: {e}")

def preparar_dados_para_insercao(df):
    """
    Prepara os dados de um DataFrame para inserção no banco de dados.

    Args:
    df (pd.DataFrame): O DataFrame contendo os dados.
    colunas (list): Uma lista com os nomes das colunas a serem extraídas do DataFrame.

    Returns:
    list of tuples: Uma lista de tuplas, onde cada tupla contém os valores correspondentes às colunas.
    """
    dados = []
    colunas = df.columns.tolist()
    # Itera sobre as linhas do DataFrame e extrai os valores das colunas especificadas
    for _, row in df.iterrows():
        dados.append(tuple(row[coluna] for coluna in colunas))  # Extrai os valores das colunas e os adiciona como tupla

    return dados

def setup_db(path):
    db = DatabaseManagement(path)
    db.abrir_conn()

    # Tabela - Input
    query1 = """
    CREATE TABLE IF NOT EXISTS dados_input (
        periodo int PRIMARY KEY,
        colmeia float NOT NULL,
        piquet float NOT NULL,
        maxim float NOT NULL
    );
    """
    db.criar_tabela(query1)

    # Tabela - Resultados
    query2 = """
    CREATE TABLE IF NOT EXISTS resultados_maxim_MMS (
        periodo int PRIMARY KEY,
        demanda_real float,
        previsao_media_movel float,
        erro float,
        erro_abs float,
        mape_previsao float
    );
    """
    db.criar_tabela(query2)

    query3 = """
    CREATE TABLE IF NOT EXISTS resultados_maxim_MME (
        periodo int PRIMARY KEY,
        demanda_real float,
        previsao_media_movel float,
        erro float,
        erro_abs float,
        mape_previsao float
    );
    """
    db.criar_tabela(query3)
    return db