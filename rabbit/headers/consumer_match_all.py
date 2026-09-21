"""
x-match=all -- a mensagem só é roteada para esta fila se ela tiver
TODOS os headers exigidos com os mesmos valores: formato=pdf E
prioridade=alta.
"""

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import criar_conexao_rabbitmq

connection = criar_conexao_rabbitmq()
channel = connection.channel()

exchange = 'eventos_headers'
queue = 'fila_match_all'

# exchange_declare() cria/confirma a exchange. O consumer declara a
# MESMA exchange que o producer (idempotente, não importa quem roda
# primeiro).
channel.exchange_declare(exchange=exchange, exchange_type='headers', durable=True)

# queue_declare() cria a fila que vai armazenar as mensagens até este
# consumer buscá-las.
channel.queue_declare(queue=queue, durable=True)

# Numa exchange headers, o "binding key" não é uma string -- é um dict de
# argumentos que o RabbitMQ compara com os headers de cada mensagem:
#   x-match='all'  -> a mensagem só bate no binding se tiver TODOS os
#                     headers abaixo com o mesmo valor
#   formato='pdf'       -> header exigido #1
#   prioridade='alta'   -> header exigido #2
binding_args = {
    'x-match': 'all',
    'formato': 'pdf',
    'prioridade': 'alta',
}

# queue_bind() liga a fila à exchange usando esses argumentos.
#   queue        -> a fila sendo ligada
#   exchange     -> a exchange de origem
#   routing_key  -> ignorada pela exchange headers; deixamos vazia
#   arguments    -> o dict acima, com a regra x-match + headers exigidos
channel.queue_bind(queue=queue, exchange=exchange, routing_key='', arguments=binding_args)

print(f"[{queue}] Aguardando mensagens com formato=pdf E prioridade=alta. CTRL+C para sair.", flush=True)


# callback é chamada pelo pika para cada mensagem entregue a esta fila.
#   ch          -> o channel
#   method      -> metadados de entrega (não usados aqui)
#   properties  -> metadados da mensagem; properties.headers traz o dict
#                  de headers que o producer enviou
#   body        -> conteúdo da mensagem em bytes (por isso .decode())
def callback(ch, method, properties, body):
    headers = properties.headers
    print(f"[{queue}] headers={json.dumps(headers)} body=\"{body.decode()}\"", flush=True)


# basic_consume() registra o callback para cada mensagem desta fila.
# auto_ack=True -> confirma a entrega automaticamente, sem esperar ack
# manual (channel.basic_ack). Simples para estudo, mas se o consumer cair
# no meio do processamento a mensagem é perdida.
channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)

try:
    # Loop bloqueante que escuta a fila e chama callback por mensagem.
    channel.start_consuming()
except KeyboardInterrupt:
    # CTRL+C -> sai do loop de forma limpa antes de fechar a conexão.
    channel.stop_consuming()

connection.close()
