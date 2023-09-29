from view.principal import Principal
from view.principal import inicializar_ciclos
from database.bd import verificar_banco
from tkinter import messagebox
import tkinter as tk

if __name__ == "__main__":
    # Inicializando o banco de dados

    if verificar_banco():
        app = Principal()
        inicializar_ciclos(app)
        app.mainloop()
    else:
        tk.messagebox.showerror(title="Erro", message="Erro ao iniciar o banco de dados")
