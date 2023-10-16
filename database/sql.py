def verificar_basico(nome_tabela):
    return f"SELECT name FROM sqlite_master WHERE type='table' AND name='{nome_tabela}'"


def sql_delete_item(tabela, valor):
    if tabela == 'eventos':
        return f"DELETE FROM {tabela} as x WHERE x.acao = '{valor}';"
    else:
        return f"DELETE FROM {tabela} as x WHERE x.nome = '{valor}';"


""" --------------------------------------------------------------------------- """
# TABELA BOOLEANA
sql_verificar_booleanos = verificar_basico('booleanos')
sql_criar_booleanos = """
        CREATE TABLE booleanos (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        booleano_id INTEGER NOT NULL,
        nome TEXT NOT NULL
        );"""
sql_inserir_base_booleanos = 'INSERT INTO booleanos (booleano_id, nome) VALUES (?,?)'
sql_inserir_valores_booleanos = (
    [(0, 'NÃO')],
    [(1, 'SIM')],
)

""" --------------------------------------------------------------------------- """
# TABELA TIPO DE EVENTOS
sql_verificar_tipos_eventos = verificar_basico('tipos_evento')
sql_criar_tipos_eventos = """
        CREATE TABLE tipos_evento (
        tipo_evento_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
        );"""
sql_inserir_base_tipos_eventos = 'INSERT INTO tipos_evento (nome) VALUES (?)'
sql_inserir_valores_tipos_eventos = [(
    ['ACESSO'],
    ['CADASTRO'],
    ['CONFIGURAÇÃO_AREA'],
    ['INICIALIZAÇÃO'],
    ['FALHAS'],
    ['OPERAÇÃO'],
    ['STARTUP'],
    ['SETUP'],
)]

""" --------------------------------------------------------------------------- """
# TABELA EVENTOS
sql_verificar_eventos = verificar_basico('eventos')
sql_criar_eventos = """
        CREATE TABLE eventos (
        evento_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        data DATE NOT NULL,
        usuario TEXT,
        acao TEXT,
        descricao TEXT NOT NULL
        );"""
sql_inserir_base_eventos = 'INSERT INTO eventos (data, usuario, acao, descricao) VALUES (?,?,?,?)'
sql_inserir_valores_eventos = []

sql_excluir_falhas = """
DELETE FROM eventos WHERE acao = 'FALHAS';
"""


def sql_consultar_eventos_acao(acao):
    return f"SELECT data ||'  -  '|| usuario ||'  -  '|| descricao as valor FROM eventos WHERE acao = '{acao}' ORDER BY data DESC"


""" --------------------------------------------------------------------------- """
# TABELA PERFIL
sql_verificar_perfis = verificar_basico('perfis')
sql_criar_perfis = """
        CREATE TABLE perfis (
        perfil_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
        );"""
sql_inserir_base_perfis = 'INSERT INTO perfis (nome) VALUES (?)'
sql_inserir_valores_perfis = [(
    ['MANUTENÇÃO'],
    ['SUPERVISÃO'],
    ['OPERAÇÃO']
)]

""" --------------------------------------------------------------------------- """
# TABELA USUARIO
sql_verificar_usuarios = verificar_basico('usuarios')
sql_criar_usuarios = """
        CREATE TABLE usuarios (
        usuario_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        booleano_id INTEGER NOT NULL,
        senha TEXT NOT NULL,
        perfil_id INTEGER NOT NULL,
        FOREIGN KEY(perfil_id) REFERENCES perfis(perfil_id)
        FOREIGN KEY(booleano_id) REFERENCES booleanos(booleano_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
        );"""
sql_inserir_base_usuarios = 'INSERT INTO usuarios (nome, booleano_id, perfil_id, senha) VALUES (?,?,?,?)'
sql_inserir_valores_usuarios = (
    [('OPERADOR', 1, 3, '$2b$12$jNngFwYq2Ttm33xR6a0DZ.IYdsblz4XuejzpGYGTg923U/2/6UFpS')],
    [('SUPERVISOR', 1, 2, '$2b$12$2nydp4dkjfvi7DWZEXnG.eYQu2sI6TlfUQaZe9Wslt44fFWf7EGbO')],
    [('ADMINISTRADOR', 1, 1, '$2b$12$lF4y1dalv7sQe6jXfMlgm.uNr/Fd1SoIRHBJIGGHfWlDrowUOhwtK')],
)

sql_consultar_usuario = """SELECT nome, booleano_id, perfil_id, senha WHERE nome = ?"""

