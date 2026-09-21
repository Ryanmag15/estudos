"""
Binding "pedido.*" -- o "*" substitui EXATAMENTE uma palavra.
Pega: pedido.criado, pedido.aprovado, pedido.cancelado
NÃO pega: pedido.item.adicionado (tem duas palavras depois de "pedido")
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import criar_conexao_rabbitmq

connection = criar_conexao_rabbitmq()
channel = connection.channel()

exchange = 'eventos_topic'
queue = 'fila_pedidos_asterisco'
binding_key = 'pedido.*'

# exchange_declare() cria/confirma a exchange. O consumer declara a
# MESMA exchange que o producer (idempotente, não importa quem roda
# primeiro).
channel.exchange_declare(exchange=exchange, exchange_type='topic', durable=True)

# queue_declare() cria a fila que vai armazenar as mensagens até este
# consumer buscá-las.
channel.queue_declare(queue=queue, durable=True)

# queue_bind() liga a fila à exchange usando um PADRÃO como binding key
# (routing_key aqui funciona como "binding key" do lado da fila).
#   queue        -> a fila sendo ligada
#   exchange     -> a exchange de origem
#   routing_key  -> o padrão 'pedido.*' -- o '*' substitui EXATAMENTE uma
#                   palavra, então bate com 'pedido.criado',
#                   'pedido.aprovado' etc., mas NÃO com
#                   'pedido.item.adicionado' (duas palavras depois)
channel.queue_bind(queue=queue, exchange=exchange, routing_key=binding_key)

print(f"[{queue}] Aguardando mensagens que casem com '{binding_key}'. CTRL+C para sair.", flush=True)


# callback é chamada pelo pika para cada mensagem entregue a esta fila.
#   ch          -> o channel
#   method      -> metadados de entrega; usamos method.routing_key para
#                  ver a routing key exata publicada (não o padrão)
#   properties  -> metadados da mensagem enviados pelo producer
#   body        -> conteúdo da mensagem em bytes (por isso .decode())
def callback(ch, method, properties, body):
    routing_key_recebida = method.routing_key
    print(f"[{queue}] routing_key='{routing_key_recebida}' body=\"{body.decode()}\"", flush=True)


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
