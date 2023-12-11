from config import Config
from flask import Flask
from flask import jsonify, request

# Importando o arquivo de configuração
from config import conexao_BD1

import psycopg2 # para BD Postgres
from flask_cors import CORS

# Criando a aplicação
api = Flask (__name__)
CORS(api)
api.config.from_object(Config)

# Conectando com o banco de dados
minhaConexaoSql = psycopg2.connect(
    host=conexao_BD1['host'],
    database=conexao_BD1['banco'],
    user=conexao_BD1['usuario'],
    password=conexao_BD1['senha']
)
cursor = minhaConexaoSql.cursor()

# CREATE grupo_musculo
@api.route('/grupo_musculo', methods=['POST'])
def cadastrarGrupoMusculo():

    dados = request.get_json()

    if 'nome' not in dados:
        return jsonify({'mensagem': 'Campos obrigatórios não fornecidos.'}), 400

    nome = dados['nome']

    cursor.execute("INSERT INTO V_Grupo_musculo (nome) VALUES (%s)", (nome,))
    minhaConexaoSql.commit()

    return jsonify({'mensagem': 'Grupo Muscular cadastrado com sucesso.'}), 201

# READ grupo_musculo (todos)
@api.route('/grupo_musculo', methods=['GET'])
def obterTodosGrupoMusculo():

    comandoSQL = "SELECT * FROM V_Grupo_musculo"

    cursor.execute(comandoSQL)
    registros = cursor.fetchall()

    registros_json = []
    for registro in registros:
        registro_json = {
            'cod_grupo_musculo': registro[0],
            'nome': registro[1]
        }
        registros_json.append(registro_json)
    response = jsonify(registros_json)
    # response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8081')
    return response

# READ grupo_musculo (único)
@api.route('/grupo_musculo/<int:cod_grupo_musculo>', methods=['GET'])
def obterUmGrupoMusculo(cod_grupo_musculo):
    cursor.execute("SELECT * FROM V_Grupo_musculo WHERE cod_grupo_musculo = %s", (cod_grupo_musculo,))
    registro = cursor.fetchone()

    if registro is None:
        return jsonify({'mensagem': 'Grupo muscular não encontrado.'}), 404
    
    grupo_musculo = {
        'cod_grupo_musculo': registro[0],
        'nome': registro[1]
    }

    return jsonify(grupo_musculo)

# UPDATE grupo_musculo
@api.route('/grupo_musculo/<int:cod_grupo_musculo>', methods=['PUT'])
def atualizarGrupoMusculo(cod_grupo_musculo):
    cursor.execute("SELECT * FROM V_Grupo_musculo WHERE cod_grupo_musculo = %s", (cod_grupo_musculo,))
    registro = cursor.fetchone()

    if registro is None:
        return jsonify({'mensagem': 'Grupo muscular não encontrado.'}), 404

    dados = request.get_json()

    # Mapeamento dos campos do JSON para as colunas do banco de dados
    campos_para_atualizar = {
        'cod_grupo_musculo': registro[0],
        'nome': registro[1]
    }

    for campo_json, valor in campos_para_atualizar.items():
        if campo_json in dados:
            novo_valor = dados[campo_json]
            cursor.execute(f'UPDATE V_Grupo_musculo SET {campo_json} = %s WHERE cod_grupo_musculo = %s', (novo_valor, cod_grupo_musculo)) # coluna_bd trocado por campo_json

    minhaConexaoSql.commit()

    return jsonify({'mensagem': 'Grupo muscular atualizado com sucesso.'}), 200

# DELETE grupo_musculo
@api.route('/grupo_musculo/<int:cod_grupo_musculo>', methods=['DELETE'])
def excluirGrupoMusculo(cod_grupo_musculo):
    cursor.execute("SELECT * FROM V_Grupo_musculo WHERE cod_grupo_musculo = %s", (cod_grupo_musculo,))
    registro = cursor.fetchone()

    if registro is None:
        return jsonify({'mensagem': 'Grupo muscular não encontrado.'}), 404
    
    cursor.execute("DELETE FROM Grupo_musculo WHERE cod_grupo_musculo = %s", (cod_grupo_musculo,))
    minhaConexaoSql.commit()

    return jsonify({'mensagem': 'Grupo muscular excluído com sucesso.'}), 200