sql_consulta_lista_usuario = """
SELECT u.nome, u.nome || '  -  ' || p.nome AS valor
FROM usuarios AS u INNER JOIN perfis as p ON u.perfil_id = p.perfil_id;"""

sql_atualizar_valores_usuario = """UPDATE usuarios set booleano_id = ?, perfil_id = ?, senha = ? WHERE nome = ?"""

""" --------------------------------------------------------------------------- """
# TABELA AREAS
sql_verificar_areas = verificar_basico('areas')
sql_criar_areas = """
        CREATE TABLE areas (
        area_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        hora_ligar TIMESTAMP NOT NULL,
        hora_desligar TIMESTAMP NOT NULL,
        tipo_operacao TEXT NOT NULL,
        ligado INTEGER NOT NULL,
        ligado_parcial INTEGER NOT NULL,
        alarme INTEGER NOT NULL,
        conexao INTEGER NOT NULL,
        local INTEGER NOT NULL,
        dia_semana INTEGER NOT NULL
        );"""

sql_inserir_base_areas = 'INSERT INTO areas (nome, hora_ligar, hora_desligar, tipo_operacao, ligado, alarme, ' \
                         'conexao, local, ligado_parcial, dia_semana) VALUES (?,?,?,?,?,?,?,?,?,?)'

sql_inserir_valores_areas = (
    [('salao_embarque_internacional', '16:00:00', '06:20:00', 'MANUAL', 1, 0, 0, 0, 0, 1)],
    [('salao_embarque_domestico', '16:00:00', '06:20:00', 'MANUAL', 1, 0, 0, 0, 0, 1)],
    [('conectores', '16:00:00', '06:20:00', 'MANUAL', 1, 0, 0, 0, 0, 1)],
    [('salao_desembarque_internacional', '16:00:00', '06:20:00', 'MANUAL', 1, 0, 0, 0, 0, 1)],
    [('salao_desembarque_domestico', '16:00:00', '06:20:00', 'MANUAL', 1, 0, 0, 0, 0, 1)],
    [('saguao_embarque', '16:00:00', '06:20:00', 'MANUAL', 1, 0, 0, 0, 0, 1)],
    [('mezanino', '07:00:00', '23:00:00', 'MANUAL', 1, 0, 0, 0, 0, 2)],
    [('saguao_desembarque', '16:00:00', '06:20:00', 'MANUAL', 1, 0, 0, 0, 0, 1)],
    [('viaduto_superior', '17:00:00', '05:30:00', 'MANUAL', 1, 0, 0, 0, 0, 1)],
    [('viaduto_inferior', '16:30:00', '05:30:00', 'MANUAL', 1, 0, 0, 0, 0, 1)],
)

sql_atualizar_valores_areas = """UPDATE areas set hora_ligar = ?, hora_desligar = ?, dia_semana = ? WHERE nome = ?"""
sql_atualizar_operacao_areas = """UPDATE areas set ligado = ?, ligado_parcial = ? WHERE nome = ?"""
sql_atualizar_conexao_areas = """UPDATE areas set conexao = ? WHERE nome = ?"""
sql_atualizar_local_areas = """UPDATE areas set local = ? WHERE nome = ?"""
sql_atualizar_alarme_areas = """UPDATE areas set alarme = ? WHERE nome = ?"""
sql_atualizar_modo_areas = """UPDATE areas set tipo_operacao = ? WHERE nome = ?"""


def sql_consultar_operacao_area(area):
    return f"SELECT a.ligado FROM areas as a WHERE a.nome = '{area}'"


def sql_consultar_config_area(area):
    return f"SELECT * FROM areas as a WHERE a.nome = '{area}'"


def sql_consultar_clp_areas(area, tipo):
    return f"SELECT DISTINCT a.nome, c.ip, c.porta, e.endereco, c.nome FROM areas as a " \
           f" INNER JOIN entradas_saidas as e ON e.area_id = a.area_id" \
           f" INNER JOIN tipos_io as t ON e.tipo_io_id = t.tipo_io_id" \
           f" INNER JOIN clps as c ON e.clp_id = c.clp_id WHERE t.nome = '{tipo}' and a.nome = '{area}'"


sql_consultar_atualizacao = """SELECT a.nome as nome, 
count(a.nome) as total, 
count(CASE	WHEN a.ligado = 1 THEN 1 END) as ligado,
count(CASE	WHEN a.alarme = 1 THEN 1 END) as alarme,
count(CASE	WHEN a.conexao = 1 THEN 1 END) as conexao
FROM areas as a
GROUP BY a.nome;"""

