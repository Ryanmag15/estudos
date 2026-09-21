"""
FANOUT EXCHANGE
----------------
Uma exchange "fanout" ignora completamente a routing key: toda
mensagem publicada é entregue a TODAS as filas ligadas (bound) a ela.
É um broadcast puro.

Cenário real: evento "novo usuário cadastrado" que precisa disparar
várias ações independentes ao mesmo tempo (email de boas-vindas, SMS,
log de auditoria).
"""

import os
import sys

import pika

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import criar_conexao_rabbitmq

connection = criar_conexao_rabbitmq()
# channel() abre um canal dentro da conexão -- é por ele que passam todos
# os comandos AMQP (declarar exchange/fila, publicar, consumir).
channel = connection.channel()

exchange = 'eventos_fanout'

# exchange_declare() cria a exchange no broker (ou confirma que já existe
# com a mesma config). O producer publica nela, nunca direto numa fila.
#   exchange       -> nome da exchange
#   exchange_type  -> 'fanout' = ignora routing key e entrega a mensagem
#                     para TODAS as filas ligadas (broadcast)
#   durable=True   -> a exchange sobrevive a um restart do broker
channel.exchange_declare(exchange=exchange, exchange_type='fanout', durable=True)

mensagens = [
    "Novo usuário 'maria@example.com' cadastrado",
    "Novo usuário 'joao@example.com' cadastrado",
]

# Publica o mesmo conjunto de mensagens várias vezes, para simular um
# volume maior de tráfego (útil para observar throughput/consumo). Ajuste
# repeticoes para publicar mais ou menos mensagens.
repeticoes = 200000
contador = 0

for rodada in range(1, repeticoes + 1):
    for corpo_base in mensagens:
        contador += 1
        corpo = f"{corpo_base} (msg #{contador})"

        # basic_publish() envia a mensagem para a exchange.
        #   exchange     -> para qual exchange publicar
        #   routing_key  -> a exchange fanout IGNORA esse valor por
        #                   completo; publicamos com string vazia de
        #                   propósito, só para deixar isso explícito
        #   body         -> o conteúdo da mensagem
        #   properties   -> metadados; delivery_mode=Persistent grava a
        #                   mensagem em disco, sobrevivendo a um restart
        #                   do broker (combinado com fila durable)
        channel.basic_publish(
            exchange=exchange,
            routing_key='',
            body=corpo,
            properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
        )

        print(f"[Producer] Publicado (broadcast) body=\"{corpo}\"", flush=True)

connection.close()

print(f"\n{contador} mensagens publicadas para TODAS as filas ligadas.", flush=True)
