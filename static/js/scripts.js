/* Obtêm o endereço e a porta da API definidos no header */
var apiHost = document.querySelector('meta[name="api-host"]').getAttribute('content')
var apiPort = document.querySelector('meta[name="api-port"]').getAttribute('content')

/* Função para buscar exercícios da API */
async function fetchExercicios(codGrupoMusculo) {
    try {
        const response = await fetch(apiHost + ':' + apiPort + `/exercicio_generico/por_grupo_musculo/${codGrupoMusculo}`);
        const exercicios = await response.json();
        return exercicios;
    } catch (error) {
        console.error(error);
        throw new Error("Erro ao obter exercícios do Grupo Muscular.");
    }
}

/* Função para buscar grupos musculares da API */
async function fetchGruposMusculares() {
    try {
        const response = await fetch(apiHost + ':' + apiPort + '/grupo_musculo');
        const gruposMusculares = await response.json();
        return gruposMusculares;
    } catch (error) {
        console.error(error);
        throw new Error("Erro ao obter Grupos Musculares.");
    }
}

/* Função para montar os dados obtidos nas funções "fetchGruposMusculares" e "fetchExercicios" */
/* Foram utilizadas funções assíncronas para carregar o conteúdo, pois funções normais (sícronas)
não estavam funcionando bem, exercícios apareciam em outros grupos musculares, por exemplo. */
async function exibirGruposMusculares() {
    try {
        const gruposMusculares = await fetchGruposMusculares();
        const listaGrupoMusculo = document.querySelector('#lista-grupo-musculo');

        for (const grupoMuscular of gruposMusculares) {
            const ulId = `lista-exercicio-generico-${grupoMuscular.cod_grupo_musculo}`;
            listaGrupoMusculo.innerHTML +=
                `   
                    <li class="grupo-musculo">
                        <div class="opcoes-grupo-musculo">
                            <h2>• ${grupoMuscular.nome}</h2>
                            <div class="botao-opcoes-group">
                                <a href="exercicios/adicionar/exercicio_generico/${grupoMuscular.cod_grupo_musculo}"><button class="botao-adicionar"><i
                                        class="fi fi-rr-plus"></i></button></a>
                                <a href="/exercicios/confirmacao-editar/grupo_musculo/${grupoMuscular.cod_grupo_musculo}"><button class="botao-editar"><i
                                    class="fi fi-rr-pencil"></i></button></a>
                                <a href="/exercicios/confirmacao-excluir/grupo_musculo/${grupoMuscular.cod_grupo_musculo}"><button class="botao-excluir"><i
                                    class="fi fi-rr-trash"></i></button></a>
                            </div>
                        </div>
                        <ul id="lista-exercicio-generico-${grupoMuscular.cod_grupo_musculo}">

                        </ul>
                    </li>
                `;

            const exercicios = await fetchExercicios(grupoMuscular.cod_grupo_musculo);
            const listaExercicios = document.querySelector(`#lista-exercicio-generico-${grupoMuscular.cod_grupo_musculo}`);

            for (const exercicio of exercicios) {
                if (exercicio.aparelho == null) {
                    listaExercicios.innerHTML +=
                        `
                        <li class="opcoes-exercicio">
                                <a href="/exercicios/editar/exercicio_generico/${exercicio.cod_exercicio}"><button class="botao-editar"><i class="fi fi-rr-pencil"></i></button></a>
                                <a href="/exercicios/confirmacao-excluir/exercicio_generico/${exercicio.cod_exercicio}"><button class="botao-excluir"><i class="fi fi-rr-trash"></i></button></a>
                                ${exercicio.nome}
                        </li>
                    `;
                } else {
                    listaExercicios.innerHTML +=
                        `
                        <li class="opcoes-exercicio">
                                <a href="/exercicios/editar/exercicio_generico/${exercicio.cod_exercicio}"><button class="botao-editar"><i class="fi fi-rr-pencil"></i></button></a>
                                <a href="/exercicios/confirmacao-excluir/exercicio_generico/${exercicio.cod_exercicio}"><button class="botao-excluir"><i class="fi fi-rr-trash"></i></button></a>
                                [${exercicio.aparelho}]${exercicio.nome}
                        </li>
                    `;
                }
            }
        }
    } catch (error) {
        console.log(error.message);
        alert("Ocorreu um erro ao carregar os Exercícios.")
    }
}

/* Chama a função após a página ser completamente carregada */
document.addEventListener("DOMContentLoaded", function () {
    /* A função só é executada na rota /exercicios */
    if (window.location.pathname === '/exercicios') {
        exibirGruposMusculares();
    }
});


// Função para ordenar os elementos com base no nome
function ordenarElementosPorNome(a, b) {
    var nomeA = a.querySelector('h2').innerText.toUpperCase();
    var nomeB = b.querySelector('h2').innerText.toUpperCase();

    if (nomeA < nomeB) {
        return -1;
    }
    if (nomeA > nomeB) {
        return 1;
    }
    return 0;
}

