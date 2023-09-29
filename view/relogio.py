import tkinter as tk
from tkinter import *
from view.base import TelaBaseFilha


class Relogio(TelaBaseFilha):
    def __init__(self, parent, usuario, tela_fechada, alterar_parametro, posicao, nome, widthinc, heightinc):
        super().__init__(parent, usuario, tela_fechada, nome, widthinc, heightinc)
        self.alterar_parametro = alterar_parametro
        self.posicao = posicao
        # Tamanho da tela
        self.posicionar_tela(widht=200, height=200)
        # ajustar os tamanhos das colunas e linhas
        self.ajustar_colunas_linhas(4, 4)

        # Linha do Título
        self.criar(Label, name='titulo', borderwidth=2, relief='groove', text="RELÓGIO", font=self.fonteTitulo, pady=10)
        self.instalar_em(name='titulo', row=0, column=0, rowspan=1, columnspan=4, sticky=tk.NSEW)
        self.criar(Label, name='st_hora', borderwidth=2, relief='groove', text="HORA", font=self.fonte, anchor='w')
        self.instalar_em(name='st_hora', row=1, column=0, rowspan=1, columnspan=2, sticky=tk.NSEW)
        self.criar(Label, name='st_minuto', borderwidth=2, relief='groove', text="MINUTO", font=self.fonte, anchor='w')
        self.instalar_em(name='st_minuto', row=1, column=2, rowspan=1, columnspan=2, sticky=tk.NSEW)

        # Horas
        self.criar_lista('sb_horas', 'ltb_horas', lista=list(range(24)),
                         row1=2, col_lb=0, colspan_lb=1, col_sb=1, colspan_sb=1, tipolista="numero")
        # Minutos
        self.criar_lista('sb_minutos', 'ltb_minutos', lista=list(range(60)),
                         row1=2, col_lb=2, colspan_lb=1, col_sb=3, colspan_sb=1, tipolista="numero")

        # Botões Salvar e Cancelar
        self.criar(Button, name='bt_salvar', text="Salvar", font=self.fonte, command=self.salvar, fg="green")
        self.instalar_em(name='bt_salvar', row=3, column=0, sticky=tk.NSEW)
        self.criar(Button, name='bt_cancelar', text="SAIR", font=self.fonte, command=self.sair, fg="red")
        self.instalar_em(name='bt_cancelar', row=3, column=2, sticky=tk.NSEW)

    def salvar(self):
        """Função para salvar na tela de configurações o horário selecionado"""
        # Verifica se foram selecionado a hora e o minuto
        if len(self.widgets['ltb_horas'].curselection()) > 0 and len(self.widgets['ltb_minutos'].curselection()) > 0:
            self.alterar_parametro(self.posicao, text=str("{:02d}".format(self.widgets['ltb_horas'].curselection()[0])) + ':' +
                                                      str("{:02d}".format(self.widgets['ltb_minutos'].curselection()[0])) + ':00')
            self.sair()
