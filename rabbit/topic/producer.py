"""
TOPIC EXCHANGE
---------------
Uma exchange "topic" roteia por PADRÕES na routing key, que deve ter
o formato "palavra.palavra.palavra" (separado por pontos). Bindings
podem usar dois wildcards:
  *  -> substitui exatamente UMA palavra
  #  -> substitui ZERO ou MAIS palavras

Cenário real: eventos de e-commerce (pedidos, pagamentos), onde cada
serviço assina só os padrões que lhe interessam.
"""

import os
import sys

import pika

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import criar_conexao_rabbitmq

connection = criar_conexao_rabbitmq()
channel = connection.channel()

exchange = 'eventos_topic'

# exchange_declare() cria a exchange no broker (ou confirma que já existe
# com a mesma config).
#   exchange_type='topic' -> roteia comparando a routing key com padrões
#                             (binding keys com wildcards * e #) definidos
#                             em cada binding de fila
#   durable=True           -> a exchange sobrevive a um restart do broker
channel.exchange_declare(exchange=exchange, exchange_type='topic', durable=True)

mensagens = [
    {'routing_key': 'pedido.criado', 'corpo': 'Pedido #1001 foi criado'},
    {'routing_key': 'pedido.aprovado', 'corpo': 'Pedido #1001 foi aprovado'},
    {'routing_key': 'pedido.cancelado', 'corpo': 'Pedido #1002 foi cancelado'},
    {'routing_key': 'pagamento.aprovado', 'corpo': 'Pagamento do pedido #1001 foi aprovado'},
    {'routing_key': 'pagamento.recusado', 'corpo': 'Pagamento do pedido #1003 foi recusado'},
    # Routing key com DOIS níveis depois de "pedido" -- serve para mostrar
    # na prática que "pedido.*" NÃO pega isso, mas "pedido.#" pega.
    {'routing_key': 'pedido.item.adicionado', 'corpo': "Item 'Teclado' foi adicionado ao pedido #1001"},
]

# Publica o mesmo conjunto de mensagens várias vezes, para simular um
# volume maior de tráfego (útil para observar throughput/consumo). Ajuste
# repeticoes para publicar mais ou menos mensagens.
repeticoes = 200000
contador = 0

for rodada in range(1, repeticoes + 1):
    for item in mensagens:
        contador += 1
        corpo = f"{item['corpo']} (msg #{contador})"

        # basic_publish() envia a mensagem para a exchange.
        #   exchange     -> para qual exchange publicar
        #   routing_key  -> deve seguir o formato "palavra.palavra..." --
        #                   é contra ela que os bindings com * e # das
        #                   filas vão ser comparados
        #   body         -> o conteúdo da mensagem
        #   properties   -> delivery_mode=Persistent grava a mensagem em
        #                   disco, sobrevivendo a um restart do broker
        channel.basic_publish(
            exchange=exchange,
            routing_key=item['routing_key'],
            body=corpo,
            properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
        )

        print(f"[Producer] Publicado routing_key='{item['routing_key']}' body=\"{corpo}\"", flush=True)

connection.close()

print(f"\n{contador} mensagens publicadas ao todo.", flush=True)