# READ exercicio_generico
@api.route('/exercicio_generico', methods=['GET'])
def obterTodosExercicioGenerico():

    comandoSQL = "SELECT * FROM V_Exercicio_generico"

    cursor.execute(comandoSQL)
    registros = cursor.fetchall()

    registros_json = []
    for registro in registros:
        registro_json = {
            'cod_exercicio': registro[0],
            'nome': registro[1],
            'aparelho': registro[2],
            'cod_grupo_musculo': registro[3]
        }
        registros_json.append(registro_json)
    
    return jsonify(registros_json)

# READ exercicio_generico (obter exercicios por grupo muscular)
@api.route('/exercicio_generico/por_grupo_musculo/<int:cod_grupo_musculo>', methods=['GET'])
def obterExercicioGenericoPorGrupoMusculo(cod_grupo_musculo):

    # Verifica se o cod_grupo_musculo existe no BD
    cursor.execute("SELECT * FROM V_Grupo_musculo WHERE cod_grupo_musculo = %s", (cod_grupo_musculo,))
    registro_grupo_musculo = cursor.fetchone()

    if registro_grupo_musculo is None:
        return jsonify({'mensagem': 'Grupo muscular não encontrado.'}), 404

    cursor.execute('SELECT * FROM V_Exercicio_generico WHERE cod_grupo_musculo = %s', (cod_grupo_musculo, ))

    if cursor.rowcount == 0:
        return jsonify([])  # Retorna uma lista vazia se não houver registros
    
    registros = cursor.fetchall()

    registros_json = []
    for registro in registros:
        registro_json = {
            'cod_exercicio': registro[0],
            'nome': registro[1],
            'aparelho': registro[2],
            'cod_grupo_musculo': registro[3]
        }
        registros_json.append(registro_json)
    
    return jsonify(registros_json)

# READ exercicio generico (único)
@api.route('/exercicio_generico/<int:cod_exercicio>', methods=['GET'])
def obterUmExercicioGenerico(cod_exercicio):
    cursor.execute("SELECT * FROM V_Exercicio_generico WHERE cod_exercicio = %s", (cod_exercicio,))
    registro = cursor.fetchone()

    if registro is None:
        return jsonify({'mensagem': 'Exercício não encontrado.'}), 404
    
    exercicio_generico = {
        'cod_exercicio': registro[0],
        'nome': registro[1],
        'aparelho': registro[2],
        'cod_grupo_musculo': registro[3]
    }

    return jsonify(exercicio_generico)

# CREATE exercicio_generico
@api.route('/exercicio_generico', methods=['POST'])
def cadastrarExercicioGenerico():
    dados = request.get_json()

    if 'nome' not in dados or 'aparelho' not in dados:
        return jsonify({'mensagem': 'Campos obrigatórios não fornecidos.'}), 400
    else:
        # Verifica se o cod_grupo_musculo existe no BD
        cursor.execute("SELECT * FROM V_Grupo_musculo WHERE cod_grupo_musculo = %s", (dados['cod_grupo_musculo'],))
        registro_grupo_musculo = cursor.fetchone()

        if registro_grupo_musculo is None:
            return jsonify({'mensagem': 'Grupo muscular não encontrado.'}), 404
        
    if type(dados['cod_grupo_musculo']) == str:
        if dados['cod_grupo_musculo'].strip() == '':
            dados['cod_grupo_musculo'] = None
    
    if type(dados['aparelho']) == str:
        if dados['aparelho'].strip() == '':
            dados['aparelho'] = None
    
    nome = dados['nome']
    aparelho = dados['aparelho']
    cod_grupo_musculo = dados['cod_grupo_musculo']

    cursor.execute("INSERT INTO V_Exercicio_generico (nome, aparelho, cod_grupo_musculo) VALUES (%s,%s,%s)", (nome, aparelho, cod_grupo_musculo))
    minhaConexaoSql.commit()

    return jsonify({'mensagem': 'Exercicio generico cadastrado com sucesso.'}), 201

