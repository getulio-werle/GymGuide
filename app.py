from flask import Flask
from flask import jsonify, request, render_template, redirect
from config import Config
import requests


app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)

# Abrir página login
@app.route('/')
@app.route('/login')
def abrirLogin():
    return render_template('login.html')

# Abrir página home_instrutor
@app.route('/home_instrutor')
def abrirHomeInstrutor():
    return render_template('home_instrutor.html')

# Abrir página home_aluno
@app.route('/home_aluno')
def abrirHomeAluno():
    return render_template('home_aluno.html')

# Abrir página cadastro
@app.route('/cadastro')
def abrirCadastro():
    return render_template('cadastro.html')

# Abrir página dados_usuario
@app.route('/dados_usuario')
def abrirDadosUsuario():
    return render_template('dados_usuario.html')

# Abrir página atualizar_pagamento
@app.route('/atualizar_pagamento')
def abrirAtualizarPagamento():
    return render_template('atualizar_pagamento.html')

# Abrir página meus_dados_aluno
@app.route('/meus_dados_aluno')
def abrirMeusDadosAluno():
    return render_template('meus_dados_aluno.html')

# Abrir página meus_dados_instrutor
@app.route('/meus_dados_instrutor')
def abrirMeusDadosInstrutor():
    return render_template('meus_dados_instrutor.html')

# Abrir página meus_treinos
@app.route('/meus_treinos')
def abrirMeusTreinos():
    return render_template('meus_treinos.html')

# Abrir página consulta
@app.route('/consulta')
def abrirConsulta():
    return render_template('consulta.html')

# Abrir página exercicios
@app.route('/exercicios')
def abrirExercicios():
    return render_template('exercicios.html')

# Abrir página treinos
@app.route('/treinos')
def abrirTreinos():
    return render_template('treinos.html')

# Adicionar exercicio_generico
@app.route('/exercicios/adicionar/exercicio_generico/<int:id>', methods=['GET', 'POST'])
def adicionarExercicioGenerico(id):
    if request.method == 'GET':
        url = f"http://localhost:8080/grupo_musculo/{id}"
        grupo_musculo = requests.get(url)
        grupo_musculo = grupo_musculo.json()
        return render_template('exercicios.html', grupo_musculo_para_adicionar_exercicio=grupo_musculo, operacao='adicionar')
    else:
        nome = request.form.get("nome-exercicio-generico-adicionar")
        aparelho = request.form.get("aparelho-exercicio-generico-adicionar")
        cod_grupo_musculo = request.form.get("cod-grupo-musculo-exercicio-generico-adicionar")
        if aparelho.strip() == '':
            aparelho = None
        else:
            aparelho = int(aparelho)
        if cod_grupo_musculo.strip() == '':
            cod_grupo_musculo = None
        else:
            cod_grupo_musculo = int(cod_grupo_musculo)

        exercicio_generico = {
            'nome': nome,
            'aparelho': aparelho,
            'cod_grupo_musculo': cod_grupo_musculo
        }
        exercicio_generico = jsonify(exercicio_generico).get_data(as_text=True)
        url = f"http://localhost:8080/exercicio_generico"
        requests.post(url, data=exercicio_generico, headers={'Content-Type': 'application/json'})
        return redirect('/exercicios')

# Editar exercicio_generico
@app.route('/exercicios/editar/exercicio_generico/<int:id>', methods=['GET', 'POST'])
def editarExercicioGenerico(id):
    if request.method == 'GET':
        url = f'http://localhost:8080/exercicio_generico/{id}'
        exercicio_generico = requests.get(url)
        exercicio_generico = exercicio_generico.json()
        return render_template('exercicios.html', exercicio_generico=exercicio_generico, operacao='editar')
    else:
        aparelho = request.form.get('aparelho-exercicio-generico-editar')
        nome = request.form.get('nome-exercicio-generico-editar')
        cod_grupo_musculo = request.form.get('cod-grupo-musculo-exercicio-generico-editar')
        if aparelho.strip() == '':
            aparelho = None
        else:
            aparelho = int(aparelho)
        if cod_grupo_musculo.strip() == '':
            cod_grupo_musculo = None
        else:
            cod_grupo_musculo = int(cod_grupo_musculo)
            

        exercicio_generico = {
            'aparelho': aparelho,
            'nome': nome,
            'cod_grupo_musculo': cod_grupo_musculo
        }
        exercicio_generico = jsonify(exercicio_generico).get_data(as_text=True)
        url = f"http://localhost:8080/exercicio_generico/{id}"
        requests.put(url, data=exercicio_generico, headers={'Content-Type': 'application/json'})
        return redirect('/exercicios')

