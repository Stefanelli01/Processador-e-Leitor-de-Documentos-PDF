import customtkinter as ctk
from pathlib import Path
from tkinter import filedialog
import time
import threading

arquivo_atual = Path(__file__).resolve()
pasta_raiz = arquivo_atual.parents[2]

caminho_subpasta = pasta_raiz / "assets/themes"
arquivo_alvo = caminho_subpasta / "theme.json"

ctk.set_appearance_mode("System")

if arquivo_alvo.exists():
    ctk.set_default_color_theme(str(arquivo_alvo))
else:
    ctk.set_default_color_theme("blue")


class App(ctk.CTk):

    def mostrar_inicio(self):
        self.mudar_tela(self.tela_inicio)

    def mostrar_processar(self):
        self.mudar_tela(self.tela_process)

    def mostrar_pesquisar(self):
        self.mudar_tela(self.tela_pesq)

    def selecionar_arquivo(self):
        caminho = filedialog.askopenfilename(
            title="Selecione o arquivo PDF",
            filetypes=[("Arquivos PDF", "*.pdf"), ("Todos os arquivos", "*.*")]
        )
        if caminho:
            self.entry_caminho.delete(0, "end")
            self.entry_caminho.insert(0, caminho)

    def iniciar_processamento(self):
        caminho = self.entry_caminho.get().strip()

        if not caminho or caminho == "Nenhum arquivo selecionado...":
            self.lbl_mensagem_status.configure(
                text="Erro: Nenhum arquivo foi selecionado!",
                text_color="#ff4757"
            )
            return

        self.lbl_mensagem_status.configure(
            text="Processando arquivo, aguarde...",
            text_color="gray"
        )
        self.lbl_processo.configure(text="N° de processo: -")
        self.lbl_data.configure(text="Data encontrada: -")
        self.lbl_pag.configure(text="Total de páginas: -")

        self.btn_enviar.configure(state="disabled")
        threading.Thread(target=self.simular_processamento_pdf, daemon=True).start()

    def simular_processamento_pdf(self):
        try:
            time.sleep(2)
            self.lbl_mensagem_status.configure(
                text="Task finalizada!",
                text_color="#2ed573"
            )
            self.lbl_processo.configure(text="N° de processo: 2026.008492-1")
            self.lbl_data.configure(text="Data encontrada: 23/10/2026")
            self.lbl_pag.configure(text="Total de páginas: 14")
        except Exception as e:
            self.lbl_mensagem_status.configure(
                text=f"Erro ao processar: {str(e)}",
                text_color="#ff4757"
            )
        finally:
            self.btn_enviar.configure(state="normal")

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

            ctk.CTkLabel(self.frame_tabela_pesq, text=processo, text_color="gray80").grid(row=row_idx, column=0,
                                                                                          padx=10, pady=6, sticky="w")
            ctk.CTkLabel(self.frame_tabela_pesq, text=ficheiro, text_color="gray80").grid(row=row_idx, column=1,
                                                                                          padx=10, pady=6, sticky="w")
            ctk.CTkLabel(self.frame_tabela_pesq, text=data, text_color="gray80").grid(row=row_idx, column=2, padx=10,
                                                                                      pady=6, sticky="w")
            ctk.CTkLabel(self.frame_tabela_pesq, text=status, text_color=cor_status).grid(row=row_idx, column=3,
                                                                                          padx=10, pady=6, sticky="w")

            btn_ver = ctk.CTkButton(
                self.frame_tabela_pesq,
                text="Ver Detalhes",
                width=90,
                height=26,
                fg_color="gray30",
                hover_color="gray20",
                command=lambda p=processo: print(f"A abrir processo: {p}")
            )
            btn_ver.grid(row=row_idx, column=4, padx=10, pady=6, sticky="w")

    def filtrar_resultados(self):
        termo = self.entry_busca.get().lower().strip()
        status_sel = self.filtro_status.get()

        resultados = []
        for item in self.dados_base:
            processo, ficheiro, data, status = item

            corresponde_texto = (termo in processo.lower()) or (termo in ficheiro.lower())
            corresponde_status = (status_sel == "Todos os Status") or (status == status_sel)

            if corresponde_texto and corresponde_status:
                resultados.append(item)

        self.carregar_tabela_pesquisa(resultados)

    def __init__(self):
        super().__init__()

        self.title("Interface")
        self.geometry("1360x700")

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

        self.lbl_title = ctk.CTkLabel(
            self.tela_inicio,
            text="O que faremos hoje?",
            font=ctk.CTkFont("Helvetica", size=18, weight="bold"),
            text_color="#ebc075"
        )
        self.lbl_title.pack(anchor="w", pady=(0, 2))

        self.cards_frame = ctk.CTkFrame(self.tela_inicio, fg_color="transparent")
        self.cards_frame.pack(fill="x", pady=10)

        self.card1 = ctk.CTkFrame(self.cards_frame)
        self.card1.pack(side="left", expand=True, fill="both", padx=(0, 10))
        ctk.CTkLabel(self.card1, text="Total Processado", font=ctk.CTkFont(size=12), text_color="gray").pack(
            pady=(10, 0))
        ctk.CTkLabel(self.card1, text="1,248", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(0, 10))

        self.card2 = ctk.CTkFrame(self.cards_frame)
        self.card2.pack(side="left", expand=True, fill="both", padx=5)
        ctk.CTkLabel(self.card2, text="Consultas Hoje", font=ctk.CTkFont(size=12), text_color="gray").pack(pady=(10, 0))
        ctk.CTkLabel(self.card2, text="42", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(0, 10))

        self.card3 = ctk.CTkFrame(self.cards_frame)
        self.card3.pack(side="left", expand=True, fill="both", padx=(10, 0))
        ctk.CTkLabel(self.card3, text="Status do Banco", font=ctk.CTkFont(size=12), text_color="gray").pack(
            pady=(10, 0))
        ctk.CTkLabel(self.card3, text="● Conectado", font=ctk.CTkFont(size=16, weight="bold"),
                     text_color="#2ed573").pack(pady=(5, 10))

        table_frame = ctk.CTkFrame(self.tela_inicio)
        table_frame.pack(fill="both", expand=True, pady=(0, 10))

        table_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        headers = ["ID", "Operação", "Data / Hora", "Status"]
        for col_idx, text_header in enumerate(headers):
            lbl = ctk.CTkLabel(
                table_frame,
                text=text_header,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#ebc075"
            )
            lbl.grid(row=0, column=col_idx, padx=15, pady=10, sticky="w")

        dados_exemplo = [
            ("001", "Con1", "23/10/2026 14:20", "Concluído"),
            ("002", "Con2", "23/10/2026 15:05", "Concluído"),
            ("003", "Con3", "23/10/2026 16:10", "Pendente"),
        ]

        for row_idx, row_data in enumerate(dados_exemplo, start=1):
            for col_idx, value in enumerate(row_data):
                cor_status = "#2ed573" if value == "Concluído" else ("#ffbe76" if value == "Pendente" else "gray80")
                lbl = ctk.CTkLabel(
                    table_frame,
                    text=value,
                    text_color=cor_status if col_idx == 3 else "gray80"
                )
                lbl.grid(row=row_idx, column=col_idx, padx=15, pady=6, sticky="w")





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

        # Variáveis a serem subs
        n_processo = 1111
        valor_data = "1-1-1"
        total_pag = 120
        
        if n_processo :
            self.lbl_processo = ctk.CTkLabel(
                self.tela_process,
                text=f"N° de processo: {n_processo}",
                font=ctk.CTkFont("Helvetica", size=18, weight="bold")
            )
            self.lbl_processo.pack(anchor="w", pady=(20, 0))

        if valor_data:
            self.lbl_data = ctk.CTkLabel(
                self.tela_process,
                text=f"Data encontrada: {valor_data}",
                font=ctk.CTkFont("Helvetica", size=18, weight="bold")
            )
            self.lbl_data.pack(anchor="w", pady=(10, 0))

        if total_pag:
            self.lbl_pag = ctk.CTkLabel(
                self.tela_process,
                text=f"Total de páginas: {total_pag}",
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


        ## APENAS PARA TESTE
        self.dados_base = [
            ("2026.008492-1", "Contrato1.pdf", "23/10/2026", "Con"),
            ("2026.009110-4", "Contrato2", "22/10/2026", "Con"),
            ("2026.001239-0", "Contrato3.pdf", "21/10/2026", "Pndt"),
            ("2026.004551-8", "Contrato4.pdf", "20/10/2026", "Erro"),
        ]

        self.carregar_tabela_pesquisa(self.dados_base)




    def mudar_tela(self, nova_tela):

        if self.tela_atual is not None:
            self.tela_atual.grid_forget()

        self.tela_atual = nova_tela
        self.tela_atual.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)


if __name__ == "__main__":
    app = App()
    app.mainloop()