# UPDATE Exercicio_generico
@api.route('/exercicio_generico/<int:cod_exercicio>', methods=['PUT'])
def atualizarExercicioGenerico(cod_exercicio):
    cursor.execute("SELECT * FROM V_Exercicio_generico WHERE cod_exercicio = %s", (cod_exercicio,))
    registro = cursor.fetchone()

    if registro is None:
        return jsonify({'mensagem': 'Exercicio generico não encontrado.'}), 404
    else:
        dados = request.get_json()
        if 'cod_grupo_musculo' in dados:
            # Verifica se o cod_grupo_musculo existe no BD
            cursor.execute("SELECT * FROM V_Grupo_musculo WHERE cod_grupo_musculo = %s", (dados['cod_grupo_musculo'],))
            registro_grupo_musculo = cursor.fetchone()

            if registro_grupo_musculo is None:
                return jsonify({'mensagem': 'Grupo muscular não encontrado.'}), 404
    
    if type(dados['cod_grupo_musculo']) == str:
        if dados['cod_grupo_musculo'].strip() == '':
            dados['cod_grupo_musculo'] = None
    
    if type(dados['aparelho']) == str:
        if dados['aparelho'].strip() == '':
            dados['aparelho'] = None

    # Mapeamento dos campos do JSON para as colunas do banco de dados
    campos_para_atualizar = {
        'nome': registro[0],
        'aparelho': registro[1],
        'cod_grupo_musculo': registro[2]
    }

    for campo_json, valor in campos_para_atualizar.items():
        if campo_json in dados:
            novo_valor = dados[campo_json]
            cursor.execute(f'UPDATE V_Exercicio_generico SET {campo_json} = %s WHERE cod_exercicio = %s', (novo_valor, cod_exercicio)) # coluna_bd trocado por campo_json

    minhaConexaoSql.commit()

    return jsonify({'mensagem': 'Exercicio generico atualizado com sucesso.'}), 200

# DELETE Exercicio_generico
@api.route('/exercicio_generico/<int:cod_exercicio>', methods=['DELETE'])
def excluirExercicioGenerico(cod_exercicio):
    cursor.execute("SELECT * FROM V_Exercicio_generico WHERE cod_exercicio = %s", (cod_exercicio,))
    registro = cursor.fetchone()

    if registro is None:
        return jsonify({'mensagem': 'Exercicio generico não encontrado.'}), 404
    
    cursor.execute("DELETE FROM Exercicio_generico WHERE cod_exercicio = %s", (cod_exercicio,))
    minhaConexaoSql.commit()

    return jsonify({'mensagem': 'Exercicio generico excluído com sucesso.'}), 200

# READ Lista_treinos
@api.route('/lista_treinos')
def obterTodosListaTreinos():
    cursor.execute('SELECT * FROM Lista_treinos')
    registros = cursor.fetchall()

    registros_json = []
    for registro in registros:
        registro_json = {
            'cod_lista_treinos': registro[0],
            'nome': registro[1],
            'cod_usuario': registro[2]
        }
        registros_json.append(registro_json)
    
    return jsonify(registros_json)

# READ Lista_treinos (única)
@api.route('/lista_treinos/<int:cod_lista_treinos>', methods=['GET'])
def obterUmaListaTreinos(cod_lista_treinos):
    cursor.execute("SELECT * FROM Lista_treinos WHERE cod_lista_treinos = %s", (cod_lista_treinos,))
    registro = cursor.fetchone()

    if registro is None:
        return jsonify({'mensagem': 'Lista de treinos não encontrada.'}), 404
    
    lista_treinos = {
        'cod_lista_treinos': registro[0],
        'nome': registro[1],
        'cod_usuario': registro[2]
    }

    return jsonify(lista_treinos)

# READ Lista_treinos (obter Lista_treinos por cod_usuario)
@api.route('/lista_treinos/por_aluno/<int:cod_usuario>', methods=['GET'])
def obterListaTreinosPorAluno(cod_usuario):

    # Verifica se o cod_usuario existe no BD
    cursor.execute("SELECT * FROM Usuario WHERE cod_usuario = %s", (cod_usuario,))
    registro_usuario = cursor.fetchone()

    if registro_usuario is None:
        return jsonify({'mensagem': 'Usuário não encontrado.'}), 404

    cursor.execute('SELECT * FROM Lista_treinos WHERE cod_usuario = %s', (cod_usuario, ))

    if cursor.rowcount == 0:
        return jsonify([])  # Retorna uma lista vazia se não houver registros
    
    registros = cursor.fetchall()

    registros_json = []
    for registro in registros:
        registro_json = {
            'cod_lista_treinos': registro[0],
            'nome': registro[1],
            'cod_usuario': registro[2]
        }
        registros_json.append(registro_json)
    
    return jsonify(registros_json)

