Manipulação e Conversão de Arquivos do Censo Escolar
Este repositório contém scripts criados para automatizar o processo de geração de tabelas e importação de dados de arquivos do Censo Escolar para um banco de dados PostgreSQL. Os arquivos do censo são disponibilizados anualmente em formatos extensos e despadronizados, tornando inviável sua inserção manual.

Objetivo
Automatizar:

Geração de comandos CREATE TABLE

Criação de comandos COPY para importação de dados

Preparação de arquivos massivos com base nos dados fornecidos pelo Censo Escolar

Scripts principais
generate_schema_dicionary.py:
Gera comandos CREATE TABLE a partir de dicionários de dados do Censo, onde constam as variáveis, tipos e descrições.

generate_table.py:
Gera comandos CREATE TABLE diretamente de arquivos de dados, analisando cabeçalhos e conteúdos.

generate_copy.py:
Gera comandos COPY para importar os dados diretamente para o PostgreSQL.
Requer configuração manual dos dados de conexão com o banco e validação do schema alvo.

Uso
Configure seu ambiente Python.

Prepare os arquivos de entrada.

Execute um dos scripts conforme a necessidade:

bash
Copiar
Editar
python generate_schema_dicionary.py 
python generate_table.py 
python generate_copy.py 
No caso do generate_copy.py, edite o script para incluir suas credenciais do banco e informações da tabela alvo.

Observações
A inserção manual de dados não é viável devido ao grande volume de registros.

É necessário validar os arquivos e dicionários do Censo antes de utilizar os scripts.

Certifique-se de que o PostgreSQL está configurado corretamente e acessível pela máquina local.