""" --------------------------------------------------------------------------- """
# TABELA IMAGENS
sql_verificar_imagens = verificar_basico('imagens')
sql_criar_imagens = """
        CREATE TABLE imagens (
        imagem_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        local TEXT NOT NULL
        );"""
sql_inserir_base_imagens = 'INSERT INTO imagens (nome, local) VALUES (?,?)'
sql_inserir_valores_imagens = (
    [('alarme', 'img/alarme.png')],
    [('automatico', 'img/automatico.png')],
    [('manual', 'img/manual.png')],
    [('local', 'img/local.png')],
    [('remoto', 'img/remoto.png')],
    [('desligado', 'img/desligado.png')],
    [('ligado_completo', 'img/ligado_completo.png')],
    [('ligado_parcial', 'img/ligado_parcial.png')],
    [('desconectado', 'img/desconectado.png')],
)


def sql_consultar_ferramentas_telas(area):
    return f"SELECT s.nome, s.funcao, s.ferramenta, s.kwargs" \
           f" FROM areas AS a INNER JOIN telas as s ON a.area_id = s.area_id WHERE a.nome = '{area}'"


""" --------------------------------------------------------------------------- """
# TABELA CLP
sql_verificar_clps = verificar_basico('clps')
sql_criar_clps = """
        CREATE TABLE clps (
        clp_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        ip TEXT NOT NULL,
        porta INTEGER NOT NULL,
        id INTEGER NOT NULL,
        ativo INTEGER NOT NULL,
        FOREIGN KEY(ativo) REFERENCES booleanos(booleano_id)
        );"""
sql_inserir_base_clps = 'INSERT INTO clps (nome, ip, porta, id, ativo) VALUES (?,?,?,?,?)'

sql_inserir_valores_clps = (
    [('CLP01_SL05', '10.22.217.10', 510, 1, 0)],
    [('CLP02_SL06', '10.22.217.11', 510, 2, 0)],
    [('CLP03_SL07', '10.22.217.12', 510, 3, 0)],
    [('CLP04_SL08', '10.22.217.13', 510, 4, 0)],
    [('CLP05_SL09', '10.22.217.14', 510, 5, 0)],
    [('CLP06_SL10', '10.22.217.15', 510, 6, 0)],
    [('CLP07_SL11', '10.22.217.16', 510, 7, 0)],
    [('CLP08_SL12', '10.22.217.17', 510, 8, 0)],
)

sql_consultar_clps_concatenada = """
SELECT c.nome || ' - ' || c.ip || ' - ' || c.porta || ' - ' || c.id || ' - ' || b.nome as valor
FROM clps as c INNER JOIN booleanos as b ON c.ativo = b.booleano_id ;"""

sql_atualizar_clp = """UPDATE clps set nome = ?, ip = ?, porta = ?, id = ? WHERE nome = ?"""

sql_atualizar_clp_ativo = """UPDATE clps set ativo = ? WHERE nome = ?"""

""" --------------------------------------------------------------------------- """
# TABELA TIPOS DE ENTRADAS/SAIDAS
sql_verificar_tipos_io = verificar_basico('tipos_io')
sql_criar_tipos_io = """
        CREATE TABLE tipos_io (
        tipo_io_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
        );"""
sql_inserir_base_tipos_io = 'INSERT INTO tipos_io (nome) VALUES (?)'
sql_inserir_valores_tipos_io = [(
    ['LIGAR'],
    ['DESLIGAR'],
    ['SAIDA'],
    ['FALHA'],
)]

""" --------------------------------------------------------------------------- """
# TABELA TIPOS DE ENTRADAS/SAIDAS
sql_verificar_entradas_saidas = verificar_basico('entradas_saidas')
sql_criar_entradas_saidas = """
        CREATE TABLE entradas_saidas (
        io_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        endereco INTEGER NOT NULL,
        clp_id INTEGER NOT NULL,
        tipo_io_id INTEGER NOT NULL,
        area_id INTEGER NOT NULL,
        FOREIGN KEY(clp_id) REFERENCES clps(clp_id),
        FOREIGN KEY(tipo_io_id) REFERENCES tipos_io(tipo_io_id),
        FOREIGN KEY(area_id) REFERENCES areas(area_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
        );"""

sql_inserir_base_entradas_saidas = """
INSERT INTO entradas_saidas (nome, endereco, tipo_io_id, clp_id, area_id) VALUES (?,?,?,?,?)"""