# CREATE Lista_treinos
@api.route('/lista_treinos', methods=['POST'])
def adicionarListaTreinos():
    dados = request.get_json()

    if 'nome' not in dados:
        return jsonify({'mensagem': 'Campos obrigatórios não fornecidos.'}), 400
    elif dados['cod_usuario'] != None:
        # Verifica se o cod_usuario existe no BD
        cursor.execute('SELECT * FROM Usuario WHERE cod_usuario=%s', (dados['cod_usuario'],))
        registro_usuario = cursor.fetchone()
        if registro_usuario == None:
            return jsonify({'mensagem': 'Usuário não encontrado.'}), 404
    
    nome = dados['nome']
    cod_usuario = dados['cod_usuario']
    cursor.execute('INSERT INTO Lista_treinos (nome, cod_usuario) VALUES (%s, %s)', (nome, cod_usuario))
    minhaConexaoSql.commit()
    return jsonify({'mensagem':'Lista de treinos cadastrada com sucesso.'})

# UPDATE Lista_treinos
@api.route('/lista_treinos/<int:cod_lista_treinos>', methods=['PUT'])
def editarListaTreinos(cod_lista_treinos):
    cursor.execute('SELECT * FROM Lista_treinos WHERE cod_lista_treinos=%s', (cod_lista_treinos,))
    registro = cursor.fetchone()

    if registro is None:
        return jsonify({'mensagem': 'Lista de treinos não encontrada.'}), 404
    else:
        dados = request.get_json()
        if 'cod_usuario' in dados and dados['cod_usuario'] != None:
            # Verifica se o cod_usuario existe no BD
            cursor.execute("SELECT * FROM Usuario WHERE cod_usuario = %s", (dados['cod_usuario'],))
            registro_usuario = cursor.fetchone()
            if registro_usuario is None:
                return jsonify({'mensagem': 'Usuário não encontrado.'}), 404

    # Mapeamento dos campos do JSON para as colunas do banco de dados
    campos_para_atualizar = {
        'nome': registro[0],
        'cod_usuario': registro[1]
    }
    for campo_json, valor in campos_para_atualizar.items():
        if campo_json in dados:
            novo_valor = dados[campo_json]
            cursor.execute(f'UPDATE Lista_treinos SET {campo_json} = %s WHERE cod_lista_treinos = %s', (novo_valor, cod_lista_treinos)) # coluna_bd trocado por campo_json
    minhaConexaoSql.commit()
    return jsonify({'mensagem': 'Lista de treinos atualizada com sucesso.'}), 200

# DELETE Lista_treinos
@api.route('/lista_treinos/<int:cod_lista_treinos>', methods=['DELETE'])
def excluirListaTreinos(cod_lista_treinos):
    cursor.execute("SELECT * FROM Lista_treinos WHERE cod_lista_treinos = %s", (cod_lista_treinos,))
    registro = cursor.fetchone()

    if registro is None:
        return jsonify({'mensagem': 'Lista de treinos não encontrada.'}), 404
    
    cursor.execute("DELETE FROM Lista_treinos WHERE cod_lista_treinos = %s", (cod_lista_treinos,))
    minhaConexaoSql.commit()

    return jsonify({'mensagem': 'Lista de treinos excluída com sucesso.'}), 200

# CREATE Treino
@api.route('/treino', methods=['POST'])
def cadastrarTreino():
    dados = request.get_json()

    if 'nome' not in dados or 'cod_lista_treinos' not in dados:
        return jsonify({'mensagem': 'Campos obrigatórios não fornecidos.'}), 400
    else:
        # Verifica se o cod_lista_treinos existe no BD
        cursor.execute("SELECT * FROM Lista_treinos WHERE cod_lista_treinos = %s", (dados['cod_lista_treinos'],))
        registro_lista_treinos = cursor.fetchone()

        if registro_lista_treinos is None:
            return jsonify({'mensagem': 'Lista de treinos não encontrada.'}), 404

    nome = dados['nome']
    cod_lista_treinos = dados['cod_lista_treinos']

    cursor.execute("INSERT INTO Treino (nome, cod_lista_treinos) VALUES (%s,%s)", (nome, cod_lista_treinos))
    minhaConexaoSql.commit()

    return jsonify({'mensagem': 'Treino cadastrado com sucesso.'}), 201

