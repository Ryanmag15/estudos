# Laboratório de estudos RabbitMQ em PHP — Design

Data: 2026-09-14

## Contexto e objetivo

Projeto didático, em `~/estudos/rabbit`, para estudar na prática os quatro
tipos de exchange do RabbitMQ (`direct`, `topic`, `fanout`, `headers`):
como exchanges, filas, bindings e routing keys/headers decidem para onde
uma mensagem vai. Cada tipo de exchange vira um exemplo independente e
executável, com producer(s) e consumer(s) em PHP, para o usuário poder
alterar routing keys/bindings e observar o comportamento na hora.

Não é uma aplicação de produção: prioriza simplicidade e comentários
explicativos sobre abstração, testes automatizados ou tratamento de erro
além do mínimo necessário para o script rodar.

## Stack

- **RabbitMQ**: container Docker, imagem `rabbitmq:3-management` (inclui
  plugin de management, UI em `http://localhost:15672`, login `guest`/`guest`).
- **PHP**: executado localmente pelo usuário (não containerizado). Requer
  PHP >= 8.1 e Composer instalados na máquina.
- **Biblioteca AMQP**: `php-amqplib/php-amqplib` — cliente PHP puro para
  AMQP 0-9-1, não depende de extensão C, é o padrão de fato para RabbitMQ
  em PHP.

## Estrutura de arquivos

```
rabbit/
├── docker-compose.yml
├── composer.json
├── config.php                 # conexão AMQP compartilhada (host/porta/user/senha)
├── README.md                  # conceitos gerais, comparação dos 4 tipos, setup
├── direct/
│   ├── README.md
│   ├── producer.php
│   ├── consumer_info.php
│   ├── consumer_warning.php
│   ├── consumer_error.php
│   └── consumer_critical.php  # bind em "error" E "warning" (múltiplos bindings)
├── topic/
│   ├── README.md
│   ├── producer.php
│   ├── consumer_pedido_asterisco.php   # binding "pedido.*"
│   ├── consumer_aprovado_asterisco.php # binding "*.aprovado"
│   └── consumer_pedido_hash.php        # binding "pedido.#"
├── fanout/
│   ├── README.md
│   ├── producer.php
│   ├── consumer_email.php
│   ├── consumer_sms.php
│   └── consumer_log.php
└── headers/
    ├── README.md
    ├── producer.php
    ├── consumer_match_all.php  # x-match=all
    └── consumer_match_any.php  # x-match=any
```

Princípio central: **cada consumer declara sua própria topologia**
(exchange + queue + binding), de forma idempotente, igual a um consumer
real. Isso significa que qualquer consumer pode ser iniciado antes ou
depois do producer sem erro, e reforça que declarar topologia não é
responsabilidade exclusiva de quem publica.

## Configuração de conexão (`config.php`)

Retorna um array associativo com host/porta/user/senha/vhost, lidos de
variáveis de ambiente (`RABBITMQ_HOST`, `RABBITMQ_PORT`, `RABBITMQ_USER`,
`RABBITMQ_PASS`, `RABBITMQ_VHOST`) com defaults iguais aos do
`docker-compose.yml` (`localhost`, `5672`, `guest`, `guest`, `/`). Cada
producer/consumer faz `require __DIR__ . '/../config.php'` e usa
`PhpAmqpLib\Connection\AMQPStreamConnection`.

## Docker Compose

Um único serviço `rabbitmq`, imagem `rabbitmq:3-management`, portas
`5672:5672` e `15672:15672`. Sem volume nomeado — dados são efêmeros por
padrão (aceitável para um laboratório de estudo; documentado no README).

## Composer

`composer.json` na raiz com dependência única `php-amqplib/php-amqplib`
(versão estável mais recente). Sem autoload customizado — cada script é
standalone e dá `require` direto no `config.php` e no vendor autoload.

## Detalhamento por exchange

### Direct

Cenário real: roteamento de logs por severidade (cada nível de log vai
para um handler diferente — console, email, etc.).

- Exchange `logs_direct` (tipo `direct`, durable).
- Filas: `fila_info`, `fila_warning`, `fila_error` — cada uma com binding
  de mesmo nome da routing key (`info`, `warning`, `error`).
