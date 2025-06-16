import csv
import psycopg2
import sys

#Conexão com o banco
db_params = {
    "database": "data_palavras",
    "user": "postgres",
    "password": "km04aktc21",
    "host": "localhost",
    "port": "5432",
}


file_path = 'suplemento_cursos_tecnicos_2024_tratado.csv' #Nome do arquivo a ser análisado
table_name = 'suplemento_cursos_tecnicos_2024' #Nome da tabela que será inserida no copy
csv_delimiter = ';'
csv_encoding = 'UTF8'

conn = None
cur = None

try:

    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    print("Conexão com o banco de dados bem-sucedida.")

    cur.execute(f"""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = current_schema() -- ou 'public' ou o schema correto (ex: 'public')
          AND table_name = '{table_name}'
        ORDER BY ordinal_position;
    """)
    table_columns = [row[0] for row in cur.fetchall()]

    if not table_columns:
        print(
            f"\nErro: Tabela '{table_name}' não encontrada ou não contém colunas no schema atual. Verifique o nome da tabela e o schema.")
        sys.exit(1)

    print(f"Colunas encontradas na tabela '{table_name}' no banco:")
    print(table_columns)

    try:
        with open(file_path, 'r', encoding=csv_encoding) as f:
            reader = csv.reader(f, delimiter=csv_delimiter)
            csv_headers = next(reader)

        print(f"\nCabeçalho encontrado no arquivo '{file_path}':")
        print(csv_headers)

        if not csv_headers:
            print(
                f"\nAviso: O arquivo '{file_path}' está vazio ou não tem cabeçalho.")

    except FileNotFoundError:
        print(f"\nErro: Arquivo não encontrado no caminho: {file_path}")
        print("Verifique se o caminho está correto e se você tem permissão de leitura para o arquivo.")
        sys.exit(1)
    except StopIteration:
        print(
            f"\nAviso: O arquivo '{file_path}' está vazio ou só contém o cabeçalho.")
        csv_headers = []

    table_columns_lower = {col.lower(): col for col in table_columns}

    def clean_header(header):
        return header.lower().strip()

    final_copy_columns = []
    headers_without_table_match = []

    for header in csv_headers:
        cleaned_header = clean_header(header)

        matched_col = table_columns_lower.get(cleaned_header)
        if matched_col:

            final_copy_columns.append(matched_col)
        else:

            headers_without_table_match.append(header)

    if headers_without_table_match:
        print("\nAviso: Alguns headers do CSV não encontraram correspondência na tabela (verifique nomes e case):")
        print(headers_without_table_match)
        print("\nPara que o \\copy funcione corretamente com uma lista de colunas, o número de colunas listadas DEVE ser igual ao número total de campos no arquivo CSV que você deseja ler para essas colunas.")
        print("Se houver headers sem match, eles serão ignorados na lista de colunas do \\copy.")
        print("Isso pode causar erros se as colunas ignoradas não estiverem no final do arquivo CSV.")
    elif not final_copy_columns and csv_headers:
        print("\nErro: Nenhum header do CSV pôde ser mapeado para uma coluna na tabela. Verifique se os headers do CSV e os nomes das colunas da tabela correspondem (pelo menos em lower case) ou ajuste a função clean_header.")
        sys.exit(1)

    columns_clause = ""
    if final_copy_columns:
        columns_clause = "(" + ", ".join(final_copy_columns) + ")"
        print(
            f"\nNúmero de colunas mapeadas do CSV para a tabela: {len(final_copy_columns)}")
        print(f"Número total de headers no CSV: {len(csv_headers)}")
        if len(final_copy_columns) != len(csv_headers):
            print(
                "\nAviso: O número de colunas mapeadas é diferente do número total de headers do CSV.")
            print(
                "O comando \\copy gerado incluirá a cláusula de colunas. Isso funcionará")
            print(
                "SE as colunas correspondentes no arquivo CSV estão na mesma ordem que na lista gerada")
            print(
                "E SE as colunas no CSV sem correspondência na tabela estão *no final* do arquivo.")
            print("Caso contrário, o \\copy pode falhar com erros de mapeamento ou tipo.")
    elif csv_headers:
        print("\nNão foi possível gerar a cláusula de colunas para o \\copy porque nenhum header do CSV mapeou para a tabela.")
        print("O comando \\copy será gerado SEM a lista de colunas, tentando mapear todos os campos do arquivo para a tabela na ordem padrão.")
        print("Isso provavelmente resultará no mesmo erro de 'invalid input syntax' que você teve inicialmente.")
        print("Recomenda-se corrigir o mapeamento de nomes entre o CSV e a tabela.")

    copy_command_string = f"""
\\copy {table_name} {columns_clause} FROM '{file_path}' DELIMITER '{csv_delimiter}' CSV HEADER ENCODING '{csv_encoding}';
"""

    print("\nComando \\copy gerado (copie e cole no seu terminal psql):")
    print(copy_command_string)
    print("\nVerifique se a lista de colunas gerada corresponde à ordem dos campos no seu arquivo")
    print("e se pulou corretamente colunas como ID SERIAL se for o caso (colunas da tabela não mapeadas pelo header do CSV não entram na lista).")


except psycopg2.OperationalError as e:
    print(f"\nErro de conexão com o banco de dados: {e}")
    print("Verifique as configurações de host, porta, usuário, senha e nome do banco de dados.")
except psycopg2.ProgrammingError as e:
    print(
        f"\nErro de programação no banco de dados (ex: tabela não existe, sintaxe SQL inválida na query de colunas): {e}")
    print(
        f"Query executada para obter colunas: SELECT column_name FROM information_schema.columns WHERE table_schema = current_schema() AND table_name = '{table_name}' ORDER BY ordinal_position;")
except Exception as e:
    print(f"\nOcorreu um erro inesperado: {e}")
    print(f"Tipo do erro: {type(e).__name__}")
    
finally:
    if cur:
        cur.close()
    if conn:
        conn.close()