// Função para ordenar a lista de grupo_musculo
function ordenarGrupoMusculo() {

    var listaGrupoMusculo = document.getElementById('lista-grupo-musculo');
    var elementosArray = Array.from(listaGrupoMusculo.children);

    // Ordena a array de elementos
    elementosArray.sort(ordenarElementosPorNome);

    // Remove todos os elementos da lista HTML
    while (listaGrupoMusculo.firstChild) {
        listaGrupoMusculo.removeChild(listaGrupoMusculo.firstChild);
    }

    // Adiciona os elementos ordenados de volta à lista HTML
    elementosArray.forEach(function (elemento) {
        listaGrupoMusculo.appendChild(elemento);
    });
}

/* Função para buscar registros de exercicios cadastrados em treinos na API */
async function fetchExerciciosTreinos(cod_treino) {
    try {
        const response = await fetch(apiHost + ':' + apiPort + `/exercicio_treino/por_treino/${cod_treino}`);
        const exercicios = await response.json();
        return exercicios;
    } catch (error) {
        console.error(error);
        throw new Error("Erro ao obter exercícios do treino.");
    }
}

/* Função para buscar treinos na API */
async function fetchTreinos(cod_lista_treinos) {
    try {
        const response = await fetch(apiHost + ':' + apiPort + `/treino/por_lista_treinos/${cod_lista_treinos}`);
        const treinos = await response.json();
        return treinos;
    } catch (error) {
        console.error(error);
        throw new Error("Erro ao obter treinos da lista de treinos.");
    }
}

/* Função para buscar listas de treinos na API */
async function fetchListasTreinos() {
    try {
        const response = await fetch(apiHost + ':' + apiPort + '/lista_treinos');
        const lista_treinos = await response.json();
        return lista_treinos;
    } catch (error) {
        console.error(error);
        throw new Error("Erro ao obter lista de treinos.");
    }
}

