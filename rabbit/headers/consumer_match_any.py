"""
x-match=any -- a mensagem é roteada para esta fila se ela tiver
PELO MENOS UM dos headers exigidos: formato=pdf OU prioridade=alta.
"""

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import criar_conexao_rabbitmq

connection = criar_conexao_rabbitmq()
channel = connection.channel()

exchange = 'eventos_headers'
queue = 'fila_match_any'

# Mesmo padrão de consumer_match_all.py (ver lá o detalhe de cada
# parâmetro): cria/confirma a exchange e cria a fila.
channel.exchange_declare(exchange=exchange, exchange_type='headers', durable=True)
channel.queue_declare(queue=queue, durable=True)

# A diferença para o consumer_match_all.py é só o x-match:
#   x-match='any' -> a mensagem bate no binding se tiver PELO MENOS UM
#                    dos headers abaixo com o mesmo valor (é um "OR")
binding_args = {
    'x-match': 'any',
    'formato': 'pdf',
    'prioridade': 'alta',
}
# queue_bind(): liga a fila à exchange; routing_key é ignorada pela
# exchange headers, e arguments carrega a regra x-match + headers.
channel.queue_bind(queue=queue, exchange=exchange, routing_key='', arguments=binding_args)

print(f"[{queue}] Aguardando mensagens com formato=pdf OU prioridade=alta. CTRL+C para sair.", flush=True)


# properties.headers traz o dict de headers enviado pelo producer;
# body vem em bytes, por isso o .decode().
def callback(ch, method, properties, body):
    headers = properties.headers
    print(f"[{queue}] headers={json.dumps(headers)} body=\"{body.decode()}\"", flush=True)


# auto_ack=True -> confirma a entrega automaticamente, sem esperar ack
# manual (channel.basic_ack).
channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)

try:
    # Loop bloqueante que escuta a fila e chama callback por mensagem.
    channel.start_consuming()
except KeyboardInterrupt:
    # CTRL+C -> sai do loop de forma limpa antes de fechar a conexão.
    channel.stop_consuming()

connection.close()