# sql_inserir_valores_entradas_saidas = ()
sql_inserir_valores_entradas_saidas = (
    [('CLP01_SAIDA01', 1, 3, 1, 3)],
    [('CLP01_SAIDA02', 2, 3, 1, 5)],
    [('CLP01_LIGAR_01', 1, 1, 1, 3)],
    [('CLP01_DESLIGAR_01', 2, 2, 1, 3)],
    [('CLP01_LIGAR_02', 3, 1, 1, 5)],
    [('CLP01_DESLIGAR_02', 4, 2, 1, 5)],
    [('CLP01_FALHA_01', 1, 4, 1, 3)],
    [('CLP01_FALHA_02', 2, 4, 1, 5)],

    [('CLP02_SAIDA01', 1, 3, 2, 5)],
    [('CLP02_SAIDA02', 2, 3, 2, 4)],
    [('CLP02_SAIDA03', 3, 3, 2, 8)],
    [('CLP02_SAIDA04', 4, 3, 2, 10)],
    [('CLP02_LIGAR_01', 1, 1, 2, 5)],
    [('CLP02_DESLIGAR_01', 2, 2, 2, 5)],
    [('CLP02_LIGAR_02', 3, 1, 2, 4)],
    [('CLP02_DESLIGAR_02', 4, 2, 2, 4)],
    [('CLP02_LIGAR_03', 5, 1, 2, 8)],
    [('CLP02_DESLIGAR_03', 6, 2, 2, 8)],
    [('CLP02_LIGAR_04', 7, 1, 2, 10)],
    [('CLP02_DESLIGAR_04', 8, 2, 2, 10)],
    [('CLP02_FALHA_01', 1, 4, 2, 5)],
    [('CLP02_FALHA_02', 2, 4, 2, 4)],
    [('CLP02_FALHA_03', 3, 4, 2, 8)],
    [('CLP02_FALHA_04', 4, 4, 2, 10)],

    [('CLP03_SAIDA01', 1, 3, 3, 4)],
    [('CLP03_SAIDA02', 2, 3, 3, 8)],
    [('CLP03_SAIDA03', 3, 3, 3, 10)],
    [('CLP03_LIGAR_01', 1, 1, 3, 4)],
    [('CLP03_DESLIGAR_01', 2, 2, 3, 4)],
    [('CLP03_LIGAR_02', 3, 1, 3, 8)],
    [('CLP03_DESLIGAR_02', 4, 2, 3, 8)],
    [('CLP03_LIGAR_03', 5, 1, 3, 10)],
    [('CLP03_DESLIGAR_03', 6, 2, 3, 10)],
    [('CLP03_FALHA_01', 1, 4, 3, 4)],
    [('CLP03_FALHA_02', 2, 4, 3, 8)],
    [('CLP03_FALHA_03', 3, 4, 3, 10)],

    [('CLP04_SAIDA01', 1, 3, 4, 4)],
    [('CLP04_SAIDA02', 2, 3, 4, 3)],
    [('CLP04_LIGAR_01', 1, 1, 4, 4)],
    [('CLP04_DESLIGAR_01', 2, 2, 4, 4)],
    [('CLP04_LIGAR_02', 3, 1, 4, 3)],
    [('CLP04_DESLIGAR_02', 4, 2, 4, 3)],
    [('CLP04_FALHA_01', 1, 4, 4, 4)],
    [('CLP04_FALHA_02', 2, 4, 4, 3)],

    [('CLP05_SAIDA01', 1, 3, 5, 2)],
    [('CLP05_LIGAR_01', 1, 1, 5, 2)],
    [('CLP05_DESLIGAR_01', 2, 2, 5, 2)],
    [('CLP05_FALHA_01', 1, 4, 5, 2)],

    [('CLP06_SAIDA02', 2, 3, 6, 2)],
    [('CLP06_SAIDA03', 3, 3, 6, 6)],
    [('CLP06_SAIDA04', 4, 3, 6, 9)],
    [('CLP06_LIGAR_02', 3, 1, 6, 2)],
    [('CLP06_DESLIGAR_02', 4, 2, 6, 2)],
    [('CLP06_LIGAR_03', 5, 1, 6, 6)],
    [('CLP06_DESLIGAR_03', 6, 2, 6, 6)],
    [('CLP06_LIGAR_04', 7, 1, 6, 9)],
    [('CLP06_DESLIGAR_04', 8, 2, 6, 9)],
    [('CLP06_FALHA_02', 2, 4, 6, 2)],
    [('CLP06_FALHA_03', 3, 4, 6, 6)],
    [('CLP06_FALHA_04', 4, 4, 6, 9)],

    [('CLP07_SAIDA01', 1, 3, 7, 2)],
    [('CLP07_SAIDA02', 2, 3, 7, 7)],
    [('CLP07_SAIDA03', 3, 3, 7, 6)],
    [('CLP07_SAIDA04', 4, 3, 7, 9)],
    [('CLP07_LIGAR_01', 1, 1, 7, 2)],
    [('CLP07_DESLIGAR_01', 2, 2, 7, 2)],
    [('CLP07_LIGAR_02', 3, 1, 7, 7)],
    [('CLP07_DESLIGAR_02', 4, 2, 7, 7)],
    [('CLP07_LIGAR_03', 5, 1, 7, 6)],
    [('CLP07_DESLIGAR_03', 6, 2, 7, 6)],
    [('CLP07_LIGAR_04', 7, 1, 7, 9)],
    [('CLP07_DESLIGAR_04', 8, 2, 7, 9)],
    [('CLP07_FALHA_01', 1, 4, 7, 2)],
    [('CLP07_FALHA_02', 2, 4, 7, 7)],
    [('CLP07_FALHA_03', 3, 4, 7, 6)],
    [('CLP07_FALHA_04', 4, 4, 7, 9)],

    [('CLP08_SAIDA01', 1, 3, 8, 1)],
    [('CLP08_LIGAR_01', 1, 1, 8, 1)],
    [('CLP08_DESLIGAR_01', 2, 2, 8, 1)],
    [('CLP08_FALHA_01', 1, 4, 8, 1)],
)

