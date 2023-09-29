from view.base import *
from tkinter import *
from tkinter import messagebox
from database.bd import *


class Historico(TelaBaseFilha):
    def __init__(self, parent, usuario, tela_fechada, nome, widthinc, heightinc):
        super().__init__(parent, usuario, tela_fechada, nome, widthinc, heightinc)
        # ajustar o tamanho da tela largura x altura
        self.posicionar_tela(widht=700, height=500)
        # ajustar os tamanhos das colunas e linhas
        self.ajustar_colunas_linhas(25, 28)

        self.criar(Label, name='titulo', borderwidth=2, relief='groove', text="LISTA DO HISTÓRICO DE EVENTOS E FALHAS", font=self.fonteSubtitulo,
                   pady=10)
        self.instalar_em(name='titulo', row=1, column=1, rowspan=1, columnspan=20, sticky=tk.NSEW)

        self.criar(Label, name='filtro', borderwidth=2, relief='groove', text="LISTA:", font=self.fonte, pady=10)
        self.instalar_em(name='filtro', row=2, column=1, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar_lista('sb_filtro', 'lt_filtro', lista=bd_consultar("tipos_evento"),
                         row1=2, col_lb=2, colspan_lb=7, col_sb=2, colspan_sb=1)
        self.criar(Button, name='bt_atualizar', text="FILTRAR", command=self.atualizar_listar, fg="blue", font=self.fonte)
        self.instalar_em(name='bt_atualizar', row=2, column=9, rowspan=1, columnspan=1, sticky=tk.NSEW)

        self.criar(Button, name='bt_sair', text="SAIR", command=self.sair, fg="red", font=self.fonte)
        self.instalar_em(name='bt_sair', row=2, column=20, rowspan=1, columnspan=1, sticky=tk.NSEW)

        self.criar(Label, name='subtitulo', borderwidth=2, relief='groove', text="Data - Usuário - Descrição", font=self.fonte, pady=10)
        self.instalar_em(name='subtitulo', row=3, column=1, rowspan=1, columnspan=20, sticky=tk.NSEW)

        self.criar_lista('sb_io', 'lt_io', lista='',
                         row1=4, col_lb=1, colspan_lb=20, rowspan_lb=21, col_sb=21, colspan_sb=1, rowspan_sb=21)

    def atualizar_listar(self):
        # buscar o valor do filtro selecionado
        valor = self.item_selecionado(self.widgets['lt_filtro'])

        # verifica se um dos filtros foi selecionado
        if valor == '':
            tk.messagebox.showerror(title="Erro", message="Filtro não selecionado!")
        else:
            # limpar lista antiga
            self.widgets['lt_io'].delete(0, END)
            # gerar a lista do historico atualizada
            lista = bd_consulta_generica(sql_consultar_eventos_acao(valor))

            # Inserir valores atualizados
            for item in lista:
                self.widgets['lt_io'].insert(END, item[0])