/* Função para montar as Listas de treinos, Treinos e Exercícios */
async function exibirListaTreinos() {
    try {

        const listas_treinos = await fetchListasTreinos();
        const lista_lista_treinos = document.querySelector('ul#lista-lista_treinos');     // Tag que reúne todas as "Listas de Treinos"

        for (const lista_treinos of listas_treinos) {
            lista_lista_treinos.innerHTML +=
                `   
                <div class="opcoes-lista-treino">
                    <h2 class="nome-lista-treino">${lista_treinos.nome}</h2>
                    <div class="botao-opcoes-group">
                        <a href="/treinos/adicionar/treino/${lista_treinos.cod_lista_treinos}"><button class="botao-adicionar"><i
                            class="fi fi-rr-plus"></i></button></a>
                        <a href="/treinos/editar/lista_treinos/${lista_treinos.cod_lista_treinos}"><button class="botao-editar"><i
                            class="fi fi-rr-pencil"></i></button></a>
                        <a href="/treinos/confirmacao-excluir/lista_treinos/${lista_treinos.cod_lista_treinos}"><button class="botao-excluir"><i
                            class="fi fi-rr-trash"></i></button></a>
                    </div>
                </div>
                <div class="lista-treino" id="lista-treino-${lista_treinos.cod_lista_treinos}"></div>
                `;

            const treinos = await fetchTreinos(lista_treinos.cod_lista_treinos);
            const lista_treino = document.querySelector(`#lista-treino-${lista_treinos.cod_lista_treinos}`);    // Tag que reúne todos os treinos de cada "Lista de Treinos"

            for (const um_treino of treinos) {

                lista_treino.innerHTML +=
                    `
                    <div class="treino">
                        <div class="opcoes-treino">
                            <h2>• ${um_treino.nome}</h2>
                            <div class="botao-opcoes-group">
                                <a href="/treinos/adicionar/exercicio_treino/${um_treino.cod_treino}"><button class="botao-adicionar"><i
                                    class="fi fi-rr-plus"></i></button></a>
                                <a href="/treinos/editar/treino/${um_treino.cod_treino}"><button class="botao-editar"><i
                                    class="fi fi-rr-pencil"></i></button></a>
                                <a href="/treinos/confirmacao-excluir/treino/${um_treino.cod_treino}"><button class="botao-excluir"><i
                                    class="fi fi-rr-trash"></i></button></a>
                            </div>
                        </div>
                        <ul id="lista-exercicio-treino-${um_treino.cod_treino}"></ul>
                    </div>
                    `;

                const exercicios_treinos = await fetchExerciciosTreinos(um_treino.cod_treino);
                const treino = document.querySelector(`#lista-exercicio-treino-${um_treino.cod_treino}`);    // Tag que reúne todos os exercícios de cada "Treino"

                for (const exercicio_treino of exercicios_treinos) {
                    if (exercicio_treino.observacao == null) {exercicio_treino.observacao = ''} /* Caso o exercício não tenha observações, não é exibido "null" */
                    if (exercicio_treino.aparelho != null) {
                        if (exercicio_treino.series != null || exercicio_treino.repeticoes != null) {
                            treino.innerHTML +=
                                `
                                <div class="opcoes-exercicio">
                                    <a href="/treinos/editar/exercicio_treino/${exercicio_treino.cod_exercicio_treino}"><button class="botao-editar"><i
                                            class="fi fi-rr-pencil"></i></button></a>
                                    <a href="/treinos/confirmacao-excluir/exercicio_treino/${exercicio_treino.cod_exercicio_treino}"><button class="botao-excluir"><i
                                            class="fi fi-rr-trash"></i></button></a>
                                    <div>
                                        <li>[${exercicio_treino.aparelho}] ${exercicio_treino.nome_grupo_musculo} ${exercicio_treino.nome} (${exercicio_treino.series}x${exercicio_treino.repeticoes})</li>
                                        <p>${exercicio_treino.observacao}</p>
                                    </div>
                                </div>
                            `;
                        } else {
                            treino.innerHTML +=
                                `
                                <div class="opcoes-exercicio">
                                    <a href="/treinos/editar/exercicio_treino/${exercicio_treino.cod_exercicio_treino}"><button class="botao-editar"><i
                                            class="fi fi-rr-pencil"></i></button></a>
                                    <a href="/treinos/confirmacao-excluir/exercicio_treino/${exercicio_treino.cod_exercicio_treino}"><button class="botao-excluir"><i
                                            class="fi fi-rr-trash"></i></button></a>
                                    <div>
                                        <li>[${exercicio_treino.aparelho}] ${exercicio_treino.nome_grupo_musculo} ${exercicio_treino.nome}</li>
                                        <p>${exercicio_treino.observacao}</p>
                                    </div>
                                </div>
                            `;
                        }
                    } else {
                        if (exercicio_treino.series != null || exercicio_treino.repeticoes != null) {
                            treino.innerHTML +=
                                `
                                <div class="opcoes-exercicio">
                                    <a href="/treinos/editar/exercicio_treino/${exercicio_treino.cod_exercicio_treino}"><button class="botao-editar"><i
                                            class="fi fi-rr-pencil"></i></button></a>
                                    <a href="/treinos/confirmacao-excluir/exercicio_treino/${exercicio_treino.cod_exercicio_treino}"><button class="botao-excluir"><i
                                            class="fi fi-rr-trash"></i></button></a>
                                    <div>
                                        <li>${exercicio_treino.nome_grupo_musculo} ${exercicio_treino.nome} (${exercicio_treino.series}x${exercicio_treino.repeticoes})</li>
                                        <p>${exercicio_treino.observacao}</p>
                                    </div>
                                </div>
                            `;
                        } else {
                            treino.innerHTML +=
                                `
                                <div class="opcoes-exercicio">
                                    <a href="/treinos/editar/exercicio_treino/${exercicio_treino.cod_exercicio_treino}"><button class="botao-editar"><i
                                            class="fi fi-rr-pencil"></i></button></a>
                                    <a href="/treinos/confirmacao-excluir/exercicio_treino/${exercicio_treino.cod_exercicio_treino}"><button class="botao-excluir"><i
                                            class="fi fi-rr-trash"></i></button></a>
                                    <div>
                                        <li>${exercicio_treino.nome_grupo_musculo} ${exercicio_treino.nome}</li>
                                        <p>${exercicio_treino.observacao}</p>
                                    </div>
                                </div>
                            `;
                        }
                    }
                }
            }
        }
    } catch (error) {
        console.log(error.message);
        alert("Ocorreu um erro ao carregar as Lista de Treinos.")
    }
}

/* A função só é executada após a página ser carregada */
document.addEventListener("DOMContentLoaded", function () {
    /* A função funciona apenas na rota /treinos */
    if (window.location.pathname === '/treinos') {
        exibirListaTreinos();
    }
});

// Função para abrir o menu lateral
function abrirMenu() {
    var menu = document.getElementById('menu')
    var tela = window.matchMedia("width > 1280px")
    if (menu.style.width == '') { // Se a largura do menu for 0 (definido no style.css) ele abre
        document.getElementById('menu').style.width = '300px'
        if (tela.matches) {  // Se a tela for maior do que 700px, o conteúdo é empurrado
            document.getElementById('conteudo').style.marginLeft = '150px'
        }
    } else { // Se a largura do menu é maior que 0, ou seja, está aberto, ele fecha
        document.getElementById('menu').style.width = ''
        document.getElementById('conteudo').style.marginLeft = ''
    }
}

// Função para abrir os modais (Pop-ups) do usuário, contato e sobre
function openModal(x) {
    document.querySelector(x).showModal()
    if (x == '#modal-adicionar-lista-treino-existente' || x == '#modal-adicionar-nova-lista-treino') {
        document.querySelector('#modal-adicionar-lista-treino').close()
    }
}

// Função para fechar os modais (Pop-ups)
function closeModal(x) {
    document.querySelector(x).close()
}