# READ treino
@api.route('/treino')
def obterTodosTreino():
    cursor.execute('SELECT * FROM Treino')
    registros = cursor.fetchall()

    registros_json = []
    for registro in registros:
        registro_json = {
            'cod_treino': registro[0],
            'nome': registro[1],
            'cod_lista_treino': registro[2]
        }
        registros_json.append(registro_json)
    
    return jsonify(registros_json)

# READ treino (único)
@api.route('/treino/<int:cod_treino>', methods=['GET'])
def obterUmTreino(cod_treino):
    cursor.execute("SELECT * FROM Treino WHERE cod_treino = %s", (cod_treino,))
    registro = cursor.fetchone()

    if registro is None:
        return jsonify({'mensagem': 'Treino não encontrado.'}), 404
    
    treino = {
        'cod_treino':registro[0],
        'nome': registro[1],
        'cod_lista_treinos': registro[2]
    }

    return jsonify(treino)

# READ Treino (obter Treino por cod_lista_treino)
@api.route('/treino/por_lista_treinos/<int:cod_lista_treinos>', methods=['GET'])
def obterTreinoPorListaTreinos(cod_lista_treinos):

    # Verifica se o cod_lista_treinos existe no BD
    cursor.execute("SELECT * FROM Lista_treinos WHERE cod_lista_treinos = %s", (cod_lista_treinos,))
    registro_usuario = cursor.fetchone()

    if registro_usuario is None:
        return jsonify({'mensagem': 'Lista de treinos não encontrada.'}), 404

    cursor.execute('SELECT * FROM Treino WHERE cod_lista_treinos = %s', (cod_lista_treinos, ))

    if cursor.rowcount == 0:
        return jsonify([])  # Retorna uma lista vazia se não houver registros
    
    registros = cursor.fetchall()

    registros_json = []
    for registro in registros:
        registro_json = {
            'cod_treino': registro[0],
            'nome': registro[1],
            'cod_lista_treino': registro[2]
        }
        registros_json.append(registro_json)
    
    return jsonify(registros_json)

# UPDATE treino
@api.route('/treino/<int:cod_treino>', methods=['PUT'])
def atualizarTreino(cod_treino):
    cursor.execute("SELECT * FROM Treino WHERE cod_treino = %s", (cod_treino,))
    registro = cursor.fetchone()

    if registro is None:
        return jsonify({'mensagem': 'Treino não encontrado.'}), 404
    else:
        dados = request.get_json()
        if 'cod_lista_treinos' in dados:
            # Verifica se o cod_lista_treinos existe no BD
            cursor.execute("SELECT * FROM Lista_treinos WHERE cod_lista_treinos = %s", (dados['cod_lista_treinos'],))
            registro_lista_treinos = cursor.fetchone()
            if registro_lista_treinos is None:
                return jsonify({'mensagem': 'Lista de Treinos não encontrada.'}), 404

    # Mapeamento dos campos do JSON para as colunas do banco de dados
    campos_para_atualizar = {
        'nome': registro[0],
        'cod_lista_treinos': registro[1]
    }

    for campo_json, valor in campos_para_atualizar.items():
        if campo_json in dados:
            novo_valor = dados[campo_json]
            cursor.execute(f'UPDATE Treino SET {campo_json} = %s WHERE cod_treino = %s', (novo_valor, cod_treino)) # coluna_bd trocado por campo_json

    minhaConexaoSql.commit()

    return jsonify({'mensagem': 'Treino atualizado com sucesso.'}), 200

# DELETE Treino
@api.route('/treino/<int:cod_treino>', methods=['DELETE'])
def excluirTreino(cod_treino):
    cursor.execute("SELECT * FROM Treino WHERE cod_treino = %s", (cod_treino,))
    registro = cursor.fetchone()

    if registro is None:
        return jsonify({'mensagem': 'Treino não encontrado.'}), 404
    
    cursor.execute("DELETE FROM Treino WHERE cod_treino = %s", (cod_treino,))
    minhaConexaoSql.commit()

    return jsonify({'mensagem': 'Treino excluído com sucesso.'}), 200


