"""
Configuração de conexão com o RabbitMQ.

Os valores podem ser sobrescritos por variáveis de ambiente
(RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USER, RABBITMQ_PASS,
RABBITMQ_VHOST), mas os defaults já batem com o docker-compose.yml
deste projeto, então "docker compose up -d" + rodar os scripts
já funciona sem configurar nada.
"""

import os

import pika


def criar_conexao_rabbitmq() -> pika.BlockingConnection:
    host = os.getenv('RABBITMQ_HOST', 'localhost')
    port = int(os.getenv('RABBITMQ_PORT', '5672'))
    user = os.getenv('RABBITMQ_USER', 'guest')
    senha = os.getenv('RABBITMQ_PASS', 'guest')
    vhost = os.getenv('RABBITMQ_VHOST', '/')

    # PlainCredentials = usuário/senha em texto puro para autenticar no
    # broker (equivalente ao login que você usa no RabbitMQ Management UI).
    credenciais = pika.PlainCredentials(user, senha)

    # ConnectionParameters agrupa tudo que é preciso para abrir a conexão:
    #   host          -> endereço do broker RabbitMQ
    #   port          -> porta do protocolo AMQP (padrão 5672; NÃO é a
    #                     porta 15672, que é do painel web)
    #   virtual_host  -> "vhost": um namespace lógico dentro do broker,
    #                     isola exchanges/filas de diferentes apps/ambientes
    #                     (o padrão "/" serve para este estudo)
    #   credentials   -> as credenciais criadas acima
    parametros = pika.ConnectionParameters(
        host=host,
        port=port,
        virtual_host=vhost,
        credentials=credenciais,
    )

    # BlockingConnection abre a conexão TCP com o broker e devolve um
    # objeto de conexão "síncrono": cada chamada (publicar, consumir etc.)
    # bloqueia a thread até o RabbitMQ responder. É o modo mais simples de
    # usar pika, ideal para scripts e estudo.
    return pika.BlockingConnection(parametros)
