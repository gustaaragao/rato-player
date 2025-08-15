import psycopg2
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente do .env
load_dotenv()

# Lê as variáveis do .env
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def conectar_bd():
    """
    Tenta conectar ao banco de dados PostgreSQL.
    Retorna o objeto de conexão se bem-sucedido, senão retorna None.
    """
    conn = None
    try:
        # Conecta ao banco
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("INFO: Conexão com o banco de dados bem-sucedida! ✅")
        return conn
    except Exception as e:
        print(f"ERROR: Erro ao conectar ao banco ❌")
        print(f"ERROR: {e}")
        return None

def inserir_colecoes(conn):
    """
    Insere uma lista de coleções na tabela 'Colecao' usando executemany.
    """
    if not conn:
        return

    # Lista de tuplas com os dados das coleções a serem inseridas
    colecoes_para_inserir = [
        (0, '/capas/edsongomes_campodebatalha.jpg', 2274, '1992-01-06', 'Campo de Batalha', 'Album'),
        (1, '/capas/papangu_holoceno.jpg', 2648, '2021-06-25', 'Holoceno', 'Album'),
        (2, '/capas/druqks.jpg', 6000, '2001-08-22', 'Druqks', 'Album'),
        (3, '/capas/last-words.jpg', 1328, '2020-01-08', 'Last Words: Screamed from Behind God''s Muzzle', 'EP'),
        (4, '/capas/gybe_fsharpasharpinfinity.jpg', 3780, '1997-08-14', 'F♯ A♯ ∞', 'Album'),
        (5, '/necrophagist_onsetofputrefication.png', 2530, '2004-01-01', 'Onset Of Putrefication', 'Album'),
        (6, '/sapac/thedailymail_staircase.webp', 489, '2011-12-19', 'The Daily Mail/Staircase', 'Single'),
        (7, '/capas/duster_capsulelosingcontact.gif', 9000, '2019-03-22', 'Capsule Losing Contact', 'Compilacao'),
        (8, '/games/th/mof_ost.wbmp', 4620, '2007-08-17', '東方風神録　～ Mountain of Faith', 'Album'),
        (9, '/capas/engenheiros_infinitahighway.ogg', 27240, '1998-03-04', 'Infinita Highway', 'Compilacao')
    ]

    print(f"\n--- Inserindo {len(colecoes_para_inserir)} coleções na tabela... ---")
    try:
        with conn.cursor() as cur:
            # Query com ON CONFLICT para evitar erros em execuções repetidas
            query = """
                INSERT INTO colecao (id_colecao, caminho_capa, duracao, data_lancamento, titulo, tipo) 
                VALUES (%s, %s, %s, %s, %s, %s);
            """

            # executemany é otimizado para inserir múltiplas linhas
            cur.executemany(query, colecoes_para_inserir)
            
            conn.commit()
            
            # cur.rowcount retorna o número de linhas afetadas pela última operação
            print(f"INFO: {cur.rowcount} novas coleções inseridas com sucesso! ✨")

    except Exception as e:
        print(f"ERROR: Erro ao inserir coleções ❌")
        print(f"ERROR: {e}")
        conn.rollback()

def consultar_colecoes(conn):
    """
    Executa uma consulta SELECT para buscar e exibir os dados da tabela Colecao.
    """
    if not conn:
        return

    print("\n--- Consultando coleções no banco de dados... ---")
    try:
        with conn.cursor() as cur:
            query = "SELECT id_colecao, titulo, tipo, data_lancamento FROM colecao ORDER BY id_colecao;"
            cur.execute(query)
            
            resultados = cur.fetchall()
            
            print(f"INFO: {len(resultados)} coleções encontradas.")
            for colecao in resultados:
                # O formato da data é um objeto datetime, formatamos para string
                data_formatada = colecao[3].strftime('%d/%m/%Y')
                print(f"  ID: {colecao[0]:<2} | Título: {colecao[1]:<45} | Tipo: {colecao[2]:<11} | Lançamento: {data_formatada}")

    except Exception as e:
        print(f"ERROR: Erro ao consultar coleções ❌")
        print(f"ERROR: {e}")

def main():
    """
    Função principal que orquestra a conexão e as operações no banco.
    """
    conn = None
    try:
        # Tenta se conectar ao Banco
        conn = conectar_bd()

        # Se a conexão foi estabelecida, executa as operações
        if conn:
            # 1. Insere a lista de coleções
            inserir_colecoes(conn)
            
            # 2. Consulta e exibe as coleções para verificar
            consultar_colecoes(conn)

    except Exception as e:
        print(f"ERROR: Um erro inesperado ocorreu durante a execução: {e}")
    finally:
        # Este bloco SEMPRE será executado, garantindo que a conexão seja fechada
        if conn:
            conn.close()
            print("\nINFO: Conexão com o banco de dados fechada. 👋")

if __name__ == '__main__':
    main()