# CREATE Exercicio_treino
@api.route('/exercicio_treino', methods=['POST'])
def cadastrarExercicioTreino():
    dados = request.get_json()

    if 'series' not in dados or 'repeticoes' not in dados or 'cod_treino' not in dados or 'cod_exercicio' not in dados:
        return jsonify({'mensagem': 'Campos obrigatórios não fornecidos.'}), 400
    
    # Verifica se o cod_treino existe no BD
    cursor.execute("SELECT * FROM Treino WHERE cod_treino = %s", (dados['cod_treino'],))
    registro_treino = cursor.fetchone()

    if registro_treino is None:
        return jsonify({'mensagem': 'Treino não encontrado.'}), 404
        
    # Verifica se o cod_exercicio existe no BD
    cursor.execute("SELECT * FROM Exercicio_generico WHERE cod_exercicio = %s", (dados['cod_exercicio'],))
    registro_exercicio = cursor.fetchone()

    if registro_exercicio is None:
        return jsonify({'mensagem': 'Exercicio não encontrado.'}), 404
    
    if 'series' in dados and type(dados['series']) == str:
        if dados['series'].strip() == '':
            dados['series'] = None

    if 'repeticoes' in dados and type(dados['repeticoes']) == str:
        if dados['repeticoes'].strip() == '':
            dados['repeticoes'] = None

    if 'cod_treino' in dados and type(dados['cod_treino']) == str:
        if dados['cod_treino'].strip() == '':
            dados['cod_treino'] = None

    if 'cod_exercicio' in dados and type(dados['cod_exercicio']) == str:
        if dados['cod_exercicio'].strip() == '':
            dados['cod_exercicio'] = None

    if 'observacao' in dados and type(dados['observacao']) == str:
        if dados['observacao'].strip() == '':
            dados['observacao'] = None


    series = dados['series']
    repeticoes = dados['repeticoes']
    observacao = dados['observacao']
    cod_treino = dados['cod_treino']
    cod_exercicio = dados['cod_exercicio']

    cursor.execute("INSERT INTO Exercicio_treino (series, repeticoes, observacao, cod_treino, cod_exercicio) VALUES (%s, %s, %s, %s, %s)", (series, repeticoes, observacao, cod_treino, cod_exercicio))
    minhaConexaoSql.commit()

    return jsonify({'mensagem': 'Exercicio cadastrado com sucesso.'}), 201

# READ Exercicio_treino
@api.route('/exercicio_treino')
def obterTodosExercicioTreino():
    cursor.execute('SELECT * FROM Exercicio_treino')
    registros = cursor.fetchall()

    registros_json = []
    for registro in registros:
        registro_json = {
            'cod_exercicio_treino': registro[0],
            'series': registro[1],
            'repeticoes': registro[2],
            'observacao': registro[3],
            'cod_treino': registro[4],
            'cod_exercicio': registro[5]
        }
        registros_json.append(registro_json)
    
    return jsonify(registros_json)

# READ exercicio_treino (único)
@api.route('/exercicio_treino/<int:cod_exercicio_treino>', methods=['GET'])
def obterUmExercicioTreino(cod_exercicio_treino):
    cursor.execute("SELECT * FROM Exercicio_treino WHERE cod_exercicio_treino = %s", (cod_exercicio_treino,))
    registro = cursor.fetchone()

    if registro is None:
        return jsonify({'mensagem': 'Exercício não encontrado.'}), 404
    
    exercicio_treino = {
        'cod_exercicio_treino': registro[0],
        'series': registro[1],
        'repeticoes': registro[2],
        'observacao': registro[3],
        'cod_treino': registro[4],
        'cod_exercicio': registro[5]
    }

    return jsonify(exercicio_treino)

# READ exercicio_treino (obter Exercicio_treino por cod_treino)
@api.route('/exercicio_treino/por_treino/<int:cod_treino>', methods=['GET'])
def obterExercicioTreinoPorTreino(cod_treino):

    # Verifica se o cod_treino existe no BD
    cursor.execute("SELECT * FROM Treino WHERE cod_treino = %s", (cod_treino,))
    registro_usuario = cursor.fetchone()

    if registro_usuario is None:
        return jsonify({'mensagem': 'Treino não encontrado.'}), 404

    cursor.execute("""SELECT eg.aparelho, gm.nome as nome_grupo_musculo, eg.nome, et.*
        FROM Exercicio_treino AS et 
        INNER JOIN Exercicio_generico AS eg
        ON et.cod_exercicio = eg.cod_exercicio
        INNER JOIN Grupo_musculo AS gm
        ON eg.cod_grupo_musculo = gm.cod_grupo_musculo
        WHERE et.cod_treino = %s;""", (cod_treino,))

    if cursor.rowcount == 0:
        return jsonify([])  # Retorna uma lista vazia se não houver registros
    
    registros = cursor.fetchall()

    registros_json = []
    for registro in registros:
        registro_json = {
            'aparelho': registro[0],
            'nome_grupo_musculo': registro[1],
            'nome': registro[2],
            'cod_exercicio_treino': registro[3],
            'series': registro[4],
            'repeticoes': registro[5],
            'observacao': registro[6],
            'cod_treino': registro[7],
            'cod_exercicio': registro[8]
        }
        registros_json.append(registro_json)
    
    return jsonify(registros_json)

