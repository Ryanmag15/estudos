import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import criar_conexao_rabbitmq

connection = criar_conexao_rabbitmq()
channel = connection.channel()

exchange = 'eventos_fanout'
queue = 'fila_log'

# Mesmo padrão de consumer_email.py (ver lá o detalhe de cada parâmetro):
# cria/confirma a exchange, cria a fila e liga a fila à exchange. Fanout
# não usa routing/binding key -- toda mensagem vai para todas as filas.
channel.exchange_declare(exchange=exchange, exchange_type='fanout', durable=True)
channel.queue_declare(queue=queue, durable=True)
channel.queue_bind(queue=queue, exchange=exchange)

print(f"[{queue}] Aguardando qualquer mensagem publicada na exchange fanout. CTRL+C para sair.", flush=True)


# ch=channel, method=metadados de entrega, properties=metadados da
# mensagem, body=conteúdo em bytes.
def callback(ch, method, properties, body):
    print(f"[{queue}] body=\"{body.decode()}\"", flush=True)


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
