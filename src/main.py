import pymupdf as fitz
import re
import sqlite3
import os
from pathlib import Path
from tkinter import  messagebox, Tk

PASTA_RAIZ = Path(__file__).resolve().parents[1]
DB_NAME = PASTA_RAIZ / "documentos.db"

root = Tk()
root.withdraw()

def init_db():

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS documentos_pdf (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_arquivo TEXT NOT NULL,
            caminho_arquivo TEXT NOT NULL,
            total_paginas INTEGER NOT NULL,
            numero_processo TEXT,
            data_identificada TEXT,
            conteudo_texto TEXT NOT NULL,
            criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()
        conn.close()

    except Exception as e:
        messagebox.showerror("Erro durante a inicialização do Banco de Dados", f"Falha ao Iniciar o DB:\n{e}")
        return "Erro", "Erro"

def extrair_metadados_regex(texto):

    try:
        padrao_processo = r"(?:processo|edital|licitação|licitacao|n°|no|num|nº)?\s*[:.]?\s*(\d+[\/\.-]\d+[\/\.-]?\d*)"
        match_processo = re.search(padrao_processo, texto, re.IGNORECASE)
        num_processo = match_processo.group(1) if match_processo else "Não identificado"

        padrao_data = r"\b(\d{2}[\/\.-]\d{2}[\/\.-]\d{4})\b"
        match_data = re.search(padrao_data, texto)
        data_encontrada = match_data.group(1) if match_data else "Não identificada"

        return num_processo, data_encontrada

    except Exception as e:
        messagebox.showerror("Erro durante a extração", f"Falha ao extrair metadados:\n{e}")
        return "Erro", "Erro"


def processar_pdf(caminho_pdf):

    try:
        if not os.path.exists(caminho_pdf):
            print(f"Erro, {caminho_pdf} não localizado")
            return {"sucesso": False, "erro": "Arquivo não encontrado."}

        print(f"\n Lendo arquivo = {caminho_pdf}")
        doc = fitz.open(caminho_pdf)

        texto_completo = ""
        for pagina in doc:
            texto_completo += pagina.get_text()

        total_paginas = len(doc)
        doc.close()

        num_processo, data_encontrada = extrair_metadados_regex(texto_completo)

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        query = """
            INSERT INTO documentos_pdf
            (nome_arquivo, caminho_arquivo, total_paginas, numero_processo, data_identificada, conteudo_texto)
            VALUES (?, ?, ?, ?, ?, ?)
        """

        nome_arquivo = os.path.basename(caminho_pdf)
        cursor.execute(query, (nome_arquivo, caminho_pdf, total_paginas, num_processo, data_encontrada, texto_completo))

        conn.commit()
        conn.close()

        return {
            "sucesso": True,
            "processo": num_processo,
            "data": data_encontrada,
            "total_paginas": total_paginas,
            "nome_arquivo": nome_arquivo
        }

    except Exception as e:
        messagebox.showerror("Erro durante o processamento", f"Falha ao processar o pdf:\n{e}")
        return "Erro", "Erro"


def pesquisar_documentos(termo_busca):

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        query = """
            SELECT numero_processo, nome_arquivo, data_identificada, 'Concluído' as status
            FROM documentos_pdf
            WHERE conteudo_texto LIKE ? OR numero_processo LIKE ? OR nome_arquivo LIKE ?
        """

        termo_sql = f"%{termo_busca}%"
        cursor.execute(query, (termo_sql, termo_sql, termo_sql))
        resultados = cursor.fetchall()
        conn.close()

        return resultados

    except Exception as e:
        messagebox.showerror("Erro durante a busca", f"Falha ao buscar::\n{e}")
        return "Erro", "Erro"

def obter_resumo():

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM documentos_pdf")
        total = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM documentos_pdf WHERE DATE(criado_em, 'localtime') = DATE('now', 'localtime')")
        consultas_hoje = cursor.fetchone()[0]

        cursor.execute("""
            SELECT id, numero_processo, datetime(criado_em, 'localtime'), 'Concluído'
            FROM documentos_pdf
            ORDER BY id DESC LIMIT 5
        """)
        recentes = cursor.fetchall()
        conn.close()

        return total, consultas_hoje, recentes

    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao obter resumo:\n{e}")
        return "Erro", "Erro"