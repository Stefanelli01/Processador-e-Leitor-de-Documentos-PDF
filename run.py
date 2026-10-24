from src.gui.app import App
from tkinter import messagebox

try:
    if __name__ == "__main__":
        app = App()
        app.mainloop()

except Exception as e:
    messagebox.showerror("Erro durante a inicialização", f"Falha ao iniciar o sistema:\n{e}")