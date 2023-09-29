import tkinter as tk
from tkinter import *
from view.relogio import Relogio
from database.bd import bd_consultar_config_area, bd_registrar
from utils.times import get_now
from view.base import TelaBaseFilha


class Agenda(TelaBaseFilha):
    def __init__(self, parent, usuario, tela_fechada, area, nome, widthinc, heightinc):
        super().__init__(parent, usuario, tela_fechada, nome, widthinc, heightinc)
        self.nome = area
        self.area = bd_consultar_config_area(area)[0]
        # Tamanho da tela
        self.posicionar_tela(widht=500, height=200)

        # ajustar os tamanhos das colunas e linhas
        self.ajustar_colunas_linhas(16, 6)

        # Linha do Título
        self.criar(Label, name='titulo', borderwidth=2, relief='groove', text="CONFIGURAÇÕES", font=self.fonteTitulo, pady=10)
        self.instalar_em(name='titulo', row=0, column=0, rowspan=2, columnspan=16, sticky=tk.NSEW)

        # Linhas dos Botões
        self.criar(Label, name='tit_portoes', borderwidth=2, relief='groove', text="ÁREA", font=self.fonte, width=16)
        self.instalar_em(name='tit_portoes', row=2, column=0, columnspan=3, sticky=tk.NSEW)
        self.criar(Label, name='tit_ligar', borderwidth=2, relief='groove', text="LIGAR", font=self.fonte, width=16)
        self.instalar_em(name='tit_ligar', row=2, column=4, columnspan=3, sticky=tk.NSEW)
        self.criar(Label, name='tit_desligar', borderwidth=2, relief='groove', text="DESLIGAR", font=self.fonte, width=16)
        self.instalar_em(name='tit_desligar', row=2, column=8, columnspan=3, sticky=tk.NSEW)

        self.criar(Label, name='area_lbl', borderwidth=2, relief='groove', anchor='w', text=self.nome.upper(), font=self.fonte)
        self.instalar_em(name='area_lbl', row=3, column=0, columnspan=3, sticky=tk.NSEW)
        self.criar(Label, name='area_ligar', borderwidth=2, relief='groove', width=14)
        self.instalar_em(name='area_ligar', row=3, column=4, columnspan=2, sticky=tk.NSEW)
        self.criar(Button, name='bt_area_ligar', text="#", font=self.fonte, fg="green", command=lambda: self.relogio("area_ligar"))
        self.instalar_em(name='bt_area_ligar', row=3, column=6)

        self.criar(Label, name='area_desligar', borderwidth=2, relief='groove', width=14)
        self.instalar_em(name='area_desligar', row=3, column=8, columnspan=2, sticky=tk.NSEW)
        self.criar(Button, name='bt_area_desligar', text="#", font=self.fonte, fg="red", command=lambda: self.relogio("area_desligar"))
        self.instalar_em(name='bt_area_desligar', row=3, column=10)

        # BOTOES ATUALIZAR E SAIR
        self.criar(Button, name='bt_atualizar', text="ATUALIZAR", font=self.fonte, command=self.salvar_config, fg="green")
        self.instalar_em(name='bt_atualizar', row=5, column=4, sticky=tk.NSEW)
        self.criar(Button, name='bt_sair', text="SAIR", font=self.fonte, command=self.sair, fg="red")
        self.instalar_em(name='bt_sair', row=5, column=8, sticky=tk.NSEW)

        # Consultar e atualizar na tela os parametros
        self.consultar_config()

    def consultar_config(self):
        """Função que consulta no BD as informações da respectiva área"""
        self.alterar_parametro("area_ligar", text=self.area[2])
        self.alterar_parametro("area_desligar", text=self.area[3])

    def relogio(self, posicao):
        """Função que abre a tela relógio para alteração de horários"""
        tl_relogio = Relogio(self, self.usuario, self.tela_fechada, self.alterar_parametro, posicao, 'relogio', self.widthInc, self.heightInc)
        tl_relogio.grab_set()

    def salvar_config(self):
        """Função que salvar os horario"""
        # Coletar os valores
        ligar = self.widgets["area_ligar"].config("text")[4]
        desligar = self.widgets["area_desligar"].config("text")[4]

        # Registrar os valores
        bd_registrar("areas", "atualizar_config", [(ligar, desligar, self.area[1])])

        # # Atualiza os botões da tela salão de embarque
        # self.atualizar_bt()

        # Registrar a atualização na tabela evento
        bd_registrar('eventos', 'inserir_base', [(get_now(), self.usuario, "CONFIGURAÇÃO_AREA", "Alterado os horário do Salão de Embarque")])

        # Fechar a tela de configuração
        self.sair()
