import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import criar_conexao_rabbitmq

connection = criar_conexao_rabbitmq()
channel = connection.channel()

exchange = 'eventos_fanout'
queue = 'fila_email'

# exchange_declare() cria/confirma a exchange. O consumer declara a
# MESMA exchange que o producer -- não importa quem roda primeiro
# (operação idempotente).
channel.exchange_declare(exchange=exchange, exchange_type='fanout', durable=True)

# queue_declare() cria a fila que vai armazenar as mensagens até este
# consumer buscá-las.
channel.queue_declare(queue=queue, durable=True)

# queue_bind() liga a fila à exchange. Numa fanout não existe conceito de
# routing/binding key -- toda mensagem publicada na exchange vai para
# TODAS as filas ligadas a ela, por isso aqui não passamos routing_key.
channel.queue_bind(queue=queue, exchange=exchange)

print(f"[{queue}] Aguardando qualquer mensagem publicada na exchange fanout. CTRL+C para sair.", flush=True)


# callback é chamada pelo pika para cada mensagem entregue a esta fila.
#   ch          -> o channel
#   method      -> metadados de entrega (aqui não precisamos, pois não há
#                  routing key relevante em fanout)
#   properties  -> metadados da mensagem enviados pelo producer
#   body        -> conteúdo da mensagem em bytes (por isso .decode())
def callback(ch, method, properties, body):
    print(f"[{queue}] body=\"{body.decode()}\"", flush=True)


# basic_consume() registra o callback para cada mensagem desta fila.
#   queue               -> de qual fila consumir
#   on_message_callback -> função chamada por mensagem recebida
#   auto_ack=True       -> confirma a entrega automaticamente, sem
#                          esperar um ack manual (channel.basic_ack).
#                          Simples para estudo, mas se o consumer cair no
#                          meio do processamento a mensagem é perdida.
channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)

try:
    # Loop bloqueante: fica escutando a fila e chamando callback por
    # mensagem, até ser interrompido.
    channel.start_consuming()
except KeyboardInterrupt:
    # CTRL+C -> sai do loop de forma limpa antes de fechar a conexão.
    channel.stop_consuming()

connection.close()