# Abrir modal excluir exercicio_generico
@app.route('/exercicios/confirmacao-excluir/exercicio_generico/<int:id>')
def abrirModalExcluirExercicioGenerico(id):
    url = f"http://localhost:8080/exercicio_generico/{id}"
    exercicio_generico = requests.get(url)
    exercicio_generico = exercicio_generico.json()
    return render_template('exercicios.html', exercicio_generico=exercicio_generico, operacao='excluir')

# Excluir exercicio_generico
@app.route('/exercicios/excluir/exercicio_generico/<int:id>')
def excluirExercicioGenerico(id):
    url = f"http://localhost:8080/exercicio_generico/{id}"
    requests.delete(url)
    return redirect('/exercicios')

# Adicionar grupo_musculo
@app.route('/exercicios/adicionar/grupo_musculo', methods=['GET', 'POST'])
def adicionarGrupoMusculo():
    if request.method == 'GET':
        return render_template('exercicios.html', grupo_musculo=1 ,operacao='adicionar')
    else:
        nome = request.form.get('nome-grupo-musculo-adicionar')
        grupo_musculo = {
            'nome': nome
        }
        grupo_musculo = jsonify(grupo_musculo).get_data(as_text=True)
        url = 'http://localhost:8080/grupo_musculo'
        requests.post(url, data=grupo_musculo, headers={'Content-Type': 'application/json'})
        return redirect('/exercicios')


# Abrir editar grupo_musculo
@app.route('/exercicios/confirmacao-editar/grupo_musculo/<int:id>', methods=['GET', 'POST'])
def editarGrupoMusculo(id):
    if request.method == 'GET':
        url = f"http://localhost:8080/grupo_musculo/{id}"
        grupo_musculo = requests.get(url)
        grupo_musculo = grupo_musculo.json()
        return render_template('exercicios.html', grupo_musculo=grupo_musculo, operacao='editar')
    else:
        nome = request.form.get("nome-grupo-musculo-editar")
        grupo_musculo = {
            'nome': nome
        }
        grupo_musculo = jsonify(grupo_musculo).get_data(as_text=True)
        url = f"http://localhost:8080/grupo_musculo/{id}"
        requests.put(url, data=grupo_musculo, headers={'Content-Type': 'application/json'})
        return redirect('/exercicios')

# Abrir modal excluir grupo_musculo
@app.route('/exercicios/confirmacao-excluir/grupo_musculo/<int:id>')
def abrirModalExcluirGrupoMusculo(id):
    url = f"http://localhost:8080/grupo_musculo/{id}"
    grupo_musculo = requests.get(url)
    grupo_musculo = grupo_musculo.json()
    return render_template('exercicios.html', grupo_musculo=grupo_musculo, operacao='excluir')

# Excluir grupo_musculo
@app.route('/exercicios/excluir/grupo_musculo/<int:id>')
def excluirGrupoMusculo(id):
    url = f"http://localhost:8080/grupo_musculo/{id}"
    requests.delete(url)
    return redirect('/exercicios')

# Abrir modal adicionar lista_treinos
@app.route('/treinos/adicionar/lista_treinos')
def abrirModalAdicionarListaTreinos():
    return render_template('treinos.html', lista_treinos=1, operacao='adicionar')

# Abrir modal adicionar lista_treinos já existente
@app.route('/treinos/adicionar/lista_treinos/existente', methods=['GET','POST'])
def adicionarListaTreinosExistente():
    if request.method == 'GET':
        url = 'http://localhost:8080/lista_treinos'
        listas_treinos = requests.get(url)
        listas_treinos = listas_treinos.json()
        return render_template('treinos.html', lista_treinos=1, operacao='adicionar-existente', listas_treinos=listas_treinos)
    else:
        cod_lista_treinos_selecionada = request.form.get('lista-treino-existente-adicionar-lista-treino')
        # Pega os dados completos da lista de treinos
        url = f'http://localhost:8080/lista_treinos/{cod_lista_treinos_selecionada}'
        lista_treinos = requests.get(url)
        lista_treinos = lista_treinos.json()
        # Enviar uma requisição para criar
        lista_treinos = jsonify(lista_treinos).get_data(as_text=True)
        url = 'http://localhost:8080/lista_treinos'
        requests.post(url, data=lista_treinos, headers={'Content-Type': 'application/json'})
        return redirect('/treinos')
    
