# Laboratório de estudos: RabbitMQ em PHP

Projeto didático para entender na prática como o RabbitMQ roteia
mensagens através de **exchanges**, **filas** e **bindings**, usando os
quatro tipos de exchange: `direct`, `topic`, `fanout` e `headers`.

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

Requisitos: Docker, PHP >= 8.1, Composer.

```bash
docker compose up -d   # sobe o RabbitMQ (aguarde alguns segundos para ele iniciar)
composer install       # instala a php-amqplib
```

Este `docker-compose.yml` não usa volume nomeado, então os dados (filas,
mensagens) são efêmeros -- um `docker compose down` apaga tudo. Isso é
aceitável (e até prático) para um laboratório de estudo.

UI de management (visualizar exchanges/filas/bindings em tempo real):
http://localhost:15672 (login `guest` / `guest`).

## Como rodar cada exemplo

Para cada pasta (`direct/`, `topic/`, `fanout/`, `headers/`):

1. Abra um terminal para CADA consumer daquele exemplo e rode
   `php <pasta>/consumer_X.php` -- eles ficam ouvindo (Ctrl+C para
   parar).
2. Em outro terminal, rode `php <pasta>/producer.php`.
3. Observe nos terminais dos consumers quais mensagens cada fila
   recebeu, e compare com a tabela do README daquela pasta.

Exemplo (direct):
```bash
# terminal 1
php direct/consumer_info.php
# terminal 2
php direct/consumer_warning.php
# terminal 3
php direct/consumer_error.php
# terminal 4
php direct/consumer_critical.php
# terminal 5 (publica as mensagens)
php direct/producer.php
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
