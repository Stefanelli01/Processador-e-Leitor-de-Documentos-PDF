import customtkinter as ctk
from pathlib import Path
from tkinter import filedialog, messagebox

from src.main import init_db, processar_pdf, pesquisar_documentos, obter_resumo


arquivo_atual = Path(__file__).resolve()
pasta_raiz = arquivo_atual.parents[2]
arquivo_alvo = pasta_raiz / "assets/themes/theme.json"

ctk.set_appearance_mode("System")
if arquivo_alvo.exists():
    ctk.set_default_color_theme(str(arquivo_alvo))
else:
    ctk.set_default_color_theme("blue")


class App(ctk.CTk):

    def mostrar_inicio(self):
        self.atualizar_inicial()
        self.mudar_tela(self.tela_inicio)

    def mostrar_processar(self):
        self.mudar_tela(self.tela_process)

    def mostrar_pesquisar(self):
        self.filtrar_resultados()
        self.mudar_tela(self.tela_pesq)

    def selecionar_arquivo(self):
        caminho = filedialog.askopenfilename(
            title="Selecione o arquivo PDF",
            filetypes=[("Arquivos PDF", "*.pdf"), ("Todos os arquivos", "*.*")]
        )
        if caminho:
            self.entry_caminho.delete(0, "end")
            self.entry_caminho.insert(0, caminho)

    def carregar_tabela_pesquisa(self, dados):
        for widget in self.frame_tabela_pesq.winfo_children():
            widget.destroy()

        headers = ["N° de Processo", "Ficheiro PDF", "Data", "Status", "Ação"]
        for col_idx, text_header in enumerate(headers):
            lbl = ctk.CTkLabel(
                self.frame_tabela_pesq,
                text=text_header,
                font=ctk.CTkFont("Helvetica", size=13, weight="bold"),
                text_color="#ebc075"
            )
            lbl.grid(row=0, column=col_idx, padx=10, pady=10, sticky="w")

        for row_idx, row_data in enumerate(dados, start=1):
            processo, ficheiro, data, status = row_data
            cor_status = "#2ed573" if status == "Concluído" else ("#ff4757" if status == "Erro" else "#ffbe76")

            ctk.CTkLabel(self.frame_tabela_pesq, text=processo, text_color="gray80").grid(row=row_idx, column=0, padx=10, pady=6, sticky="w")
            ctk.CTkLabel(self.frame_tabela_pesq, text=ficheiro, text_color="gray80").grid(row=row_idx, column=1, padx=10, pady=6, sticky="w")
            ctk.CTkLabel(self.frame_tabela_pesq, text=data, text_color="gray80").grid(row=row_idx, column=2, padx=10, pady=6, sticky="w")
            ctk.CTkLabel(self.frame_tabela_pesq, text=status, text_color=cor_status).grid(row=row_idx, column=3, padx=10, pady=6, sticky="w")

            btn_ver = ctk.CTkButton(
                self.frame_tabela_pesq,
                text="Ver Detalhes",
                width=90,
                height=26,
                fg_color="gray30",
                hover_color="gray20",
                command=lambda p=processo: messagebox.showinfo("Detalhes", f"Processo: {p}")
            )
            btn_ver.grid(row=row_idx, column=4, padx=10, pady=6, sticky="w")

    def iniciar_processamento(self):
        caminho = self.entry_caminho.get().strip()
        if not caminho:
            messagebox.showwarning("Aviso", "Selecione um arquivo PDF primeiro.")
            return

        self.lbl_mensagem_status.configure(text="Processando arquivo...", text_color="#ffbe76")
        self.update_idletasks()

        res = processar_pdf(caminho)

        if res.get("sucesso"):
            self.lbl_mensagem_status.configure(text="Sucesso!", text_color="#2ed573")
            self.lbl_processo.configure(text=f"N° de processo: {res['processo']}")
            self.lbl_data.configure(text=f"Data encontrada: {res['data']}")
            self.lbl_pag.configure(text=f"Total de páginas: {res['total_paginas']}")
            self.atualizar_inicial()
        else:
            self.lbl_mensagem_status.configure(text=f"Erro: {res.get('erro', 'Falha ao processar')}", text_color="#ff4757")

    def filtrar_resultados(self):
        termo = self.entry_busca.get().lower().strip()
        resultados = pesquisar_documentos(termo)
        self.carregar_tabela_pesquisa(resultados)

    def atualizar_inicial(self):
        total, consultas_hoje, recentes = obter_resumo()
        self.lbl_total_val.configure(text=str(total))
        self.lbl_hoje_val.configure(text=str(consultas_hoje))

        for widget in self.table_frame.winfo_children():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()

        for row_idx, row_data in enumerate(recentes, start=1):
            for col_idx, value in enumerate(row_data):
                cor_status = "#2ed573" if value == "Concluído" else "gray80"
                lbl = ctk.CTkLabel(
                    self.table_frame,
                    text=str(value),
                    text_color=cor_status if col_idx == 3 else "gray80"
                )
                lbl.grid(row=row_idx, column=col_idx, padx=15, pady=6, sticky="w")

    def __init__(self):
        super().__init__()

        init_db()

        self.title("Interface")
        self.geometry("1360x700")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_menu = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.frame_menu.grid(row=0, column=0, sticky="nsew")

        self.label_menu = ctk.CTkLabel(self.frame_menu, text="MENU", font=ctk.CTkFont(size=20, weight="bold"))
        self.label_menu.pack(pady=20, padx=20)

        self.btn_ini = ctk.CTkButton(self.frame_menu, text="Inicio", width=150, height=50, font=("Helvetica", 16, "bold"), command=self.mostrar_inicio)
        self.btn_ini.pack(pady=10, padx=20)

        self.btn_process = ctk.CTkButton(self.frame_menu, text="Processar", width=150, height=50, font=("Helvetica", 16, "bold"), command=self.mostrar_processar)
        self.btn_process.pack(pady=10, padx=20)

        self.btn_pesq = ctk.CTkButton(self.frame_menu, text="Pesquisar", width=150, height=50, font=("Helvetica", 16, "bold"), command=self.mostrar_pesquisar)
        self.btn_pesq.pack(pady=10, padx=20)

        self.tela_atual = None
        self.criar_telas()

        self.mostrar_inicio()

    def criar_telas(self):

        # Tela inicial
        self.tela_inicio = ctk.CTkFrame(self, fg_color="transparent")
        self.tela_inicio.grid_columnconfigure(0, weight=1)

        self.lbl_title = ctk.CTkLabel(
            self.tela_inicio,
            text="Seja Bem-Vindo!",
            font=ctk.CTkFont("Helvetica", size=24, weight="bold")
        )
        self.lbl_title.pack(anchor="w", pady=(0, 2))

        self.lbl_title_sub = ctk.CTkLabel(
            self.tela_inicio,
            text="O que faremos hoje?",
            font=ctk.CTkFont("Helvetica", size=18, weight="bold"),
            text_color="#ebc075"
        )
        self.lbl_title_sub.pack(anchor="w", pady=(0, 2))

        self.cards_frame = ctk.CTkFrame(self.tela_inicio, fg_color="transparent")
        self.cards_frame.pack(fill="x", pady=10)

        self.card1 = ctk.CTkFrame(self.cards_frame)
        self.card1.pack(side="left", expand=True, fill="both", padx=(0, 10))
        ctk.CTkLabel(self.card1, text="Total Processado", font=ctk.CTkFont(size=12), text_color="gray").pack(pady=(10, 0))
        self.lbl_total_val = ctk.CTkLabel(self.card1, text="0", font=ctk.CTkFont(size=22, weight="bold"))
        self.lbl_total_val.pack(pady=(0, 10))

        self.card2 = ctk.CTkFrame(self.cards_frame)
        self.card2.pack(side="left", expand=True, fill="both", padx=5)
        ctk.CTkLabel(self.card2, text="Consultas Hoje", font=ctk.CTkFont(size=12), text_color="gray").pack(pady=(10, 0))
        self.lbl_hoje_val = ctk.CTkLabel(self.card2, text="0", font=ctk.CTkFont(size=22, weight="bold"))
        self.lbl_hoje_val.pack(pady=(0, 10))

        self.card3 = ctk.CTkFrame(self.cards_frame)
        self.card3.pack(side="left", expand=True, fill="both", padx=(10, 0))
        ctk.CTkLabel(self.card3, text="Status do Banco", font=ctk.CTkFont(size=12), text_color="gray").pack(pady=(10, 0))
        ctk.CTkLabel(self.card3, text="● Conectado", font=ctk.CTkFont(size=16, weight="bold"), text_color="#2ed573").pack(pady=(5, 10))

        self.table_frame = ctk.CTkFrame(self.tela_inicio)
        self.table_frame.pack(fill="both", expand=True, pady=(0, 10))
        self.table_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        headers = ["ID", "Processo", "Data / Hora", "Status"]
        for col_idx, text_header in enumerate(headers):
            lbl = ctk.CTkLabel(
                self.table_frame,
                text=text_header,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#ebc075"
            )
            lbl.grid(row=0, column=col_idx, padx=15, pady=10, sticky="w")

        # Tela processar
        self.tela_process = ctk.CTkFrame(self, fg_color="transparent")
        self.tela_process.grid_columnconfigure(0, weight=1)

        self.lbl_process = ctk.CTkLabel(
            self.tela_process,
            text="Processamento de arquivos PDF",
            font=ctk.CTkFont("Helvetica", size=24, weight="bold")
        )
        self.lbl_process.pack(anchor="w", pady=(0, 20))

        self.frame_seletor = ctk.CTkFrame(self.tela_process, fg_color="transparent")
        self.frame_seletor.pack(fill="x", pady=10)

        self.entry_caminho = ctk.CTkEntry(
            self.frame_seletor,
            placeholder_text="Nenhum arquivo selecionado",
            height=40,
            border_color="#ff6600"
        )
        self.entry_caminho.pack(side="left", padx=(0, 10), expand=True, fill="x")

        self.btn_procurar = ctk.CTkButton(
            self.frame_seletor,
            text="Procurar...",
            width=120,
            height=40,
            fg_color="gray30",
            hover_color="gray20",
            command=self.selecionar_arquivo
        )
        self.btn_procurar.pack(side="left")

        self.btn_enviar = ctk.CTkButton(
            self.tela_process,
            text="Processar",
            width=150,
            height=40,
            fg_color="#ff6600",
            hover_color="#cc5200",
            command=self.iniciar_processamento
        )
        self.btn_enviar.pack(pady=20)

        self.lbl_mensagem_status = ctk.CTkLabel(
            self.tela_process,
            text="",
            font=ctk.CTkFont("Helvetica", size=14, weight="bold")
        )
        self.lbl_mensagem_status.pack(pady=(0, 20))

        self.lbl_processo = ctk.CTkLabel(
            self.tela_process,
            text="",
            font=ctk.CTkFont("Helvetica", size=18, weight="bold")
        )
        self.lbl_processo.pack(anchor="w", pady=(20, 0))

        self.lbl_data = ctk.CTkLabel(
            self.tela_process,
            text="",
            font=ctk.CTkFont("Helvetica", size=18, weight="bold")
        )
        self.lbl_data.pack(anchor="w", pady=(10, 0))

        self.lbl_pag = ctk.CTkLabel(
            self.tela_process,
            text="",
            font=ctk.CTkFont("Helvetica", size=18, weight="bold")
        )
        self.lbl_pag.pack(anchor="w", pady=(10, 0))

        # Tela pesquisar
        self.tela_pesq = ctk.CTkFrame(self, fg_color="transparent")
        self.tela_pesq.grid_columnconfigure(0, weight=1)

        self.lbl_title_pesq = ctk.CTkLabel(
            self.tela_pesq,
            text="Consulta de Processos",
            font=ctk.CTkFont("Helvetica", size=24, weight="bold")
        )
        self.lbl_title_pesq.pack(anchor="w", pady=(0, 20))

        self.frame_filtros = ctk.CTkFrame(self.tela_pesq)
        self.frame_filtros.pack(fill="x", pady=(0, 15), padx=5)

        self.entry_busca = ctk.CTkEntry(
            self.frame_filtros,
            placeholder_text="Procurar por N° de processo ou ficheiro",
            height=40,
            border_color="#ff6600"
        )
        self.entry_busca.pack(side="left", padx=10, pady=10, expand=True, fill="x")

        self.filtro_status = ctk.CTkOptionMenu(
            self.frame_filtros,
            values=["Todos", "Con", "Pndt", "Erro"],
            width=180,
            height=40,
            fg_color="gray30",
            button_color="#ff6600",
            button_hover_color="#cc5200"
        )
        self.filtro_status.pack(side="left", padx=(0, 10), pady=10)

        self.btn_executar_busca = ctk.CTkButton(
            self.frame_filtros,
            text="Pesquisar",
            width=120,
            height=40,
            fg_color="#ff6600",
            hover_color="#cc5200",
            command=self.filtrar_resultados
        )
        self.btn_executar_busca.pack(side="left", padx=(0, 10), pady=10)

        self.frame_tabela_pesq = ctk.CTkScrollableFrame(self.tela_pesq, height=380)
        self.frame_tabela_pesq.pack(fill="both", expand=True, pady=5)
        self.frame_tabela_pesq.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

    def mudar_tela(self, nova_tela):
        if self.tela_atual is not None:
            self.tela_atual.grid_forget()

        self.tela_atual = nova_tela
        self.tela_atual.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)


    def on_closing(self):
        self.withdraw()
        self.destroy()
        self.quit()

if __name__ == "__main__":
    app = App()
    app.mainloop()