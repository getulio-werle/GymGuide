# Configuração da API

class Config:
    DEBUG = True
    SECRET_KEY = "gymguide"

    #DATABASE = "postgresql://seu_usuario:senha@host_do_postgres:porta/nome_do_banco"
    DATABASE = "postgresql://postgres:1234@localhost:5432/GymGuide"

    API_HOST = "http://localhost"
    API_PORT = 8080

    APP_PORT = 8081

conexao_BD1 = {
    'host': 'localhost',
    'usuario': 'postgres',
    'senha': '1234',
    'banco': 'GymGuide'
}