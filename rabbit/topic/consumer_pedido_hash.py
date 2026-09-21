"""
Binding "pedido.#" -- o "#" substitui ZERO ou MAIS palavras.
Pega TODAS as mensagens que começam com "pedido.", não importa quantos
níveis vêm depois: pedido.criado, pedido.aprovado, pedido.cancelado
E TAMBÉM pedido.item.adicionado (2 níveis).
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import criar_conexao_rabbitmq

connection = criar_conexao_rabbitmq()
channel = connection.channel()

exchange = 'eventos_topic'
queue = 'fila_pedidos_hash'
binding_key = 'pedido.#'

# Mesmo padrão de consumer_pedido_asterisco.py (ver lá o detalhe de cada
# parâmetro): cria/confirma a exchange, cria a fila e liga a fila à
# exchange usando um padrão como binding key.
channel.exchange_declare(exchange=exchange, exchange_type='topic', durable=True)
channel.queue_declare(queue=queue, durable=True)

# Aqui o padrão é 'pedido.#': o '#' substitui ZERO OU MAIS palavras, então
# bate com 'pedido.criado' (1 palavra depois) e também com
# 'pedido.item.adicionado' (2 palavras depois) -- diferente do '*', que
# exige exatamente uma.
channel.queue_bind(queue=queue, exchange=exchange, routing_key=binding_key)

print(f"[{queue}] Aguardando mensagens que casem com '{binding_key}'. CTRL+C para sair.", flush=True)


# ch=channel, method=metadados de entrega (routing_key exata publicada),
# properties=metadados da mensagem, body=conteúdo em bytes.
def callback(ch, method, properties, body):
    routing_key_recebida = method.routing_key
    print(f"[{queue}] routing_key='{routing_key_recebida}' body=\"{body.decode()}\"", flush=True)


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
