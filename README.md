Manipulação e Conversão de Arquivos do Censo Escolar

Repositório com o intuito de automatizar a geração de tabelas e a importação de dados dos arquivos do Censo Escolar para um banco de dados PostgreSQL.
Objetivo Automatizar:
- Geração de comandos CREATE TABLE
- Criação de comandos COPY para importação de dados
- Preparação de arquivos massivos com base nas informações fornecidas pelo Censo Escolar
Scripts principais:
- generate_schema_dicionary.py: Este script gera comandos CREATE TABLE a partir dos dicionários de dados do Censo, que incluem variáveis, tipos e descrições.
- generate_table.py: Este script cria comandos CREATE TABLE diretamente de arquivos de dados, analisando os cabeçalhos e conteúdos.
- generate_copy.py: Este script gera comandos COPY que importam os dados diretamente para o banco de dados. É necessário configurar manualmente os dados de conexão com o banco e validar a tabela de destino.
Uso:
1. Configure seu ambiente Python.
2. Prepare os arquivos de entrada.
3. Execute um dos scripts conforme sua necessidade:
   ```bash
   python generate_schema_dicionary.py
   python generate_table.py
   python generate_copy.py
   ```
No caso do `generate_copy.py`, edite o script para incluir suas credenciais do banco e as informações da tabela de destino.
Observações:
- A inserção manual de dados não é viável devido ao grande volume de registros.
- É fundamental validar os arquivos e dicionários do Censo antes de utilizar os scripts.
- Conferir o PostgreSQL, ele deve estar configurado corretamente e acessível a partir da máquina local.
