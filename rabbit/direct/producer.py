"""
DIRECT EXCHANGE
----------------
Uma exchange "direct" roteia a mensagem para a(s) fila(s) cuja binding
key seja EXATAMENTE IGUAL à routing key da mensagem. É o tipo de
roteamento mais simples: um "match" exato, como um switch/case.

Cenário real: log de sistema, onde cada nível de severidade
(info/warning/error) deve ir para um handler diferente.
"""

import os
import sys

import pika

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import criar_conexao_rabbitmq

connection = criar_conexao_rabbitmq()
# channel() abre um "canal" dentro da conexão TCP: é através do canal que
# todos os comandos AMQP (declarar exchange/fila, publicar, consumir) são
# enviados. Uma mesma conexão pode ter vários canais, evitando abrir uma
# conexão TCP nova para cada operação.
channel = connection.channel()

exchange = 'logs_direct'

# exchange_declare() cria a exchange no broker (ou confirma que ela já
# existe com a mesma configuração). Uma exchange é o "roteador": o
# producer NUNCA publica direto numa fila, ele publica numa exchange, que
# decide para quais filas encaminhar a mensagem.
#   exchange       -> nome da exchange
#   exchange_type  -> algoritmo de roteamento: 'direct' | 'fanout' |
#                     'topic' | 'headers' (aqui, 'direct' = match exato
#                     entre routing key da mensagem e binding key da fila)
#   durable=True   -> a exchange é persistida em disco e sobrevive a um
#                     restart do RabbitMQ (se False, ela some ao reiniciar
#                     o broker)
channel.exchange_declare(exchange=exchange, exchange_type='direct', durable=True)

mensagens = [
    {'routing_key': 'info', 'corpo': 'Usuário 42 fez login com sucesso'},
    {'routing_key': 'warning', 'corpo': 'Uso de memória em 82%'},
    {'routing_key': 'error', 'corpo': 'Falha ao conectar no banco de dados'},
    {'routing_key': 'critical', 'corpo': 'Falha crítica: serviço de pagamento indisponível'},
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

        # basic_publish() envia a mensagem para a exchange (nunca para a
        # fila diretamente).
        #   exchange     -> para qual exchange publicar
        #   routing_key  -> "etiqueta" da mensagem; a exchange direct usa
        #                   esse valor para comparar com a binding_key de
        #                   cada fila e decidir o roteamento (match exato)
        #   body         -> o conteúdo da mensagem (bytes ou str)
        #   properties   -> metadados da mensagem. Aqui usamos apenas
        #                   delivery_mode=Persistent, que instrui o
        #                   RabbitMQ a gravar a mensagem em disco (some se
        #                   o broker cair, junto com uma fila não-durable,
        #                   caso não seja persistente)
        channel.basic_publish(
            exchange=exchange,
            routing_key=item['routing_key'],
            body=corpo,
            properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
        )

        print(f"[Producer] Publicado routing_key='{item['routing_key']}' body=\"{corpo}\"", flush=True)

connection.close()

print(f"\n{contador} mensagens publicadas ao todo.", flush=True)