# UPDATE Exercicio_treino
@api.route('/exercicio_treino/<int:cod_exercicio_treino>', methods=['PUT'])
def atualizarExercicioTreino(cod_exercicio_treino):
    cursor.execute("SELECT * FROM Exercicio_treino WHERE cod_exercicio_treino = %s", (cod_exercicio_treino,))
    registro = cursor.fetchone()

    if registro is None:
        return jsonify({'mensagem': 'Exercício não encontrado.'}), 404
    
    dados = request.get_json()
    if 'cod_treino' in dados:
        # Verifica se o cod_treino existe no BD
        cursor.execute("SELECT * FROM Treino WHERE cod_treino = %s", (dados['cod_treino'],))
        registro_treino = cursor.fetchone()
        if registro_treino is None:
            return jsonify({'mensagem': 'Treino não encontrado.'}), 404
    if 'cod_exercicio' in dados:
        # Verifica se o cod_exercicio existe no BD
        cursor.execute("SELECT * FROM Exercicio_generico WHERE cod_exercicio = %s", (dados['cod_exercicio'],))
        registro_exercicio = cursor.fetchone()
        if registro_exercicio is None:
            return jsonify({'mensagem': 'Exercicio não encontrado.'}), 404
        
    if 'series' in dados and type(dados['series']) == str:
        if dados['series'].strip() == '':
            dados['series'] = None

    if 'repeticoes' in dados and type(dados['repeticoes']) == str:
        if dados['repeticoes'].strip() == '':
            dados['repeticoes'] = None

    if 'cod_treino' in dados and type(dados['cod_treino']) == str:
        if dados['cod_treino'].strip() == '':
            dados['cod_treino'] = None

    if 'cod_exercicio' in dados and type(dados['cod_exercicio']) == str:
        if dados['cod_exercicio'].strip() == '':
            dados['cod_exercicio'] = None

    if 'observacao' in dados and type(dados['observacao']) == str:
        if dados['observacao'].strip() == '':
            dados['observacao'] = None

    # Mapeamento dos campos do JSON para as colunas do banco de dados
    campos_para_atualizar = {
        'series': registro[0],
        'repeticoes': registro[1],
        'observacao': registro[2],
        'cod_treino': registro[3],
        'cod_exercicio': registro[4]
    }

    for campo_json, valor in campos_para_atualizar.items():
        if campo_json in dados:
            novo_valor = dados[campo_json]
            cursor.execute(f'UPDATE Exercicio_treino SET {campo_json} = %s WHERE cod_exercicio_treino = %s', (novo_valor, cod_exercicio_treino)) # coluna_bd trocado por campo_json

    minhaConexaoSql.commit()

    return jsonify({'mensagem': 'Exercício atualizado com sucesso.'}), 200

# DELETE Exercicio_treino
@api.route('/exercicio_treino/<int:cod_exercicio_treino>', methods=['DELETE'])
def excluirExercicioTreino(cod_exercicio_treino):
    cursor.execute("SELECT * FROM Exercicio_treino WHERE cod_exercicio_treino = %s", (cod_exercicio_treino,))
    registro = cursor.fetchone()

    if registro is None:
        return jsonify({'mensagem': 'Exercício não encontrado.'}), 404
    
    cursor.execute("DELETE FROM Exercicio_treino WHERE cod_exercicio_treino = %s", (cod_exercicio_treino,))
    minhaConexaoSql.commit()

    return jsonify({'mensagem': 'Exercício excluído com sucesso.'}), 200

if __name__ == '__main__':
    api.run(port=api.config['API_PORT'])