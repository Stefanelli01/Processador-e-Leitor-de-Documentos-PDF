# Processador e Indexador de Documentos PDF

Ferramenta desenvolvida em Python para leitura, extração de metadados e indexação de arquivos PDF administrativos e licitatórios.

A aplicação utiliza a biblioteca PyMuPDF para extração do texto bruto, aplica padrões de Expressões Regulares (Regex) para identificar automaticamente dados estruturados (como números de processo e datas) e armazena os resultados em um banco de dados local SQLite.
Juntamente com a bilbioteca de interface CustomTkinter, para um visual de qualidade.

## Funcionalidades

- Extração de texto completo de arquivos PDF de forma rápida.
- Reconhecimento automático de números de processo e datas utilizando Expressões Regulares (Regex).
- Persistência dos metadados e do texto extraído em banco de dados SQLite local.
- Interface de linha de comando (CLI) interativa para processamento de novos arquivos e busca textual por palavras-chave ou números de processo.


## Tecnologias Utilizadas

- Linguagem: Python 3.10+
- Leitura de PDF: PyMuPDF (fitz)
- Interface: CustomTkinter v5.0.0+
- Extração de Padrões: Módulo nativo `re` (Regex)
- Banco de Dados: SQLite3