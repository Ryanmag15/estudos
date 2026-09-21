"""
Demonstra que uma fila pode ter MÚLTIPLOS bindings: esta fila recebe
tanto mensagens 'error' quanto 'warning', porque foi feito um
queue_bind() para cada routing key.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import criar_conexao_rabbitmq

connection = criar_conexao_rabbitmq()
channel = connection.channel()

exchange = 'logs_direct'
queue = 'fila_critical'

channel.exchange_declare(exchange=exchange, exchange_type='direct', durable=True)

# queue_declare() cria a fila (uma só, compartilhada pelos dois bindings
# abaixo).
channel.queue_declare(queue=queue, durable=True)

# Duas chamadas a queue_bind() para a MESMA fila = dois bindings
# independentes. Cada um adiciona uma regra de roteamento; eles não se
# substituem, se somam. Por isso esta fila recebe tanto 'error' quanto
# 'warning' -- é o jeito de simular "OR" numa exchange direct, que por si
# só só faz match exato de UMA routing_key por binding.
channel.queue_bind(queue=queue, exchange=exchange, routing_key='error')
channel.queue_bind(queue=queue, exchange=exchange, routing_key='warning')

print(f"[{queue}] Aguardando mensagens com routing_key='error' OU 'warning'. CTRL+C para sair.", flush=True)


# ch=channel, method=metadados de entrega (routing_key usada),
# properties=metadados da mensagem (headers, delivery_mode...),
# body=conteúdo em bytes.
def callback(ch, method, properties, body):
    routing_key_recebida = method.routing_key
    print(f"[{queue}] routing_key='{routing_key_recebida}' body=\"{body.decode()}\"", flush=True)


# auto_ack=True -> a mensagem é dada como entregue assim que chega ao
# consumer, sem confirmação manual (channel.basic_ack). Simples, mas se o
# consumer cair no meio do processamento a mensagem é perdida.
channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)

try:
    # Loop bloqueante que escuta a fila e chama callback por mensagem.
    channel.start_consuming()
except KeyboardInterrupt:
    # CTRL+C -> sai do loop de forma limpa antes de fechar a conexão.
    channel.stop_consuming()

connection.close()
