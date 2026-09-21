"""
Cada consumer deste lab declara sua própria topologia (idempotente): pode
ser iniciado antes ou depois do producer sem dar erro.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import criar_conexao_rabbitmq

connection = criar_conexao_rabbitmq()
channel = connection.channel()

exchange = 'logs_direct'
queue = 'fila_info'
binding_key = 'info'

# exchange_declare() cria a exchange (ou confirma que já existe). O
# consumer declara a MESMA exchange que o producer -- não importa quem
# roda primeiro, o resultado final é idêntico (operação idempotente).
#   exchange_type='direct' -> roteia por match EXATO entre a routing_key
#                              da mensagem e a binding_key da fila
#   durable=True            -> sobrevive a um restart do broker
channel.exchange_declare(exchange=exchange, exchange_type='direct', durable=True)

# queue_declare() cria a fila que vai efetivamente armazenar as mensagens
# até este consumer buscá-las.
#   queue         -> nome da fila
#   durable=True  -> a fila (e as mensagens persistentes nela) sobrevive
#                    a um restart do broker
channel.queue_declare(queue=queue, durable=True)

# queue_bind() liga a fila à exchange, dizendo qual regra de roteamento
# ela aceita (o "binding").
#   queue        -> a fila sendo ligada
#   exchange     -> a exchange de origem
#   routing_key  -> aqui funciona como "binding key": na exchange direct,
#                   só chega a esta fila mensagem cuja routing_key seja
#                   EXATAMENTE IGUAL a este valor ('info')
channel.queue_bind(queue=queue, exchange=exchange, routing_key=binding_key)

print(f"[{queue}] Aguardando mensagens com binding_key='{binding_key}'. CTRL+C para sair.", flush=True)


# callback é a função que o pika chama automaticamente para cada mensagem
# entregue a esta fila.
#   ch          -> o channel (mesma conexão/canal usado acima)
#   method      -> metadados de entrega; usamos method.routing_key para
#                  ver com qual routing key a mensagem foi publicada
#   properties  -> os BasicProperties enviados pelo producer (headers,
#                  delivery_mode etc.)
#   body        -> o conteúdo da mensagem, em bytes (por isso .decode())
def callback(ch, method, properties, body):
    routing_key_recebida = method.routing_key
    print(f"[{queue}] routing_key='{routing_key_recebida}' body=\"{body.decode()}\"", flush=True)


# basic_consume() registra o callback para ser chamado a cada mensagem
# que chegar nesta fila.
#   queue               -> de qual fila consumir
#   on_message_callback -> a função a ser chamada por mensagem recebida
#   auto_ack=True       -> o RabbitMQ dá a mensagem como entregue (e a
#                          remove da fila) assim que ela é enviada ao
#                          consumer, sem esperar confirmação manual. Mais
#                          simples para estudo, mas arriscado em produção:
#                          se o consumer cair no meio do processamento, a
#                          mensagem é perdida (o correto seria auto_ack
#                          =False + channel.basic_ack manual).
channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)

try:
    # start_consuming() entra num loop bloqueante: o script fica
    # "escutando" a fila e disparando o callback para cada mensagem que
    # chegar, até ser interrompido.
    channel.start_consuming()
except KeyboardInterrupt:
    # CTRL+C gera KeyboardInterrupt; stop_consuming() sai do loop de forma
    # limpa antes de fechar a conexão.
    channel.stop_consuming()

connection.close()
