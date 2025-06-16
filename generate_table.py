import pandas as pd
import sys

arquivo_csv = 'suplemento_cursos_tecnicos_2024_tratado.csv' #Caminho do arquivo a ser análisado
nome_tabela = 'suplemento_cursos_tecnicos_2024' #Nome tabela
delimitador = ';'
encoding_csv = 'utf-8'


print(f"Lendo o cabeçalho do arquivo: '{arquivo_csv}' ...")
try:
    df = pd.read_csv(arquivo_csv, delimiter=delimitador,
                     nrows=1000, encoding=encoding_csv, header=0)

    csv_column_count = len(df.columns)
    print(
        f"✓ Sucesso: Cabeçalho lido. Foram identificadas {csv_column_count} colunas no arquivo CSV.")

except FileNotFoundError:
    print(
        f"✗ ERRO: Arquivo CSV não encontrado em '{arquivo_csv}'. Verifique o caminho.")
    sys.exit(1)
except Exception as e:
    print(f"✗ ERRO ao ler o cabeçalho do arquivo CSV: {e}")
    print("Por favor, verifique o caminho do arquivo, o delimitador e a codificação.")
    sys.exit(1)

def map_pandas_type_to_postgres(pandas_type):
    if 'int' in str(pandas_type):

        return 'INTEGER'
    elif 'float' in str(pandas_type):
        return 'NUMERIC'
    elif 'bool' in str(pandas_type):
        return 'BOOLEAN'
    else:
        return 'TEXT'


column_definitions = []
print("\nGerando definições de colunas para o script CREATE TABLE...")
for col_name, dtype in df.dtypes.items():
    sql_col_name = f'"{col_name.lower()}"'
    sql_col_type = map_pandas_type_to_postgres(dtype)
    column_definitions.append(f"{sql_col_name} {sql_col_type}")

sql_column_count = len(column_definitions)
print(
    f"✓ Sucesso: Foram geradas {sql_column_count} definições de colunas para o script SQL.")

print("\n--- Script CREATE TABLE gerado ---")
create_table_sql = f"CREATE TABLE {nome_tabela} (\n    "
create_table_sql += ",\n    ".join(column_definitions)
create_table_sql += "\n);"
print(create_table_sql)
print("---------------------------------")
print("\n--- Resultado da Comparação ---")
print(
    f"Número de colunas no CSV (identificadas pelo pandas): {csv_column_count}")
print(f"Número de colunas definidas no script SQL gerado: {sql_column_count}")

if csv_column_count == sql_column_count:
    print("\n🎉 Ambos os contadores são iguais!")
    print("   O número de colunas no CSV corresponde ao número de colunas no CREATE TABLE gerado.")
    print("   Você pode usar este script CREATE TABLE.")
else:
    print("\n⚠️ ATENÇÃO: Os contadores são DIFERENTES!")
    print("   Isso indica uma possível inconsistência entre o CSV e o script gerado.")
    print("   Revise a leitura do CSV (delimitador, cabeçalho) e a lógica de geração do script SQL.")

print(f"\n--- Comando para carregar os dados (ajuste o caminho do arquivo) ---")
print(f"COPY {nome_tabela} FROM '{arquivo_csv}'")
print(f"DELIMITER '{delimitador}'")
print(f"CSV HEADER")
print(f"ENCODING '{encoding_csv}';")
print("------------------------------------------------------------------")
