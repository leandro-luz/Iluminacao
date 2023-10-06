from tkinter import *
from view.relogio import Relogio, DiaSemana
from view.base import TelaBaseFilha
from database.bd import *


class Agenda(TelaBaseFilha):
    def __init__(self, parent, usuario, tela_fechada, area, nome, widthinc, heightinc):
        super().__init__(parent, usuario, tela_fechada, nome, widthinc, heightinc)
        self.nome = area
        self.area = bd_consultar_config_area(area)[0]
        # Tamanho da tela
        self.posicionar_tela(widht=700, height=250)

        # ajustar os tamanhos das colunas e linhas
        self.ajustar_colunas_linhas(16, 6)

        # Linha do Título
        self.criar(Label, name='titulo', borderwidth=2, relief='groove', text="PROGRAMAÇÃO DIA/HORÁRIO", font=self.fonteTitulo, pady=10)
        self.instalar_em(name='titulo', row=0, column=0, rowspan=2, columnspan=16, sticky=tk.NSEW)

        # Linhas dos Botões
        self.criar(Label, name='tit_area', borderwidth=2, relief='groove', text="ÁREA", font=self.fonte, width=16)
        self.instalar_em(name='tit_area', row=2, column=0, columnspan=3, sticky=tk.NSEW)
        self.criar(Label, name='tit_ligar', borderwidth=2, relief='groove', text="HORA LIGAR", font=self.fonte, width=16)
        self.instalar_em(name='tit_ligar', row=2, column=4, columnspan=3, sticky=tk.NSEW)
        self.criar(Label, name='tit_desligar', borderwidth=2, relief='groove', text="HORA DESLIGAR", font=self.fonte, width=16)
        self.instalar_em(name='tit_desligar', row=2, column=8, columnspan=3, sticky=tk.NSEW)
        self.criar(Label, name='tit_dias', borderwidth=2, relief='groove', text="DIAS", font=self.fonte, width=16)
        self.instalar_em(name='tit_dias', row=2, column=12, columnspan=4, sticky=tk.NSEW)

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

        self.criar(Label, name='dias', borderwidth=2, relief='groove', width=14)
        self.instalar_em(name='dias', row=3, column=12, columnspan=3, sticky=tk.NSEW)
        self.criar(Button, name='bt_dias', text="#", font=self.fonte, fg="blue", command=lambda: self.dia_semana("dias"))
        self.instalar_em(name='bt_dias', row=3, column=15)

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
        self.alterar_parametro("dias", text=bd_consulta_valor_tabela('dias_semana', 'dia_semana_id', self.area[10])[0][1])

    def relogio(self, posicao):
        """Função que abre a tela relógio para alteração de horários"""
        self.ajustar_posicao_tela()
        tl_relogio = Relogio(self, self.usuario, self.tela_fechada, self.alterar_parametro, posicao, 'relogio', self.widthInc, self.heightInc)
        tl_relogio.grab_set()

    def dia_semana(self, posicao):
        """Função que abre a tela DiaSemana para alteração dos dias de semana que deve ser acionado"""
        self.ajustar_posicao_tela()
        tl_diasemana = DiaSemana(self, self.usuario, self.tela_fechada, self.alterar_parametro, posicao, 'dia', self.widthInc, self.heightInc)
        tl_diasemana.grab_set()

    def salvar_config(self):
        """Função que salvar os horario"""
        # Coletar os valores
        ligar = self.widgets["area_ligar"].config("text")[4]
        desligar = self.widgets["area_desligar"].config("text")[4]
        dias = bd_consulta_valor_tabela('dias_semana', 'nome', self.widgets["dias"].config("text")[4])[0][0]

        # Registrar os valores
        bd_registrar("areas", "atualizar_config", [(ligar, desligar, dias, self.area[1])])

        # Registrar a atualização na tabela evento
        bd_registrar('eventos', 'inserir_base', [(get_now(), self.usuario, "CONFIGURAÇÃO_AREA", "Alterado os horário do Salão de Embarque")])

        # Fechar a tela de configuração
        self.sair()
