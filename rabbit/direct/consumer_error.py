import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import criar_conexao_rabbitmq

connection = criar_conexao_rabbitmq()
channel = connection.channel()

exchange = 'logs_direct'
queue = 'fila_error'
binding_key = 'error'

# Mesmo padrão de consumer_info.py (ver lá o detalhe de cada parâmetro):
# exchange_declare recria/confirma a exchange, queue_declare cria a fila,
# queue_bind liga a fila à exchange usando routing_key como "binding key"
# (match exato, exigido pela exchange direct).
channel.exchange_declare(exchange=exchange, exchange_type='direct', durable=True)
channel.queue_declare(queue=queue, durable=True)
channel.queue_bind(queue=queue, exchange=exchange, routing_key=binding_key)

print(f"[{queue}] Aguardando mensagens com binding_key='{binding_key}'. CTRL+C para sair.", flush=True)


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
