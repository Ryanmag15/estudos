"""
HEADERS EXCHANGE
-----------------
Uma exchange "headers" ignora a routing key e roteia com base em
pares chave/valor colocados nos HEADERS da mensagem. O binding define
quais headers ele exige, e um argumento especial "x-match" decide a
regra:
  x-match = all -> a mensagem precisa bater em TODOS os headers do binding
  x-match = any -> a mensagem precisa bater em PELO MENOS UM

Cenário real: roteamento por metadados quando a routing key não é
suficiente -- ex.: processar documentos por formato + prioridade.
"""

import json
import os
import sys

import pika

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import criar_conexao_rabbitmq

connection = criar_conexao_rabbitmq()
channel = connection.channel()

exchange = 'eventos_headers'

# exchange_declare() cria a exchange no broker (ou confirma que já existe
# com a mesma config).
#   exchange_type='headers' -> roteia com base nos HEADERS da mensagem
#                               (não na routing key)
#   durable=True             -> a exchange sobrevive a um restart do
#                               broker
channel.exchange_declare(exchange=exchange, exchange_type='headers', durable=True)

mensagens = [
    {'headers': {'formato': 'pdf', 'prioridade': 'alta'}, 'corpo': 'Relatório financeiro (PDF, alta prioridade)'},
    {'headers': {'formato': 'pdf', 'prioridade': 'baixa'}, 'corpo': 'Manual do usuário (PDF, baixa prioridade)'},
    {'headers': {'formato': 'docx', 'prioridade': 'alta'}, 'corpo': 'Contrato (DOCX, alta prioridade)'},
    {'headers': {'formato': 'docx', 'prioridade': 'baixa'}, 'corpo': 'Rascunho (DOCX, baixa prioridade)'},
]

# Publica o mesmo conjunto de mensagens várias vezes, para simular um
# volume maior de tráfego (útil para observar throughput/consumo). Ajuste
# repeticoes para publicar mais ou menos mensagens.
repeticoes = 20
contador = 0

for rodada in range(1, repeticoes + 1):
    for item in mensagens:
        contador += 1
        corpo = f"{item['corpo']} (msg #{contador})"

        # basic_publish() envia a mensagem para a exchange.
        #   exchange     -> para qual exchange publicar
        #   routing_key  -> a exchange headers ignora esse valor;
        #                   publicamos com string vazia de propósito
        #   body         -> o conteúdo da mensagem
        #   properties   -> aqui é onde a mágica acontece:
        #     headers        -> dict de pares chave/valor que o binding
        #                       vai comparar (é o que decide o roteamento
        #                       nesta exchange, no lugar da routing key)
        #     delivery_mode  -> Persistent grava a mensagem em disco,
        #                       sobrevivendo a um restart do broker
        channel.basic_publish(
            exchange=exchange,
            routing_key='',
            body=corpo,
            properties=pika.BasicProperties(
                headers=item['headers'],
                delivery_mode=pika.DeliveryMode.Persistent,
            ),
        )

        headers_texto = json.dumps(item['headers'])
        print(f"[Producer] Publicado headers={headers_texto} body=\"{corpo}\"", flush=True)

connection.close()

print(f"\n{contador} mensagens publicadas ao todo.", flush=True)
