import time
import uuid
from threading import *
from datetime import datetime, timedelta
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from view.login import Login
from view.usuario import CadastrarUsuario, AlterarUsuario, ListarUsuario
from view.comunicacao import CadastrarClp, AlterarClp, ListarClp, CadastrarIO, ListarIO, AlterarIO
from view.config_sistema import AlterarConfigSistema
from view.historico import Historico
from view.agenda import Agenda
from database.bd import *
from database.sql import sql_consultar_clp_areas
from utils.conexao import ler_clp, escrever_clp
from utils.times import get_now

# Variavel global
threads = True


class TelaVazia:
    """Classe de tela vazia"""
    status = False
    nome = 'telavazia'

    def verificar_tela_aberta(self):
        pass

    def sair(self):
        pass


class Principal(tk.Tk):
    """Classe para montagem da tela principal"""

    def __init__(self):
        super().__init__()
        self.carregar_variaveis()

    def carregar_variaveis(self):
        # self.nome = 'teste123'
        self.versao = "ELT.004 - 06/10/2023"
        self.usuario = ""
        self.cliquebotao = datetime.now()
        self.acessado = False
        self.tela = TelaVazia()
        self.tempoacessado = ""
        # Tamanho da tela
        self.widthInc = 0
        self.heightInc = 0
        self.posicionar_tela(widht=800, height=400)

        # Permissão para redimensionamento pelo usuário
        self.resizable(False, False)
        # Titulo na aba
        self.title('ASGA')
        # Configuração o sair do windows
        self.protocol("WM_DELETE_WINDOW", self.sair)

        if self.winfo_screenwidth() > 1500:
            # Configurações de texto
            self.fonte = ("Verdana", "14")
            self.fonteSubtitulo = ("Verdana", "18", "bold")
            self.fonteTitulo = ("Verdana", "25", "bold")
            self.tamanho_imagens = 75
            self.tamanho_imagens_legenda = 50
        else:
            # Configurações de texto
            self.fonte = ("Verdana", "10")
            self.fonteSubtitulo = ("Verdana", "12", "bold")
            self.fonteTitulo = ("Verdana", "18", "bold")
            self.tamanho_imagens = 50
            self.tamanho_imagens_legenda = 25

        # consultar valor de tela aberta no BD
        valor = bd_consultar("sistema")[0]
        self.tempoacessado = datetime.now() + timedelta(minutes=valor[2])

        # Lista de ferramentas na tela
        self.__widgets = {}

        self.inserir_menu()

        # Padronização dos tamanhos das colunas e linhas
        for i in range(11):
            self.columnconfigure(i, weight=1)
        for i in range(30):
            self.rowconfigure(i, weight=1)

        # Carregamento das imagens
        # Imagens dos botões
        self.img_alarme = ''
        self.img_automatico = ''
        self.img_manual = ''
        self.img_local = ''
        self.img_remoto = ''
        self.img_desligado = ''
        self.img_ligado_completo = ''
        self.img_ligado_parcial = ''
        self.img_desconectado = ''
        self.carregar_imagens('img_', self.tamanho_imagens, self.tamanho_imagens)

        self.img2_automatico = ''
        self.img2_manual = ''
        self.img2_local = ''
        self.img2_remoto = ''
        self.carregar_imagens('img2_', self.tamanho_imagens, self.tamanho_imagens)

        # Imagens da legenda
        self.img_lg_alarme = ''
        self.img_lg_automatico = ''
        self.img_lg_manual = ''
        self.img_lg_local = ''
        self.img_lg_remoto = ''
        self.img_lg_desligado = ''
        self.img_lg_ligado_completo = ''
        self.img_lg_ligado_parcial = ''
        self.img_lg_desconectado = ''
        self.img_lg_local = ''
        self.carregar_imagens('img_lg_', self.tamanho_imagens_legenda, self.tamanho_imagens_legenda)

        # montar a tela
        self.montar_tela()
        self.ativar_desativar_botoes(ativar=False)

        # Registro de inicio do sistema
        bd_registrar('eventos', 'inserir_base', [(get_now(), "Null", "ACESSO", "Sistema de Controle e Monitoramente de Iluminação INICIADO")])

    def montar_tela(self):
        # Linha do Título
        self.criar(Label, name='titulo', borderwidth=2, relief='groove', text="CONTROLE E MONITORAMENTO - ILUMINAÇÃO", font=self.fonteTitulo, pady=10)
        self.instalar_em(name='titulo', row=0, column=0, rowspan=2, columnspan=13, sticky=tk.NSEW)

        # Linha de usuário, senha, login e data sistema
        self.criar(Label, name='usuario_lbl', borderwidth=2, relief='groove', text="Usuário:", font=self.fonte, anchor="e")
        self.instalar_em(name='usuario_lbl', row=2, column=0, rowspan=3, columnspan=1, sticky=tk.NSEW)

        self.criar(Label, name='usuario_nome', borderwidth=2, relief='groove', text=self.usuario, font=self.fonte, anchor="w")
        self.instalar_em(name='usuario_nome', row=2, column=1, rowspan=3, columnspan=3, sticky=tk.NSEW)

        self.criar(Label, name='time', borderwidth=2, relief='groove', text="data - hora", font=self.fonte)
        self.instalar_em(name='time', row=2, column=6, rowspan=3, columnspan=2, sticky=tk.NSEW)

        self.criar(Button, name='bt_login', text="LOGIN", font=self.fonte, command=lambda: self.login_user("login"))
        self.instalar_em(name='bt_login', row=2, column=8, rowspan=3, columnspan=2, sticky=tk.NSEW)

        # Linhas dos Botões
        # SALÃO EMBARQUE INTERNACIONAL LINHA 4 COLUNA 1
        self.criar(Button, name='bt_salao_embarque_internacional', text="SALÃO DE EMBARQUE \n INTERNACIONAL", font=self.fonteSubtitulo,
                   command=lambda: thread_operar(self, "salao_embarque_internacional"))
        self.instalar_em(name='bt_salao_embarque_internacional', row=5, column=0, rowspan=2, columnspan=1, sticky=tk.NSEW)
        self.criar_com_imagem(Button, name='img_modo_salao_embarque_internacional', render=self.img2_manual, image=self.img2_manual,
                              borderwidth=2, relief='groove', command=lambda: self.operacao_manual("salao_embarque_internacional"))
        self.instalar_em(name='img_modo_salao_embarque_internacional', row=5, column=1, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar_com_imagem(Button, name='img_controle_salao_embarque_internacional', render=self.img2_local, image=self.img2_local,
                              borderwidth=2, relief='groove', command=lambda: self.operacao_local("salao_embarque_internacional"))
        self.instalar_em(name='img_controle_salao_embarque_internacional', row=6, column=1, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar_com_imagem(Label, name='img_salao_embarque_internacional', render=self.img_desconectado, image=self.img_desconectado,
                              borderwidth=2,
                              relief='groove')
        self.instalar_em(name='img_salao_embarque_internacional', row=5, column=2, rowspan=2, columnspan=2, sticky=tk.NSEW)

        self.criar(Button, name='bt_configuracao_salao_embarque_internacional', text="#", font=self.fonteSubtitulo,
                   command=lambda: self.agenda("salao_embarque_internacional"))
        self.instalar_em(name='bt_configuracao_salao_embarque_internacional', row=5, column=2, rowspan=1, columnspan=1, sticky=tk.NW)

        # SAGUÃO DE EMBARQUE LINHA 4 COLUNA 7
        self.criar(Button, name='bt_saguao_embarque', text="SAGUÃO DE EMBARQUE", font=self.fonteSubtitulo,
                   command=lambda: thread_operar(self, "saguao_embarque"))
        self.instalar_em(name='bt_saguao_embarque', row=5, column=6, rowspan=2, columnspan=1, sticky=tk.NSEW)
        self.criar_com_imagem(Button, name='img_modo_saguao_embarque', render=self.img2_manual, image=self.img2_manual, borderwidth=2,
                              relief='groove', command=lambda: self.operacao_manual("saguao_embarque"))
        self.instalar_em(name='img_modo_saguao_embarque', row=5, column=7, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar_com_imagem(Button, name='img_controle_saguao_embarque', render=self.img2_local, image=self.img2_local, borderwidth=2,
                              relief='groove', command=lambda: self.operacao_local("saguao_embarque"))
        self.instalar_em(name='img_controle_saguao_embarque', row=6, column=7, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar_com_imagem(Label, name='img_saguao_embarque', render=self.img_desconectado, image=self.img_desconectado, borderwidth=2,
                              relief='groove')
        self.instalar_em(name='img_saguao_embarque', row=5, column=8, rowspan=2, columnspan=2, sticky=tk.NSEW)
        self.criar(Button, name='bt_configuracao_saguao_embarque', text="#", font=self.fonteSubtitulo,
                   command=lambda: self.agenda("saguao_embarque"))
        self.instalar_em(name='bt_configuracao_saguao_embarque', row=5, column=8, rowspan=1, columnspan=1, sticky=tk.NW)

        # SALÃO EMBARQUE DOMESTICO LINHA 7 COLUNA 1
        self.criar(Button, name='bt_salao_embarque_domestico', text="SALÃO DE EMBARQUE \n DOMÉSTICO", font=self.fonteSubtitulo,
                   command=lambda: thread_operar(self, "salao_embarque_domestico"))
        self.instalar_em(name='bt_salao_embarque_domestico', row=8, column=0, rowspan=2, columnspan=1, sticky=tk.NSEW)
        self.criar_com_imagem(Button, name='img_modo_salao_embarque_domestico', render=self.img2_manual, image=self.img2_manual,
                              borderwidth=2, relief='groove', command=lambda: self.operacao_manual("salao_embarque_domestico"))
        self.instalar_em(name='img_modo_salao_embarque_domestico', row=8, column=1, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar_com_imagem(Button, name='img_controle_salao_embarque_domestico', render=self.img2_local, image=self.img2_local,
                              borderwidth=2, relief='groove', command=lambda: self.operacao_local("salao_embarque_domestico"))
        self.instalar_em(name='img_controle_salao_embarque_domestico', row=9, column=1, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar_com_imagem(Label, name='img_salao_embarque_domestico', render=self.img_desconectado, image=self.img_desconectado, borderwidth=2,
                              relief='groove')
        self.instalar_em(name='img_salao_embarque_domestico', row=8, column=2, rowspan=2, columnspan=2, sticky=tk.NSEW)
        self.criar(Button, name='bt_configuracao_salao_embarque_domestico', text="#", font=self.fonteSubtitulo,
                   command=lambda: self.agenda("salao_embarque_domestico"))
        self.instalar_em(name='bt_configuracao_salao_embarque_domestico', row=8, column=2, rowspan=1, columnspan=1, sticky=tk.NW)

        # MEZANINO LINHA 7 COLUNA 7
        self.criar(Button, name='bt_mezanino', text="MEZANINO", font=self.fonteSubtitulo,
                   command=lambda: thread_operar(self, "mezanino"))
        self.instalar_em(name='bt_mezanino', row=8, column=6, rowspan=2, columnspan=1, sticky=tk.NSEW)
        self.criar_com_imagem(Button, name='img_modo_mezanino', render=self.img2_manual, image=self.img2_manual, borderwidth=2,
                              relief='groove', command=lambda: self.operacao_manual("mezanino"))
        self.instalar_em(name='img_modo_mezanino', row=8, column=7, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar_com_imagem(Button, name='img_controle_mezanino', render=self.img2_local, image=self.img2_local, borderwidth=2,
                              relief='groove', command=lambda: self.operacao_local("mezanino"))
        self.instalar_em(name='img_controle_mezanino', row=9, column=7, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar_com_imagem(Label, name='img_mezanino', render=self.img_desconectado, image=self.img_desconectado, borderwidth=2, relief='groove')
        self.instalar_em(name='img_mezanino', row=8, column=8, rowspan=2, columnspan=2, sticky=tk.NSEW)
        self.criar(Button, name='bt_configuracao_mezanino', text="#", font=self.fonteSubtitulo,
                   command=lambda: self.agenda("mezanino"))
        self.instalar_em(name='bt_configuracao_mezanino', row=8, column=8, rowspan=1, columnspan=1, sticky=tk.NW)

        # CONECTORES LINHA 10 COLUNA 1
        self.criar(Button, name='bt_conectores', text="CONECTORES", font=self.fonteSubtitulo,
                   command=lambda: thread_operar(self, "conectores"))
        self.instalar_em(name='bt_conectores', row=11, column=0, rowspan=2, columnspan=1, sticky=tk.NSEW)
        self.criar_com_imagem(Button, name='img_modo_conectores', render=self.img2_manual, image=self.img2_manual, borderwidth=2,
                              relief='groove', command=lambda: self.operacao_manual("conectores"))
        self.instalar_em(name='img_modo_conectores', row=11, column=1, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar_com_imagem(Button, name='img_controle_conectores', render=self.img2_local, image=self.img2_local, borderwidth=2,
                              relief='groove', command=lambda: self.operacao_local("conectores"))
        self.instalar_em(name='img_controle_conectores', row=12, column=1, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar_com_imagem(Label, name='img_conectores', render=self.img_desconectado, image=self.img_desconectado, borderwidth=2, relief='groove')
        self.instalar_em(name='img_conectores', row=11, column=2, rowspan=2, columnspan=2, sticky=tk.NSEW)
        self.criar(Button, name='bt_configuracao_conectores', text="#", font=self.fonteSubtitulo, command=lambda: self.agenda("conectores"))
        self.instalar_em(name='bt_configuracao_conectores', row=11, column=2, rowspan=1, columnspan=1, sticky=tk.NW)

        # SAGUÃO DE DESEMBARQUE LINHA 10 COLUNA 7
        self.criar(Button, name='bt_saguao_desembarque', text="SAGUÃO DE DESEMBARQUE", font=self.fonteSubtitulo,
                   command=lambda: thread_operar(self, "saguao_desembarque"))
        self.instalar_em(name='bt_saguao_desembarque', row=11, column=6, rowspan=2, columnspan=1, sticky=tk.NSEW)
        self.criar_com_imagem(Button, name='img_modo_saguao_desembarque', render=self.img2_manual, image=self.img2_manual, borderwidth=2,
                              relief='groove', command=lambda: self.operacao_manual("saguao_desembarque"))
        self.instalar_em(name='img_modo_saguao_desembarque', row=11, column=7, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar_com_imagem(Button, name='img_controle_saguao_desembarque', render=self.img2_local, image=self.img2_local, borderwidth=2,
                              relief='groove', command=lambda: self.operacao_local("saguao_desembarque"))
        self.instalar_em(name='img_controle_saguao_desembarque', row=12, column=7, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar_com_imagem(Label, name='img_saguao_desembarque', render=self.img_desconectado, image=self.img_desconectado, borderwidth=2,
                              relief='groove')
        self.instalar_em(name='img_saguao_desembarque', row=11, column=8, rowspan=2, columnspan=2, sticky=tk.NSEW)
        self.criar(Button, name='bt_configuracao_saguao_desembarque', text="#", font=self.fonteSubtitulo,
                   command=lambda: self.agenda("saguao_desembarque"))
        self.instalar_em(name='bt_configuracao_saguao_desembarque', row=11, column=8, rowspan=1, columnspan=1, sticky=tk.NW)

        # SALÃO DESEMBARQUE INTERNACIONAL LINHA 13 COLUNA 1
        self.criar(Button, name='bt_salao_desembarque_internacional', text="SALÃO DE DESEMBARQUE \n INTERNACIONAL", font=self.fonteSubtitulo,
                   command=lambda: thread_operar(self, "salao_desembarque_internacional"))
        self.instalar_em(name='bt_salao_desembarque_internacional', row=14, column=0, rowspan=2, columnspan=1, sticky=tk.NSEW)
        self.criar_com_imagem(Button, name='img_modo_salao_desembarque_internacional', render=self.img2_manual, image=self.img2_manual,
                              borderwidth=2, relief='groove', command=lambda: self.operacao_manual("salao_desembarque_internacional"))
        self.instalar_em(name='img_modo_salao_desembarque_internacional', row=14, column=1, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar_com_imagem(Button, name='img_controle_salao_desembarque_internacional', render=self.img2_local, image=self.img2_local,
                              borderwidth=2, relief='groove', command=lambda: self.operacao_local("salao_desembarque_internacional"))
        self.instalar_em(name='img_controle_salao_desembarque_internacional', row=15, column=1, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar_com_imagem(Label, name='img_salao_desembarque_internacional', render=self.img_desconectado, image=self.img_desconectado,
                              borderwidth=2,
                              relief='groove')
        self.instalar_em(name='img_salao_desembarque_internacional', row=14, column=2, rowspan=2, columnspan=2, sticky=tk.NSEW)
        self.criar(Button, name='bt_configuracao_salao_desembarque_internacional', text="#", font=self.fonteSubtitulo,
                   command=lambda: self.agenda("salao_desembarque_internacional"))
        self.instalar_em(name='bt_configuracao_salao_desembarque_internacional', row=14, column=2, rowspan=1, columnspan=1, sticky=tk.NW)

        # VIADUTO LINHA 13 COLUNA 7
        self.criar(Button, name='bt_viaduto_superior', text="VIADUTO SUPERIOR", font=self.fonteSubtitulo,
                   command=lambda: thread_operar(self, "viaduto_superior"))
        self.instalar_em(name='bt_viaduto_superior', row=14, column=6, rowspan=2, columnspan=1, sticky=tk.NSEW)
        self.criar_com_imagem(Button, name='img_modo_viaduto_superior', render=self.img2_manual, image=self.img2_manual, borderwidth=2,
                              relief='groove', command=lambda: self.operacao_manual("viaduto_superior"))
        self.instalar_em(name='img_modo_viaduto_superior', row=14, column=7, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar_com_imagem(Button, name='img_controle_viaduto_superior', render=self.img2_local, image=self.img2_local, borderwidth=2,
                              relief='groove', command=lambda: self.operacao_local("viaduto_superior"))
        self.instalar_em(name='img_controle_viaduto_superior', row=15, column=7, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar_com_imagem(Label, name='img_viaduto_superior', render=self.img_desconectado, image=self.img_desconectado, borderwidth=2,
                              relief='groove')
        self.instalar_em(name='img_viaduto_superior', row=14, column=8, rowspan=2, columnspan=2, sticky=tk.NSEW)
        self.criar(Button, name='bt_configuracao_viaduto_superior', text="#", font=self.fonteSubtitulo,
                   command=lambda: self.agenda("viaduto_superior"))
        self.instalar_em(name='bt_configuracao_viaduto_superior', row=14, column=8, rowspan=1, columnspan=1, sticky=tk.NW)

        # SALÃO DESEMBARQUE DOMESTICO LINHA 16 COLUNA 1
        self.criar(Button, name='bt_salao_desembarque_domestico', text="SALÃO DE DESEMBARQUE \n DOMÉSTICO", font=self.fonteSubtitulo,
                   command=lambda: thread_operar(self, "salao_desembarque_domestico"))
        self.instalar_em(name='bt_salao_desembarque_domestico', row=17, column=0, rowspan=2, columnspan=1, sticky=tk.NSEW)
        self.criar_com_imagem(Button, name='img_modo_salao_desembarque_domestico', render=self.img2_manual, image=self.img2_manual,
                              borderwidth=2, relief='groove', command=lambda: self.operacao_manual("salao_desembarque_domestico"))
        self.instalar_em(name='img_modo_salao_desembarque_domestico', row=17, column=1, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar_com_imagem(Button, name='img_controle_salao_desembarque_domestico', render=self.img2_local, image=self.img2_local,
                              borderwidth=2, relief='groove', command=lambda: self.operacao_local("salao_desembarque_domestico"))
        self.instalar_em(name='img_controle_salao_desembarque_domestico', row=18, column=1, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar_com_imagem(Label, name='img_salao_desembarque_domestico', render=self.img_desconectado, image=self.img_desconectado, borderwidth=2,
                              relief='groove')
        self.instalar_em(name='img_salao_desembarque_domestico', row=17, column=2, rowspan=2, columnspan=2, sticky=tk.NSEW)
        self.criar(Button, name='bt_configuracao_salao_desembarque_domestico', text="#", font=self.fonteSubtitulo,
                   command=lambda: self.agenda("salao_desembarque_domestico"))
        self.instalar_em(name='bt_configuracao_salao_desembarque_domestico', row=17, column=2, rowspan=1, columnspan=1, sticky=tk.NW)

        # VIADUTO LINHA 16 COLUNA 7
        self.criar(Button, name='bt_viaduto_inferior', text="VIADUTO INFERIOR", font=self.fonteSubtitulo,
                   command=lambda: thread_operar(self, "viaduto_inferior"))
        self.instalar_em(name='bt_viaduto_inferior', row=17, column=6, rowspan=2, columnspan=1, sticky=tk.NSEW)
        self.criar_com_imagem(Button, name='img_modo_viaduto_inferior', render=self.img2_manual, image=self.img2_manual, borderwidth=2,
                              relief='groove', command=lambda: self.operacao_manual("viaduto_inferior"))
        self.instalar_em(name='img_modo_viaduto_inferior', row=17, column=7, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar_com_imagem(Button, name='img_controle_viaduto_inferior', render=self.img2_local, image=self.img2_local, borderwidth=2,
                              relief='groove', command=lambda: self.operacao_local("viaduto_inferior"))
        self.instalar_em(name='img_controle_viaduto_inferior', row=18, column=7, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar_com_imagem(Label, name='img_viaduto_inferior', render=self.img_desconectado, image=self.img_desconectado, borderwidth=2,
                              relief='groove')
        self.instalar_em(name='img_viaduto_inferior', row=17, column=8, rowspan=2, columnspan=2, sticky=tk.NSEW)
        self.criar(Button, name='bt_configuracao_viaduto_inferior', text="#", font=self.fonteSubtitulo,
                   command=lambda: self.agenda("viaduto_inferior"))
        self.instalar_em(name='bt_configuracao_viaduto_inferior', row=17, column=8, rowspan=1, columnspan=1, sticky=tk.NW)

        # # Legenda
        self.criar(Label, name='lb_legenda', borderwidth=2, relief='groove', text="LEGENDA:", anchor="c", font=self.fonte)
        self.instalar_em(name='lb_legenda', row=2, rowspan=3, column=11, columnspan=2, sticky=tk.NSEW)

        self.criar(Label, name='lb_lg_ligado', borderwidth=2, relief='groove', text="Ligado Total", anchor="e", font=self.fonte)
        self.instalar_em(name='lb_lg_ligado', row=5, column=11, columnspan=1, sticky=tk.NSEW)
        self.criar_com_imagem(Label, name='img_lg_ligado', text="Ligado Completo", render=self.img_lg_ligado_completo,
                              image=self.img_lg_ligado_completo, borderwidth=2, relief='groove')
        self.instalar_em(name='img_lg_ligado', row=5, column=12, rowspan=1, columnspan=1, sticky=tk.NSEW)

        self.criar(Label, name='lb_lg_parcial', borderwidth=2, relief='groove', text="Ligado Parcial", anchor="e", font=self.fonte)
        self.instalar_em(name='lb_lg_parcial', row=6, column=11, columnspan=1, sticky=tk.NSEW)
        self.criar_com_imagem(Label, name='img_lg_parcial', text="Ligado Parcial", render=self.img_lg_ligado_parcial,
                              image=self.img_lg_ligado_parcial, borderwidth=2, relief='groove')
        self.instalar_em(name='img_lg_parcial', row=6, column=12, rowspan=1, columnspan=1, sticky=tk.NSEW)

        self.criar(Label, name='lb_lg_desligado', borderwidth=2, relief='groove', text="Desligado", anchor="e", font=self.fonte)
        self.instalar_em(name='lb_lg_desligado', row=8, column=11, columnspan=1, sticky=tk.NSEW)
        self.criar_com_imagem(Label, name='img_lg_desligado', text="Desligado", render=self.img_lg_desligado,
                              image=self.img_lg_desligado, borderwidth=2, relief='groove')
        self.instalar_em(name='img_lg_desligado', row=8, column=12, rowspan=1, columnspan=1, sticky=tk.NSEW)

        self.criar(Label, name='lb_lg_alarme', borderwidth=2, relief='groove', text="Alarme", anchor="e", font=self.fonte)
        self.instalar_em(name='lb_lg_alarme', row=9, column=11, columnspan=1, sticky=tk.NSEW)
        self.criar_com_imagem(Label, name='img_lg_alarme', text="Alarme", render=self.img_lg_alarme,
                              image=self.img_lg_alarme, borderwidth=2, relief='groove')
        self.instalar_em(name='img_lg_alarme', row=9, column=12, rowspan=1, columnspan=1, sticky=tk.NSEW)

        self.criar(Label, name='lb_lg_desconectado', borderwidth=2, relief='groove', text="Desconectado", anchor="e", font=self.fonte)
        self.instalar_em(name='lb_lg_desconectado', row=11, column=11, columnspan=1, sticky=tk.NSEW)
        self.criar_com_imagem(Label, name='img_lg_desconectado', text="Desconectado", render=self.img_lg_desconectado,
                              image=self.img_lg_desconectado, borderwidth=2, relief='groove')
        self.instalar_em(name='img_lg_desconectado', row=11, column=12, rowspan=1, columnspan=1, sticky=tk.NSEW)

        self.criar(Label, name='lb_lg_automatico', borderwidth=2, relief='groove', text="Automático", anchor="e", font=self.fonte)
        self.instalar_em(name='lb_lg_automatico', row=12, column=11, columnspan=1, sticky=tk.NSEW)
        self.criar_com_imagem(Label, name='img_lg_automatico', text="Automático", render=self.img_lg_automatico,
                              image=self.img_lg_automatico, borderwidth=2, relief='groove')
        self.instalar_em(name='img_lg_automatico', row=12, column=12, rowspan=1, columnspan=1, sticky=tk.NSEW)

        self.criar(Label, name='lb_lg_manual', borderwidth=2, relief='groove', text="Manual", anchor="e", font=self.fonte)
        self.instalar_em(name='lb_lg_manual', row=14, column=11, columnspan=1, sticky=tk.NSEW)
        self.criar_com_imagem(Label, name='img_lg_manual', text="Manual", render=self.img_lg_manual,
                              image=self.img_lg_manual, borderwidth=2, relief='groove')
        self.instalar_em(name='img_lg_manual', row=14, column=12, rowspan=1, columnspan=1, sticky=tk.NSEW)

        self.criar(Label, name='lb_lg_local', borderwidth=2, relief='groove', text="Modo Local", anchor="e", font=self.fonte)
        self.instalar_em(name='lb_lg_local', row=15, column=11, columnspan=1, sticky=tk.NSEW)
        self.criar_com_imagem(Label, name='img_lg_local', text="Modo Local", render=self.img_lg_local,
                              image=self.img_lg_local, borderwidth=2, relief='groove')
        self.instalar_em(name='img_lg_local', row=15, column=12, rowspan=1, columnspan=1, sticky=tk.NSEW)

        self.criar(Label, name='lb_lg_remoto', borderwidth=2, relief='groove', text="Modo Remoto", anchor="e", font=self.fonte)
        self.instalar_em(name='lb_lg_remoto', row=17, column=11, columnspan=1, sticky=tk.NSEW)
        self.criar_com_imagem(Label, name='img_lg_remoto', text="Modo Remoto", render=self.img_lg_remoto,
                              image=self.img_lg_remoto, borderwidth=2, relief='groove')
        self.instalar_em(name='img_lg_remoto', row=17, column=12, rowspan=1, columnspan=1, sticky=tk.NSEW)

        self.criar(Label, name='lb_falhas', borderwidth=2, relief='groove', text="Total Falhas:", anchor="e", font=self.fonte)
        self.instalar_em(name='lb_falhas', row=18, column=11, columnspan=1, sticky=tk.NSEW)
        self.criar(Label, name='lb_falhas_total', borderwidth=2, relief='groove', text="0", anchor="e", font=self.fonte)
        self.instalar_em(name='lb_falhas_total', row=18, column=12, columnspan=1, sticky=tk.NSEW)

        self.criar(Label, name='lb_versao', borderwidth=2, relief='groove', text=self.versao, anchor="w", font=self.fonte)
        self.instalar_em(name='lb_versao', row=19, column=0, columnspan=1, sticky=tk.NSEW)

    def inserir_menu(self):
        """Função para criar o menu"""
        self.menubar = Menu(self, font=self.fonte)

        user_menu = Menu(self.menubar, tearoff=0, font=self.fonte)
        user_menu.add_command(label="Adicionar", command=lambda: self.crud("cadastrar", "usuario"), font=self.fonte)
        user_menu.add_command(label="Alterar", command=lambda: self.crud("alterar", "usuario"), font=self.fonte)
        user_menu.add_command(label="Listar", command=lambda: self.crud("listar", "usuario"), font=self.fonte)
        self.menubar.add_cascade(label="Usuário", menu=user_menu, font=self.fonte)
        self.menubar.entryconfig("Usuário", state='disabled', font=self.fonte)

        comm_menu = Menu(self, tearoff=0, font=self.fonte)
        comm_menu.add_command(label="Adicionar", command=lambda: self.crud("cadastrar", "clp"), font=self.fonte)
        comm_menu.add_command(label="Alterar", command=lambda: self.crud("alterar", "clp"), font=self.fonte)
        comm_menu.add_command(label="Listar", command=lambda: self.crud("listar", "clp"), font=self.fonte)

        io_menu = Menu(self, tearoff=0, font=self.fonte)
        io_menu.add_command(label="Adicionar", command=lambda: self.crud("cadastrar", "io"), font=self.fonte)
        io_menu.add_command(label="Alterar", command=lambda: self.crud("alterar", "io"), font=self.fonte)
        io_menu.add_command(label="Listar", command=lambda: self.crud("listar", "io"), font=self.fonte)

        clp_menu = Menu(self, tearoff=0, font=self.fonte)
        self.menubar.add_cascade(label="Comunicação", menu=clp_menu, font=self.fonte)
        self.menubar.entryconfig("Comunicação", state='disabled')

        clp_menu.add_cascade(label="CLP", menu=comm_menu, font=self.fonte)
        clp_menu.add_cascade(label="Entradas/Saídas", menu=io_menu, font=self.fonte)

        sistema_menu = Menu(self, tearoff=0, font=self.fonte)
        sistema_menu.add_command(label="Alterar", command=lambda: self.crud("sistema", 'sistema'), font=self.fonte)
        sistema_menu.add_command(label="Habilitar_PC", command=self.habilitar_computador, font=self.fonte)
        self.menubar.add_cascade(label="Sistema", menu=sistema_menu, font=self.fonte)
        self.menubar.entryconfig("Sistema", state='disabled')

        historico_menu = Menu(self, tearoff=0, font=self.fonte)
        historico_menu.add_command(label="Listar", command=lambda: self.crud("historico", 'historico'), font=self.fonte)
        historico_menu.add_command(label="Excluir_Falhas", command=self.excluir_falhas, font=self.fonte)
        self.menubar.add_cascade(label="Histórico", menu=historico_menu, font=self.fonte)
        self.menubar.entryconfig("Histórico", state='disabled')

        self.config(menu=self.menubar)

    def sair(self):
        """Função para saida do sistema"""
        if tk.messagebox.askokcancel("Sair da Aplicação", "Quer sair do Sistema de Controle e Monitoramento de Iluminacao?"):
            bd_registrar('eventos', 'inserir_base', [(get_now(), "Null", "ACESSO", "Sistema de Controle e Monitoramente de Iluminação FECHADO")])
            "Finalizar os ciclos de threads"
            finalizar_ciclos()
            "Fechar a tela"
            self.destroy()

    def ciclo_relogio(self):
        """ Função para atualização do relógio na tela principal e filhas """
        # Atualiza a hora
        self.alterar_parametro("time", text=get_now())

        # Atualizar totalizador de falhas
        falhas = bd_consulta_generica(sql_consultar_eventos_acao('FALHAS'))
        self.alterar_parametro("lb_falhas_total", text=len(falhas))

        # Verificar se o tempo de login não está expirado
        if self.acessado and datetime.now() > self.tempoacessado:
            self.logout_user("automaticamente")

        # atualiza as imagens das areas
        self.atualizar_imagem_areas()

        # coletar informações da posição da tela
        self.ajustar_posicao_tela()

        # # se existir uma tela aberta, atualiza as imagens da tela filha
        if self.tela.status:
            self.tela.verificar_tela_aberta()
            # self.tela.atualizar_bt()

    def ajustar_posicao_tela(self):
        """Função que coleta a posição da tela principal"""
        posicoes = self.winfo_geometry().split('+')
        self.widthInc = posicoes[1]
        self.heightInc = posicoes[2]

    def login_user(self, nome):
        """Função para acessar o usuário ao sistema"""
        # Se não tiver nenhum usuario acessando o sistema, libera a tela de login
        if not self.acessado:
            tl_login = Login(self, self.update_user, self.tela_fechada, nome, self.widthInc, self.heightInc)
            tl_login.grab_set()
        else:
            self.logout_user("manualmente")

    def logout_user(self, tipo):
        """Função para alterar os variaveis da tela ao sair o usuario do acesso"""

        bd_registrar('eventos', 'inserir_base', [(get_now(), self.usuario, "ACESSO", f"Usuário: {self.usuario} saiu do sistema {tipo}")])
        self.fechar_telas()
        self.usuario = None
        self.acessado = False
        self.alterar_parametro("usuario_nome", text="")
        self.alterar_parametro("bt_login", text='LOGIN')

        # Desabilitar os botões
        self.ativar_desativar_botoes(ativar=False)

    def tela_fechada(self):
        """Função para registrar quando a tela filha e fechada por ela"""
        self.tela = TelaVazia()

    def fechar_telas(self):
        """Função que fecha a tela filha aberta"""
        if self.tela:
            self.tela.sair()

    def update_user(self, usuario, perfil):
        """Atualizar as informações dos usuário que acessou o sistema"""
        self.usuario = usuario
        self.acessado = True
        valor = bd_consultar("sistema")[0]
        # Colocar o tempo máximo de login ativado
        self.tempoacessado = datetime.now() + timedelta(minutes=valor[2])

        self.alterar_parametro("bt_login", text='LOGOUT')
        self.alterar_parametro("usuario_nome", text=usuario)
        self.alterar_parametro("usuario_nome", text=usuario)

        # Habilitar os botões
        self.ativar_desativar_botoes(ativar=True, perfil=perfil)

        # Registra o acesso do usuário nos eventos
        bd_registrar('eventos', 'inserir_base', [(get_now(), self.usuario, "ACESSO", f"Usuário: {self.usuario} acessou o sistema")])

    def criar(self, widget, **kwargs):
        """Função que criar uma ferramenta na tela"""
        w = widget(self, **kwargs)
        name = kwargs.get("name", str(w))
        self.__widgets[name] = w
        return name

    def instalar_em(self, name, **kwargs):
        """Função que instala a ferramenta em uma posição na tela"""
        self.__widgets[name].grid(**kwargs)

    def criar_com_imagem(self, widget, render, **kwargs):
        """Função que criar uma ferramenta na tela"""
        w = widget(self, **kwargs)
        w.image = render

        name = kwargs.get("name", str(w))
        self.__widgets[name] = w
        return name

    def carregar_imagens(self, prefixo, largura, comprimento):
        """Função para carregar a imagem"""
        for imagem in bd_consultar("imagens"):
            setattr(self, prefixo + imagem[1], ImageTk.PhotoImage(Image.open(imagem[2]).resize((largura, comprimento))))

    def alterar_imagem(self, nome, imagem):
        """Altera a imagem de uma ferramenta"""
        self.__widgets[nome].image = imagem

    def retornar_valor_parametro(self, nome, *args):
        """Função que retorna o valor do parametro selecionado"""
        return self.__widgets[nome].config(*args)

    def alterar_parametro(self, name, **kwargs):
        """Função que alterar algum parametro de uma ferramenta"""
        self.__widgets[name].config(**kwargs)

    def atualizar_imagem_areas(self):
        """Função para atualizar as imagens da tela"""
        # Consulta no banco de dados as situações atualizadas
        lista = bd_consultar('areas')
        # Percorre por todas as areas
        for item in lista:
            nome = item[1].lower()
            modo = item[4]
            ligado = item[5]
            ligado_parcial = item[6]
            alarme = item[7]
            conexao = item[8]
            controle = item[9]

            # formata o nome do local da imagem
            nome_imagem_1 = "img_" + nome
            nome_imagem_2 = "img_modo_" + nome
            nome_imagem_3 = "img_controle_" + nome

            # se estiver desconectado
            if conexao == 0:
                imagem_1 = self.img_desconectado
            else:
                # se houver falha
                if alarme == 1:
                    imagem_1 = self.img_alarme
                else:
                    # se todos estão apagados
                    if ligado == 0:
                        # imagem de apagado
                        imagem_1 = self.img_desligado
                    else:
                        # se todos estão ligados
                        if ligado_parcial == 1:
                            # imagem ligado parcial
                            imagem_1 = self.img_ligado_parcial
                        else:
                            # imagem ligado total
                            imagem_1 = self.img_ligado_completo

            # se está em modo é automatico/manual
            if modo == 'AUTOMATICO':
                imagem_2 = self.img2_automatico
                auto = "disabled"
            else:
                imagem_2 = self.img2_manual
                auto = "active"

            # verifica se está logado
            if self.acessado:
                # Ativando /desativando o botão da area
                self.alterar_parametro("bt_" + nome, state=auto)

            # se o controle é remoto/local
            if controle == 1:
                imagem_3 = self.img2_remoto
            else:
                imagem_3 = self.img2_local

            self.alterar_imagem(nome_imagem_1, imagem_1)
            self.alterar_parametro(nome_imagem_1, image=imagem_1)
            self.alterar_imagem(nome_imagem_2, imagem_2)
            self.alterar_parametro(nome_imagem_2, image=imagem_2)
            self.alterar_imagem(nome_imagem_3, imagem_3)
            self.alterar_parametro(nome_imagem_3, image=imagem_3)

    def operacao_automatico(self):
        """Função para operar as areas que estiverem em modo automático """
        # Consulta no banco de dados os horarios das areas
        areas = bd_consultar('areas')
        # Percorre por todas as areas
        for area in areas:
            nome = area[1]
            hora_ligar = area[2]
            hora_desligar = area[3]
            modo = area[4]
            ligado = area[5]
            alarme = area[7]
            conexao = area[8]
            local_ = area[9]

            # Verifica as condições alarme=(0)sem alarme, conexao=(1)conectado, local=(1)remoto,
            if alarme == 0 and conexao == 1 and local_ == 1 and modo == 'AUTOMATICO':
                # Verifica se esta desligada
                if ligado == 0:
                    # Verifica se é permitido ligar neste dia
                    if verifica_dia_semana(area[10]):
                        # Verifica se a hora atual pode ligar dentro da programacao
                        if verificar_horario(hora_ligar, hora_desligar):
                            # consulta os clps da area
                            clp_saidas = bd_consulta_generica(sql_consultar_clp_areas(nome, 'LIGAR'))
                            for clp in clp_saidas:
                                # realiza a ação de ligar
                                if escrever_clp(host=clp[1], port=clp[2], endereco=clp[3]):
                                    # grava no BD o log do evento
                                    bd_registrar('eventos', 'inserir_base',
                                                 [(get_now(), self.usuario, "OPERAÇÃO", f"LIGADO AUTOMATICAMENTE:{area[1]} - {clp[4]}")])
                                else:
                                    # grava no BD o log do evento
                                    bd_registrar('eventos', 'inserir_base',
                                                 [(get_now(), self.usuario, "FALHAS", f"FALHA NA TENTATIVA DE LIGAR:{area[1]} - {clp[4]}")])
                else:
                    # Verifica se hora_atual > hora_desligar
                    if not verificar_horario(hora_ligar, hora_desligar):
                        # consulta os clps da area
                        clp_saidas = bd_consulta_generica(sql_consultar_clp_areas(nome, 'DESLIGAR'))
                        for clp in clp_saidas:
                            # realiza a ação de desligar
                            if escrever_clp(host=clp[1], port=clp[2], endereco=clp[3]):
                                # grava no BD o log do evento
                                bd_registrar('eventos', 'inserir_base',
                                             [(get_now(), self.usuario, "OPERAÇÃO", f"DESLIGADO AUTOMATICAMENTE:{area[1]} - {clp[4]}")])
                            else:
                                # grava no BD o log do evento
                                bd_registrar('eventos', 'inserir_base',
                                             [(get_now(), self.usuario, "FALHAS", f"FALHA NA TENTATIVA DE DESLIGAR:{area[1]} - {clp[4]}")])

    def crud(self, tipo, tabela):
        """Função para abetura das telas do menu administrador"""
        if tipo == "cadastrar":
            if tabela == "usuario":
                self.tela = CadastrarUsuario(self, self.usuario, self.tela_fechada, tabela, self.widthInc, self.heightInc)
            if tabela == "clp":
                self.tela = CadastrarClp(self, self.usuario, self.tela_fechada, tabela, self.widthInc, self.heightInc)
            if tabela == "io":
                self.tela = CadastrarIO(self, self.usuario, self.tela_fechada, tabela, self.widthInc, self.heightInc)
        if tipo == "alterar":
            if tabela == "usuario":
                self.tela = AlterarUsuario(self, self.usuario, self.tela_fechada, tabela, self.widthInc, self.heightInc)
            if tabela == "clp":
                self.tela = AlterarClp(self, self.usuario, self.tela_fechada, tabela, self.widthInc, self.heightInc)
            if tabela == "io":
                self.tela = AlterarIO(self, self.usuario, self.tela_fechada, tabela, self.widthInc, self.heightInc)
        if tipo == "listar":
            if tabela == "usuario":
                self.tela = ListarUsuario(self, self.usuario, self.tela_fechada, tabela, self.widthInc, self.heightInc)
            if tabela == "clp":
                self.tela = ListarClp(self, self.usuario, self.tela_fechada, tabela, self.widthInc, self.heightInc)
            if tabela == "io":
                self.tela = ListarIO(self, self.usuario, self.tela_fechada, tabela, self.widthInc, self.heightInc)
        if tipo == "historico":
            self.tela = Historico(self, self.usuario, self.tela_fechada, tabela, self.widthInc, self.heightInc)
        if tipo == "sistema":
            self.tela = AlterarConfigSistema(self, self.usuario, self.tela_fechada, self.logout_user, tabela, self.widthInc, self.heightInc)
        self.tela.grab_set()

    def atualizar_bd(self):
        """  Função para realizar o teste de conexão com o clps e atualizar as informações no BD  """
        # gerar a lista de areas
        for area in bd_consultar("areas"):
            soma = 0

            # gerar a lista de clps de uma area
            clp_saidas = bd_consulta_generica(sql_consultar_clp_areas(area[1], 'SAIDA'))
            for clp in clp_saidas:
                # verifica os acionamentos das saidas dos clps
                conectado, valor = ler_clp(host=clp[1], port=clp[2], tipo='saidas')
                if not conectado:
                    # se negativo altera o valor para falha
                    bd_registrar("areas", "atualizar_conexao", [(0, clp[0])])
                    bd_registrar("clps", 'atualizar_clp_ativo', [(0, clp[4])])
                else:
                    # se positivo altera o valor para normal
                    bd_registrar("areas", "atualizar_conexao", [(1, clp[0])])
                    bd_registrar("clps", 'atualizar_clp_ativo', [(1, clp[4])])
                    # incrementa a soma se a saida estiver ligada, busca atraves da posição, do endereço
                    if valor[clp[3] - 1]:
                        soma += 1
                # verifica se está em modo remoto ou local
                conectado, valor = ler_clp(host=clp[1], port=clp[2], tipo='remoto')
                if conectado:
                    if area[9] == 1 and valor[0]:
                        # registra como local
                        bd_registrar("areas", "atualizar_local", [(0, clp[0])])
                        bd_registrar('eventos', 'inserir_base', [(get_now(), self.usuario, "OPERAÇÃO", f"ALTERADO PARA MODO LOCAL - {area[1]}")])
                    if area[9] == 0 and not valor[0]:
                        # registra como remoto
                        bd_registrar("areas", "atualizar_local", [(1, clp[0])])
                        bd_registrar('eventos', 'inserir_base', [(get_now(), self.usuario, "OPERAÇÃO", f"ALTERADO PARA MODO REMOTO - {area[1]}")])

            # gerar a lista de clps de uma area
            clp_falhas = bd_consulta_generica(sql_consultar_clp_areas(area[1], 'FALHA'))
            for clp in clp_falhas:
                # verifica os acionamento de falhas nos clps
                conectado, valor = ler_clp(host=clp[1], port=clp[2], endereco=clp[3], tipo='alarmes')
                if conectado:
                    # retira a falha
                    bd_registrar("areas", "atualizar_falha", [(0, clp[0])])
                    if valor[0]:
                        # informa a falha
                        bd_registrar("areas", "atualizar_falha", [(1, clp[0])])

            # verifica se foi acionado por completou parcialmente
            if soma == 0:
                # desligado totalmente
                bd_registrar("areas", "atualizar_operacao", [(0, 0, area[1])])
            else:
                if soma != len(clp_saidas):
                    # ligado parcialmente
                    bd_registrar("areas", "atualizar_operacao", [(1, 1, area[1])])
                else:
                    # está ligado por completo
                    bd_registrar("areas", "atualizar_operacao", [(1, 0, area[1])])

    def operacao_ligar(self, nome):
        """Função que realiza as operações MANUALMENTE de ligar/desligar"""
        # busca no BD pelo nome a situação(ligado/desligado) atual do local
        status_atual = bd_consultar_operacao_area(nome)
        clp_saidas = []
        status_nome = ''

        # verifica se está permitido o clique dentro do prazo
        if datetime.now() > self.cliquebotao:
            # realiza a inversão de situação
            if status_atual[0] == 1:
                # realizar a pergunta de confirmação de desligamento
                if tk.messagebox.askokcancel("Desligar", "Têm certeza que quer desligar está área?"):
                    status_nome = "DESLIGADO MANUALMENTE"
                    clp_saidas = bd_consulta_generica(sql_consultar_clp_areas(nome, 'DESLIGAR'))
            else:
                status_nome = "LIGADO MANUALMENTE"
                clp_saidas = bd_consulta_generica(sql_consultar_clp_areas(nome, 'LIGAR'))

            # verifica se existe algum área para desligar
            if clp_saidas:
                # Enviar as informações ao clp para ligar ou desligar
                for clp in clp_saidas:
                    # realiza a ação de ligar
                    if escrever_clp(host=clp[1], port=clp[2], endereco=clp[3]):
                        # grava no BD o log do evento
                        bd_registrar('eventos', 'inserir_base', [(get_now(), self.usuario, "OPERAÇÃO", f"{status_nome} - {nome}")])

            # atualizando o tempo entre cliques
            self.cliquebotao = datetime.now() + timedelta(seconds=2)

    def operacao_manual(self, nome):
        """Função que alterar o modo de operação manual/automático"""
        # conferir o valor atual
        status_atual = bd_consulta_valor_tabela('areas', 'nome', nome)[0]
        # inverter o valor
        if status_atual[4] == 'AUTOMATICO':
            valor = "MANUAL"
        else:
            valor = "AUTOMATICO"
        # salvar o valor final
        bd_registrar("areas", "atualizar_modo", [(valor, nome)])
        bd_registrar('eventos', 'inserir_base',
                     [(get_now(), self.usuario, "CONFIGURAÇÃO_AREA", f"Alterado o modo de operação manualmente para {valor} de {nome}")])

    def operacao_local(self, nome):
        """Função que alterar o modo de operação local/remoto"""
        # conferir o valor atual
        status_atual = bd_consulta_valor_tabela('areas', 'nome', nome)[0]
        # realiza a inversão de situação
        if status_atual[9] == 1:
            status_nome = "LOCAL"
            endereco = 9
        else:
            status_nome = "REMOTO"
            endereco = 10

        # lista dos clps vinculado a area
        clp_saidas = bd_consulta_generica(sql_consultar_clp_areas(nome, 'LIGAR'))
        # Enviar as informações ao clp para ligar ou desligar
        for clp in clp_saidas:
            # realiza a ação de ligar
            if escrever_clp(host=clp[1], port=clp[2], endereco=endereco):
                # grava no BD o log do evento
                bd_registrar('eventos', 'inserir_base', [(get_now(), self.usuario, "CONFIGURAÇÃO_AREA",
                                                          f"Alterado o controle de operação manualmente para {status_nome} de {nome}")])

    def agenda(self, area):
        """Função abertura da tela de configuração da área"""
        agenda = Agenda(self, self.usuario, self.tela_fechada, area, "agenda", self.widthInc, self.heightInc)
        agenda.grab_set()

    def posicionar_tela(self, widht, height):
        """Função para posicionamento da tela"""
        widht = int(self.winfo_screenwidth() * 0.95)
        height = int(self.winfo_screenheight() * 0.85)
        self.geometry(f'{widht}x{height}+{0}+{0}')

    def ativar_desativar_botoes(self, ativar, perfil=0):
        """Função para ativar e desativar os botões da tela principal"""

        acao_sup = 'disabled'
        acao_opr = 'disabled'
        acao = 'disabled'
        menu = False

        # verifica se é para ativar os botões
        if ativar:
            # perfil administrador
            if perfil == 1:
                menu = True
                acao_sup = 'active'
                acao_opr = 'active'

            # perfil supervisor
            if perfil == 2:
                acao_sup = 'active'
                acao_opr = 'active'
            # perfil operador
            if perfil == 3:
                acao_opr = 'active'

        self.ativar_desativar_menu(menu)

        self.alterar_parametro("bt_salao_embarque_internacional", state=acao)
        self.alterar_parametro("img_modo_salao_embarque_internacional", state=acao_opr)
        self.alterar_parametro("bt_configuracao_salao_embarque_internacional", state=acao_sup)
        self.alterar_parametro("bt_saguao_embarque", state=acao)
        self.alterar_parametro("img_modo_saguao_embarque", state=acao_opr)
        self.alterar_parametro("bt_configuracao_saguao_embarque", state=acao_sup)
        self.alterar_parametro("bt_salao_embarque_domestico", state=acao)
        self.alterar_parametro("img_modo_salao_embarque_domestico", state=acao_opr)
        self.alterar_parametro("bt_configuracao_salao_embarque_domestico", state=acao_sup)
        self.alterar_parametro("bt_mezanino", state=acao)
        self.alterar_parametro("img_modo_mezanino", state=acao_opr)
        self.alterar_parametro("bt_configuracao_mezanino", state=acao_sup)
        self.alterar_parametro("bt_conectores", state=acao)
        self.alterar_parametro("img_modo_conectores", state=acao_opr)
        self.alterar_parametro("bt_configuracao_conectores", state=acao_sup)
        self.alterar_parametro("bt_saguao_desembarque", state=acao)
        self.alterar_parametro("img_modo_saguao_desembarque", state=acao_opr)
        self.alterar_parametro("bt_configuracao_saguao_desembarque", state=acao_sup)
        self.alterar_parametro("bt_salao_desembarque_internacional", state=acao)
        self.alterar_parametro("img_modo_salao_desembarque_internacional", state=acao_opr)
        self.alterar_parametro("bt_configuracao_salao_desembarque_internacional", state=acao_sup)
        self.alterar_parametro("bt_viaduto_superior", state=acao)
        self.alterar_parametro("img_modo_viaduto_superior", state=acao_opr)
        self.alterar_parametro("bt_configuracao_viaduto_superior", state=acao_sup)
        self.alterar_parametro("bt_viaduto_inferior", state=acao)
        self.alterar_parametro("img_modo_viaduto_inferior", state=acao_opr)
        self.alterar_parametro("bt_configuracao_viaduto_inferior", state=acao_sup)
        self.alterar_parametro("bt_salao_desembarque_domestico", state=acao)
        self.alterar_parametro("img_modo_salao_desembarque_domestico", state=acao_opr)
        self.alterar_parametro("bt_configuracao_salao_desembarque_domestico", state=acao_sup)

    def ativar_desativar_menu(self, ativar):
        """Função para ativar e desativar o menu da tela principal"""
        if ativar:
            self.menubar.entryconfig("Usuário", state='active')
            self.menubar.entryconfig("Comunicação", state='active')
            self.menubar.entryconfig("Sistema", state='active')
            self.menubar.entryconfig("Histórico", state='active')
        else:
            self.menubar.entryconfig("Usuário", state='disabled')
            self.menubar.entryconfig("Comunicação", state='disabled')
            self.menubar.entryconfig("Sistema", state='disabled')
            self.menubar.entryconfig("Histórico", state='disabled')

    def habilitar_computador(self):
        """Função que insere o mac_address no banco de dados"""
        valor = str(hex(uuid.getnode()))

        # verifica se mac_address já está cadastrada no BD
        if bd_consulta_valor_tabela('mac_address', 'mac_nome', valor):
            tk.messagebox.showerror(title="Erro", message="Computador já está habilitado!")
        else:
            bd_registrar("mac_address", 'inserir_base', [[(valor)]])
            bd_registrar('eventos', 'inserir_base', [(get_now(), self.usuario, "CADASTRO", f"CADASTRADO NOVO MAC_ADDRESS - {valor}")])
            tk.messagebox.showinfo(title="Sucesso", message="Computador habilitado!")

    def excluir_falhas(self):
        """Função que exclui as falhas existentes"""
        bd_excluir_item('eventos', 'FALHAS')


def verificar_horario(ligar_txt, desligar_txt):
    """Função que realiza as operações AUTOMATICAMENTE de ligar/desligar"""
    now = datetime.now()
    ligar_fmt = ligar_txt.split(':')
    desligar_fmt = desligar_txt.split(':')

    h_ligar = datetime(now.year, now.month, now.day, int(ligar_fmt[0]), int(ligar_fmt[1]))
    h_desligar = datetime(now.year, now.month, now.day, int(desligar_fmt[0]), int(desligar_fmt[1]))

    # verifica se os horarios de ligar e desligar
    if h_ligar > h_desligar:
        # verifica se a hora atual e para ligar
        if now > h_ligar or now < h_desligar:
            return True
    else:
        # verifica se a hora atual e para ligar
        if h_ligar < now < h_desligar:
            return True


def inicializar_ciclos(principal):
    """Função que inicializa a thread para a atualizacao do relogio"""
    t1 = Thread(name='atualizar_relogio', target=lambda: thread_atualizar_relogio(principal))
    t1.daemon = True
    t1.start()

    t2 = Thread(name='atualizar_bd', target=lambda: thread_atualizar_bd(principal))
    t2.daemon = True
    t2.start()

    t3 = Thread(name='operacao', target=lambda: thread_operacao(principal))
    t3.daemon = True
    t3.start()


def thread_operar(principal, posicao):
    """Função que gera uma thread para uma operação ligar/desligar"""
    t4 = Thread(name='operar', target=lambda: principal.operacao_ligar(posicao))
    t4.start()


def finalizar_ciclos():
    """Função para finalizar os threads"""
    globals()["threads"] = False


def thread_atualizar_relogio(principal):
    """Função que atualiza o relogio"""
    while globals()["threads"]:
        principal.ciclo_relogio()
        time.sleep(1)


def thread_atualizar_bd(principal):
    """Função que atualiza o banco de dados"""
    while globals()["threads"]:
        principal.atualizar_bd()
        time.sleep(bd_consultar("sistema")[0][3])


def thread_operacao(principal):
    """Função que realiza as operações em modo automatico"""
    while globals()["threads"]:
        principal.operacao_automatico()
        time.sleep(bd_consultar("sistema")[0][4] * 60)


def verifica_dia_semana(dia_semana):
    """Função que verifica a data de operação"""

    resultado = False
    hoje = datetime.now().weekday()

    # todos os dia
    if dia_semana == 1:
        resultado = True
    # dias úteis
    if dia_semana == 2 and hoje <= 4:
        resultado = True
    # fim de semana
    if dia_semana == 3 and hoje >= 5:
        resultado = True

    return resultado