- `consumer_critical.php` demonstra uma quarta fila (`fila_critical`) com
  **dois bindings** (`error` e `warning`), mostrando que uma fila pode
  receber mensagens de múltiplas routing keys.
- `producer.php` publica mensagens com routing keys `info`, `warning`,
  `error` e imprime no console, para cada mensagem, quais filas
  deveriam recebê-la (baseado no match exato routing key == binding key).

### Topic

Cenário real: eventos de e-commerce (pedidos e pagamentos), onde
diferentes serviços assinam padrões de interesse.

- Exchange `eventos_topic` (tipo `topic`, durable).
- `producer.php` publica, em sequência, mensagens com as routing keys:
  `pedido.criado`, `pedido.aprovado`, `pedido.cancelado`,
  `pagamento.aprovado`, `pagamento.recusado`, e uma extra
  `pedido.item.adicionado` (dois níveis) só para evidenciar a diferença
  entre `*` (exatamente um nível) e `#` (zero ou mais níveis).
- Filas e bindings:
  - `fila_pedidos_asterisco` → binding `pedido.*` (pega os `pedido.X` de
    um nível, não pega `pedido.item.adicionado`).
  - `fila_aprovados_asterisco` → binding `*.aprovado` (pega
    `pedido.aprovado` e `pagamento.aprovado`).
  - `fila_pedidos_hash` → binding `pedido.#` (pega todos os `pedido.*`
    E também `pedido.item.adicionado`).
- Cada consumer imprime a routing key recebida para deixar claro o
  padrão de match na prática.

### Fanout

Cenário real: evento "novo usuário cadastrado" replicado para múltiplos
serviços (email de boas-vindas, SMS, log de auditoria) simultaneamente.

- Exchange `eventos_fanout` (tipo `fanout`, durable).
- Filas `fila_email`, `fila_sms`, `fila_log`, todas com binding vazio
  (routing key é ignorada pelo fanout).
- `producer.php` publica uma única mensagem de broadcast; README explica
  que routing key é irrelevante aqui — mesmo se o producer mandar uma,
  as três filas recebem igual.

### Headers

Cenário real: roteamento por metadados quando routing key não é
suficiente (ex.: processar documentos por formato + prioridade).

- Exchange `eventos_headers` (tipo `headers`, durable).
- `fila_match_all` — binding com `x-match=all`, headers
  `{formato: pdf, prioridade: alta}` (mensagem precisa bater nos dois).
- `fila_match_any` — binding com `x-match=any`, mesmos headers
  (mensagem precisa bater em pelo menos um).
- `producer.php` publica mensagens com combinações variadas de headers
  (`formato`/`prioridade`) para evidenciar quais filas recebem cada uma.

## Documentação

- **README.md raiz**: o que é Exchange, Queue, Binding, Routing Key; como
  o RabbitMQ decide o roteamento; tabela comparativa `direct` vs `topic`
  vs `fanout` vs `headers` com casos de uso reais; instruções de setup
  (`docker compose up -d`, `composer install`); como acessar a UI de
  management; como rodar os exemplos (abrir um terminal por consumer,
  depois rodar o producer); troubleshooting (ex.: aguardar RabbitMQ
  subir antes de conectar).
- **README.md por pasta de exchange**: conceito específico daquele tipo,
  cenário real de uso, tabela/diagrama textual "routing key ou headers
  publicados → qual(is) fila(s) deveriam receber".

## Fluxo de execução (fica documentado no README raiz)

1. `docker compose up -d`
2. `composer install`
3. Abrir um terminal por consumer do exemplo escolhido e rodar
   `php <pasta>/consumer_X.php` (ficam ouvindo, saem com Ctrl+C).
4. Em outro terminal, rodar `php <pasta>/producer.php`.
5. Observar nos terminais dos consumers quais mensagens cada fila
   recebeu, e comparar com o que o README daquele exemplo descreve.

## Fora de escopo (YAGNI)

- Sem testes automatizados, CI, autoload PSR-4 ou containerização do PHP.
- Sem persistência de dados do RabbitMQ (volume Docker) — reinícios
  limpam o estado, o que é aceitável para um lab de estudo.
- Sem tratamento de erro além do necessário para os scripts rodarem
  (sem retries, reconexão automática, dead-letter, etc. — fora do escopo
  didático pedido).
