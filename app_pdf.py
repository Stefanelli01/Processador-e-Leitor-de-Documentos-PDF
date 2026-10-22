import fitz
import re
import sqlite3
import os
from datetime import datetime

DB_NAME = "documentos.db"



def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents_pdf (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_arquivo TEXT NOT NULL,
        diretório_arquivo TEXT NOT NULL,
        total_paginas INTEGER NOT NULL,
        numero_processo TEXT,
        data_identificada TEXT,
        conteudo_texto TEXT NOT NULL,
        criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()



def extrair_metadados_regex(texto):

    padrao_processo = r"(?:processo|edital|licitação)?\s*(?:n°|no|num)?\s(\d+[\/\.-]\d{4})"

    match_processo = re.search(padrao_processo, texto, re.IGNORECASE)
    num_processo = match_processo.group(1) if match_processo else "Não identificado"  ## Alterar quando for para janela

    padrao_data = r"\b(\d{2}[\/\.-]\d{2}[\/\.-]\d{4})\b"
    match_data = re.search(padrao_data, texto)
    data_encontrada = match_data.group(1) if match_data else "Não identificada" ## Alterar quando for para janela

    return num_processo, data_encontrada



def processar_pdf(caminho_pdf):
    if not os.path.exists(caminho_pdf):
        print(f"Erro, {caminho_pdf} não localizado")
        return

    print(f"\n Lendo arquivo = {caminho_pdf}")
    doc =fitz.open(caminho_pdf)

    texto_completo = ""
    for pagina in doc:
        texto_completo += pagina.get_text()

    total_paginas = len(doc)
    doc.close()

    num_processo, data_encontrada = extrair_metadados_regex(texto_completo)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    query = """
        INSERT INTO documents_pdf
        (nome_arquivo, caminho_arquivo, total_paginas, numero_processo, data_identificada, conteudo_texto)
        VALUES (?, ?, ?, ?, ?, ?)
    """

    nome_arquivo = os.path.basename(caminho_pdf)
    cursor.execute(query, (nome_arquivo, caminho_pdf, total_paginas, num_processo, data_encontrada, texto_completo))

    conn.commit()
    conn.close()

    print("Sucesso, index no SQL")
    print(f"Processo: {num_processo}")
    print(f"Data: {data_encontrada}")
    print(f"Total_pag: {total_paginas}")

