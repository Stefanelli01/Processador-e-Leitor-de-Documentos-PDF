import customtkinter as ctk
from pathlib import Path
import app_pdf as appdf


arquivo_atual = Path(__file__).resolve()
pasta_raiz = arquivo_atual.parent

caminho_subpasta = pasta_raiz / "theme_ctk"
arquivo_alvo = caminho_subpasta / "theme.json"


ctk.set_appearance_mode("System")
ctk.set_default_color_theme(str(arquivo_alvo))



class App(ctk.CTk):

    def mostrar_inicio(self):
        self.mudar_tela(self.tela_inicio)

    def mostrar_processar(self):
        self.mudar_tela(self.tela_process)

    def mostrar_pesquisar(self):
        self.mudar_tela(self.tela_pesq)

    def __init__(self):
        super().__init__()

        self.title("Interface")
        self.geometry("1360x700")


        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)


        self.frame_menu = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.frame_menu.grid(row=0, column=0, sticky="nsew")

        self.label_menu = ctk.CTkLabel(self.frame_menu, text="MENU", font=ctk.CTkFont(size=20, weight="bold"))
        self.label_menu.pack(pady=20, padx=20)


        self.btn_ini = ctk.CTkButton(self.frame_menu, text="Inicio", command=self.mostrar_inicio)
        self.btn_ini.pack(pady=10, padx=20)

        self.btn_process = ctk.CTkButton(self.frame_menu, text="Processar", command=self.mostrar_processar)
        self.btn_process.pack(pady=10, padx=20)

        self.btn_pesq = ctk.CTkButton(self.frame_menu, text="Pesquisar", command=self.mostrar_pesquisar)
        self.btn_pesq.pack(pady=10, padx=20)


        self.tela_atual = None
        self.criar_telas()


        self.mostrar_inicio()



    def criar_telas(self):

        # Tela inicial
        self.tela_inicio = ctk.CTkFrame(self, fg_color="transparent")
        self.tela_inicio.grid_columnconfigure(0, weight=1)

        lbl_ini1 = ctk.CTkLabel(self.tela_inicio, text="Apenas para testes", font=("Helvetica", 14, "bold"))
        lbl_ini1.pack(pady=20, padx=20)

        # Tela processar
        self.tela_process = ctk.CTkFrame(self, fg_color="transparent")
        self.tela_process.grid_columnconfigure(0, weight=1)

        lbl_process1 = ctk.CTkLabel(self.tela_process, text="Apenas para testes", font=("Helvetica", 14, "bold"))
        lbl_process1.pack(pady=20, padx=20)

        # Tela pesquisar
        self.tela_pesq = ctk.CTkFrame(self, fg_color="transparent")
        self.tela_pesq.grid_columnconfigure(0, weight=1)

        lbl_pesq1 = ctk.CTkLabel(self.tela_pesq, text="Apenas para testes", font=("Helvetica", 14, "bold"))
        lbl_pesq1.pack(pady=20, padx=20)


    def mudar_tela(self, nova_tela):

        if self.tela_atual is not None:
            self.tela_atual.grid_forget()

        self.tela_atual = nova_tela
        self.tela_atual.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)


if __name__ == "__main__":
    app = App()
    app.mainloop()