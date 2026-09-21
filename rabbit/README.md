# Laboratório de estudos: RabbitMQ em Python

Projeto didático para entender na prática como o RabbitMQ roteia
mensagens através de **exchanges**, **filas** e **bindings**, usando os
quatro tipos de exchange: `direct`, `topic`, `fanout` e `headers`.

Os scripts usam [pika](https://pika.readthedocs.io/en/stable/), o cliente
AMQP 0-9-1 oficial para Python.

## Conceitos

- **Exchange**: recebe as mensagens publicadas pelos producers e decide
  para quais filas encaminhá-las. Um producer NUNCA publica direto numa
  fila -- sempre publica numa exchange.
- **Queue (fila)**: onde as mensagens ficam armazenadas até um consumer
  processá-las.
- **Binding**: a "ligação" entre uma exchange e uma fila, que diz à
  exchange "quero receber mensagens que casem com tal critério".
- **Routing key**: um rótulo (string) que o producer anexa à mensagem ao
  publicá-la. É o principal critério de roteamento em exchanges
  `direct` e `topic` (em `fanout` é ignorada; em `headers` também).
- **Como o RabbitMQ decide o roteamento**: a exchange olha o TIPO dela e
  compara a routing key (ou os headers) da mensagem contra os bindings
  registrados; a mensagem é copiada para toda fila cujo binding "casar".
  Se nenhum binding casar, a mensagem é descartada (ou enviada para uma
  exchange alternativa, se configurada -- fora do escopo deste lab).
- **Por que rodar um consumer antes do producer funciona**: cada consumer
  deste lab declara sua própria exchange/fila/binding (de forma
  idempotente) antes de começar a ouvir -- por isso qualquer consumer
  pode ser iniciado antes ou depois do producer, sem erro. O inverso não
  é verdade: se o producer rodar ANTES de qualquer consumer ter criado a
  fila e o binding, a mensagem não encontra fila nenhuma ligada e é
  descartada silenciosamente (sem erro nenhum).

## Tipos de exchange

| Tipo      | Critério de roteamento                          | Cenário real                                  |
|-----------|--------------------------------------------------|------------------------------------------------|
| `direct`  | routing key == binding key (match exato)          | log por severidade (info/warning/error)         |
| `topic`   | routing key casa com padrão (`*` = 1 palavra, `#` = 0+ palavras) | eventos de pedido/pagamento por padrão de interesse |
| `fanout`  | nenhum -- broadcast para todas as filas ligadas    | notificar vários serviços do mesmo evento       |
| `headers` | pares chave/valor nos headers + `x-match` (all/any)| roteamento por metadados (formato, prioridade)  |

Veja o README de cada pasta (`direct/`, `topic/`, `fanout/`,
`headers/`) para o detalhamento e a tabela de roteamento de cada
exemplo.

## Setup

Requisitos: Docker, Python >= 3.8.

```bash
docker compose up -d                    # sobe o RabbitMQ (aguarde alguns segundos para ele iniciar)
python3 -m venv .venv && source .venv/bin/activate  # ambiente virtual (opcional, mas recomendado)
pip install -r requirements.txt         # instala o pika
```

Este `docker-compose.yml` não usa volume nomeado, então os dados (filas,
mensagens) são efêmeros -- um `docker compose down` apaga tudo. Isso é
aceitável (e até prático) para um laboratório de estudo.

UI de management (visualizar exchanges/filas/bindings em tempo real):
http://localhost:15672 (login `guest` / `guest`).

## Como rodar cada exemplo

Para cada pasta (`direct/`, `topic/`, `fanout/`, `headers/`):

1. Abra um terminal para CADA consumer daquele exemplo e rode
   `python3 <pasta>/consumer_X.py` -- eles ficam ouvindo (Ctrl+C para
   parar).
2. Em outro terminal, rode `python3 <pasta>/producer.py`.
3. Observe nos terminais dos consumers quais mensagens cada fila
   recebeu, e compare com a tabela do README daquela pasta.

Exemplo (direct):
```bash
# terminal 1
python3 direct/consumer_info.py
# terminal 2
python3 direct/consumer_warning.py
# terminal 3
python3 direct/consumer_error.py
# terminal 4
python3 direct/consumer_critical.py
# terminal 5 (publica as mensagens)
python3 direct/producer.py
```

## Experimente

Este é um laboratório -- altere routing keys, bindings ou headers nos
scripts e rode de novo para ver o comportamento mudar. Por exemplo, no
`topic/`, tente adicionar um binding `pagamento.#` num novo consumer e
veja quais mensagens ele passa a receber.

## Troubleshooting

- **Connection refused**: o RabbitMQ ainda não terminou de subir --
  aguarde alguns segundos após `docker compose up -d` e tente de novo.
- **Fila não recebe nada**: confira se o binding do consumer bate com a
  routing key (ou headers) publicada pelo producer -- releia a tabela do
  README daquele exemplo.
- **Rodei o producer primeiro e "não aconteceu nada"**: sem nenhum
  consumer ter rodado ainda, não existe fila nem binding -- a mensagem é
  publicada, não casa com binding nenhum, e é descartada. Rode pelo
  menos um consumer do exemplo primeiro, depois o producer.