sql_consultar_entradas_saidas_concatenada = """
SELECT e.nome, e.nome || ' - ' || e.endereco || ' - ' || c.nome || ' - ' || t.nome || ' - ' || a.nome as valor 
FROM entradas_saidas as e 
INNER JOIN clps as c ON e.clp_id = c.clp_id 
INNER JOIN tipos_io as t ON e.tipo_io_id = t.tipo_io_id
INNER JOIN areas as a ON e.area_id = a.area_id
ORDER BY valor
;"""

sql_consultar_entradas_saidas = """
SELECT e.io_id as id, e.nome, e.endereco as endereco, c.nome as clp, t.nome as tipo, a.nome as area
FROM entradas_saidas as e 
INNER JOIN clps as c ON e.clp_id = c.clp_id 
INNER JOIN tipos_io as t ON e.tipo_io_id = t.tipo_io_id
INNER JOIN areas as a ON e.area_id = a.area_id
;"""

sql_atualizar_entradas_saidas = """UPDATE entradas_saidas set nome = ?, endereco = ?, clp_id = ?, tipo_io_id = ?, area_id = ? WHERE nome = ?"""

""" --------------------------------------------------------------------------- """
# TABELA PARAMETROS DO SISTEMA
sql_verificar_sistema = verificar_basico('sistema')
sql_criar_sistema = """
        CREATE TABLE sistema (
        sistema_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        tela_aberta INTEGER NOT NULL,
        login INTEGER NOT NULL,
        atualizacao INTEGER NOT NULL,
        operacao INTEGER NOT NULL
        );"""
sql_inserir_base_sistema = 'INSERT INTO sistema (tela_aberta, login, atualizacao, operacao) VALUES (?,?,?,?)'
sql_inserir_valores_sistema = [(
    [5, 10, 1, 1],
)]
sql_atualizar_valores_sistema = """UPDATE sistema set tela_aberta = ?, login = ?, atualizacao = ?, operacao = ? WHERE sistema_id = 1"""

""" --------------------------------------------------------------------------- """
# TABELA MAC ADDRESS PC CLIENTE
sql_verificar_mac_address = verificar_basico('mac_address')

sql_criar_mac_address = """
        CREATE TABLE mac_address (
        mac_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        mac_nome TEXT NOT NULL
        );"""
sql_inserir_base_mac_address = 'INSERT INTO mac_address (mac_nome) VALUES (?)'

sql_inserir_valores_mac_address = []

""" --------------------------------------------------------------------------- """
# TABELA DIAS DA SEMANA
sql_verificar_dias_semana = verificar_basico('dias_semana')

sql_criar_dias_semana = """
        CREATE TABLE dias_semana (
        dia_semana_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
        );"""
sql_inserir_base_dias_semana = 'INSERT INTO dias_semana (nome) VALUES (?)'

sql_inserir_valores_dias_semana = [(
    ['TODOS DIAS'],
    ['DIAS ÚTEIS'],
    ['FIM DE SEMANA'],
)]