# Adicionar lista_treinos nova
@app.route('/treinos/adicionar/lista_treinos/nova', methods=['GET','POST'])
def adicionarListaTreinosNova():
    if request.method == 'GET':
        return render_template('treinos.html', lista_treinos=1, operacao='adicionar-nova')
    else:
        nome = request.form.get('lista-treino-adicionar-lista-treino-nova')
        lista_treinos = {
            'nome': nome,
            'cod_usuario': None
        }
        lista_treinos = jsonify(lista_treinos).get_data(as_text=True)
        url = 'http://localhost:8080/lista_treinos'
        requests.post(url, data=lista_treinos, headers={'Content-Type': 'application/json'})
        return redirect('/treinos')

# Editar lista_treinos
@app.route('/treinos/editar/lista_treinos/<int:id>', methods=['GET', 'POST'])
def editarListaTreinos(id):
    if request.method == 'GET':
        url = f'http://localhost:8080/lista_treinos/{id}'
        lista_treinos = requests.get(url)
        lista_treinos = lista_treinos.json()
        return render_template('treinos.html', lista_treinos=lista_treinos, operacao='editar')
    else:
        nome = request.form.get('nome-editar-lista-treinos')
        lista_treinos = {
            'nome': nome,
            'cod_usuario': None
        }
        lista_treinos = jsonify(lista_treinos).get_data(as_text=True)
        url = f'http://localhost:8080/lista_treinos/{id}'
        requests.put(url, data=lista_treinos, headers={'Content-Type': 'application/json'})
        return redirect('/treinos')

# Abrir modal excluir lista_treinos
@app.route('/treinos/confirmacao-excluir/lista_treinos/<int:id>')
def abrirModalExcluirListaTreinos(id):
    url = f"http://localhost:8080/lista_treinos/{id}"
    lista_treinos = requests.get(url)
    lista_treinos = lista_treinos.json()
    return render_template('treinos.html', lista_treinos=lista_treinos, operacao='excluir')

# Excluir lista_treinos
@app.route('/treinos/excluir/lista_treinos/<int:id>')
def excluirListaTreinos(id):
    url = f"http://localhost:8080/lista_treinos/{id}"
    requests.delete(url)
    return redirect('/treinos')

# Adicionar treino
@app.route('/treinos/adicionar/treino/<int:cod_lista_treinos>', methods=['GET', 'POST'])
def adicionarTreino(cod_lista_treinos):
    if request.method == 'GET':
        return render_template('treinos.html', treino=1, operacao='adicionar')
    else:
        nome = request.form.get('nome-treino-adicionar-treino')
        treino = {
            'nome': nome,
            'cod_lista_treinos': cod_lista_treinos
        }
        treino = jsonify(treino).get_data(as_text=True)
        url = 'http://localhost:8080/treino'
        requests.post(url, data=treino, headers={'Content-Type': 'application/json'})
        return redirect('/treinos')
    
# Editar treino
@app.route('/treinos/editar/treino/<int:id>', methods=['GET', 'POST'])
def editarTreino(id):
    if request.method == 'GET':
        url = f'http://localhost:8080/treino/{id}'
        treino = requests.get(url)
        treino = treino.json()
        return render_template('treinos.html', treino=treino, operacao='editar')
    else:
        nome = request.form.get('nome-treino-editar-treino')
        treino = {
            'nome': nome
        }
        treino = jsonify(treino).get_data(as_text=True)
        url = f'http://localhost:8080/treino/{id}'
        requests.put(url, data=treino, headers={'Content-Type': 'application/json'})
        return redirect('/treinos')
    
# Abrir modal excluir treino
@app.route('/treinos/confirmacao-excluir/treino/<int:id>')
def abrirModalExcluirTreinos(id):
    url = f"http://localhost:8080/treino/{id}"
    treino = requests.get(url)
    treino = treino.json()
    return render_template('treinos.html', treino=treino, operacao='excluir')

# Excluir treino
@app.route('/treinos/excluir/treino/<int:id>')
def excluirTreino(id):
    url = f"http://localhost:8080/treino/{id}"
    requests.delete(url)
    return redirect('/treinos')

# Adicionar exercicio_treino
@app.route('/treinos/adicionar/exercicio_treino/<int:cod_treino>', methods=['GET', 'POST'])
def adicionarExercicioTreino(cod_treino):
    if request.method == 'GET':
        # Obter os grupos musculares
        url = 'http://localhost:8080/grupo_musculo'
        grupos_musculos = requests.get(url)
        grupos_musculos = grupos_musculos.json()
        # Obter os exercícios dos treinos
        url = f'http://localhost:8080/exercicio_generico'
        exercicios_genericos = requests.get(url)
        exercicios_genericos = exercicios_genericos.json()
        return render_template('treinos.html', grupos_musculos=grupos_musculos, 
                               exercicios_genericos=exercicios_genericos, 
                               exercicio_treino=1, operacao='adicionar')
    else:
        cod_exercicio = request.form.get('exercicio-generico-adicionar-exercicio-treino')
        series = request.form.get('series-adicionar-exercicio-treino')
        repeticoes = request.form.get('repeticoes-adicionar-exercicio-treino')
        observacao = request.form.get('observacao-adicionar-exercicio-treino')
        if cod_exercicio.strip() == '':
            cod_exercicio = None
        else:
            cod_exercicio = int(cod_exercicio)
        if series.strip() == '':
            series = None
        else:
            series = int(series)
        if repeticoes.strip() == '':
            repeticoes = None
        else:
            repeticoes = int(repeticoes)

        exercicio_treino = {
            'series': series,
            'repeticoes': repeticoes,
            'observacao': observacao,
            'cod_treino': cod_treino,
            'cod_exercicio': cod_exercicio
        }
        exercicio_treino = jsonify(exercicio_treino).get_data(as_text=True)
        url = 'http://localhost:8080/exercicio_treino'
        requests.post(url, data=exercicio_treino, headers={'Content-Type': 'application/json'})
        return redirect('/treinos')
    
# Editar exercicio_treino
@app.route('/treinos/editar/exercicio_treino/<int:id>', methods=['GET', 'POST'])
def editarExercicioTreino(id):
    if request.method == 'GET':
        # Obter o exercicio_treino
        url = f'http://localhost:8080/exercicio_treino/{id}'
        exercicio_treino = requests.get(url)
        exercicio_treino = exercicio_treino.json()
        # Obter o exercicio_generico
        url = f'http://localhost:8080/exercicio_generico/{exercicio_treino["cod_exercicio"]}'
        exercicio_generico = requests.get(url)
        exercicio_generico = exercicio_generico.json()
        # Obter o grupo_musculo
        url = f'http://localhost:8080/grupo_musculo/{exercicio_generico["cod_grupo_musculo"]}'
        grupo_musculo = requests.get(url)
        grupo_musculo = grupo_musculo.json()
        return render_template('treinos.html', exercicio_treino=exercicio_treino, 
                               exercicio_generico_editar_exercicio_treino=exercicio_generico, grupo_musculo_editar_exercicio_treino=grupo_musculo,
                                operacao='editar')
    else:
        cod_exercicio = request.form.get('exercicio-generico-editar-exercicio-treino')
        series = request.form.get('series-editar-exercicio-treino')
        repeticoes = request.form.get('repeticoes-editar-exercicio-treino')
        observacao = request.form.get('observacao-editar-exercicio-treino')
        if cod_exercicio.strip() == '':
            cod_exercicio = None
        else:
            cod_exercicio = int(cod_exercicio)
        if series.strip() == '':
            series = None
        else:
            series = int(series)
        if repeticoes.strip() == '':
            repeticoes = None
        else:
            repeticoes = int(repeticoes)

        exercicio_treino = {
            'series': series,
            'repeticoes': repeticoes,
            'observacao': observacao,
            'cod_exercicio': cod_exercicio
        }
        exercicio_treino = jsonify(exercicio_treino).get_data(as_text=True)
        url = f'http://localhost:8080/exercicio_treino/{id}'
        requests.put(url, data=exercicio_treino, headers={'Content-Type': 'application/json'})
        return redirect('/treinos')
    
# Abrir modal excluir exercicio_treino
@app.route('/treinos/confirmacao-excluir/exercicio_treino/<int:id>')
def abrirModalExcluirExercicioTreino(id):
    url = f"http://localhost:8080/exercicio_treino/{id}"
    exercicio_treino = requests.get(url)
    exercicio_treino = exercicio_treino.json()
    print(exercicio_treino)
    # Busca do nome do cod_exercicio do exercicio_treino
    url = f"http://localhost:8080/exercicio_generico/{exercicio_treino['cod_exercicio']}"
    exercicio_generico = requests.get(url)
    exercicio_generico = exercicio_generico.json()
    nome_exercicio = exercicio_generico['nome']
    return render_template('treinos.html', nome_exercicio=nome_exercicio, exercicio_treino=exercicio_treino, operacao='excluir')

# Excluir exericio_treino
@app.route('/treinos/excluir/exercicio_treino/<int:id>')
def excluirExercicioTreino(id):
    url = f"http://localhost:8080/exercicio_treino/{id}"
    requests.delete(url)
    return redirect('/treinos')



if __name__ == "__main__": 
     app.run(port = app.config['APP_PORT'])