# Laboratório RabbitMQ em PHP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a runnable, well-documented PHP + Docker lab that demonstrates how RabbitMQ's four exchange types (`direct`, `topic`, `fanout`, `headers`) route messages to queues.

**Architecture:** One RabbitMQ broker in Docker (`rabbitmq:3-management`). PHP scripts run locally via Composer + `php-amqplib`. A single shared `config.php` builds the AMQP connection; every other file is a standalone producer or consumer for one exchange type, grouped by folder. Each consumer declares its own exchange/queue/binding (idempotent), so it can be started independently of the producer.

**Tech Stack:** PHP >= 8.1, Composer, `php-amqplib/php-amqplib` ^3.0, Docker Compose, RabbitMQ 3 (management image).

**Spec:** `docs/superpowers/specs/2026-09-14-rabbitmq-php-lab-design.md`

## Global Constraints

- No automated test framework — this project's spec explicitly puts automated tests out of scope. Verification is a manual/integration smoke run against the real broker (see each task's test step).
- No autoload/PSR-4, no PHP containerization, no persistent Docker volume, no reconnect/retry/dead-letter logic — all explicitly out of scope per the spec's "Fora de escopo" section.
- Connection defaults: host `localhost`, port `5672`, user `guest`, pass `guest`, vhost `/` — must match `docker-compose.yml` exactly.
- Every producer/consumer requires `__DIR__ . '/../config.php'` and calls `criarConexaoRabbitMQ()` — no duplicated connection logic.
- Consumers auto-ack (`$noAck = true`) and loop forever (`while ($channel->is_consuming()) { $channel->wait(); }`) — stopped with Ctrl+C in real use.
- All durable exchanges/queues declared with `durable = true`, `auto_delete = false`.

---

## Task 1: Infraestrutura base (Docker Compose, Composer, config.php)

**Files:**
- Create: `docker-compose.yml`
- Create: `composer.json`
- Create: `config.php`
- Create: `.gitignore`

**Interfaces:**
- Produces: `criarConexaoRabbitMQ(): PhpAmqpLib\Connection\AMQPStreamConnection` in `config.php` — every later task's producer/consumer calls this after `require __DIR__ . '/../config.php'`.

- [ ] **Step 1: Write `docker-compose.yml`**

```yaml
services:
  rabbitmq:
    image: rabbitmq:3-management
    container_name: rabbitmq-estudos
    ports:
      - "5672:5672"   # porta AMQP (usada pelos scripts PHP)
      - "15672:15672" # UI de management (http://localhost:15672, guest/guest)
```

- [ ] **Step 2: Write `composer.json`**

```json
{
    "name": "estudos/rabbitmq-php-lab",
    "description": "Laboratório de estudos dos tipos de exchange do RabbitMQ em PHP",
    "type": "project",
    "require": {
        "php": ">=8.1",
        "php-amqplib/php-amqplib": "^3.0"
    }
}
```

- [ ] **Step 3: Write `.gitignore`**

```
/vendor/
composer.lock
```

- [ ] **Step 4: Write `config.php`**

```php
<?php

/**
 * Configuração de conexão com o RabbitMQ.
 *
 * Os valores podem ser sobrescritos por variáveis de ambiente
 * (RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USER, RABBITMQ_PASS,
 * RABBITMQ_VHOST), mas os defaults já batem com o docker-compose.yml
 * deste projeto, então "docker compose up -d" + rodar os scripts
 * já funciona sem configurar nada.
 */

require_once __DIR__ . '/vendor/autoload.php';

use PhpAmqpLib\Connection\AMQPStreamConnection;

function criarConexaoRabbitMQ(): AMQPStreamConnection
{
    $host = getenv('RABBITMQ_HOST') ?: 'localhost';
    $port = (int) (getenv('RABBITMQ_PORT') ?: 5672);
    $user = getenv('RABBITMQ_USER') ?: 'guest';
    $pass = getenv('RABBITMQ_PASS') ?: 'guest';
    $vhost = getenv('RABBITMQ_VHOST') ?: '/';

    return new AMQPStreamConnection($host, $port, $user, $pass, $vhost);
}
```

- [ ] **Step 5: Subir o RabbitMQ e instalar dependências**

Run:
```bash
docker compose up -d
composer install
```
Expected: `docker compose up -d` reports the `rabbitmq` container started; `composer install` creates `vendor/` with no errors.

- [ ] **Step 6: Testar a conexão (RabbitMQ leva alguns segundos para aceitar conexões)**

Run:
```bash
for i in $(seq 1 15); do
  php -r "require 'config.php'; try { \$c = criarConexaoRabbitMQ(); echo 'OK'.PHP_EOL; \$c->close(); } catch (\Throwable \$e) { exit(1); }" && break
  sleep 2
done
```
Expected: eventually prints `OK` (retries while the broker finishes starting up).

- [ ] **Step 7: Commit**

```bash
git add docker-compose.yml composer.json composer.lock config.php .gitignore
git commit -m "chore: add RabbitMQ docker-compose, composer setup and shared connection config"
```

---

## Task 2: Exemplo Direct Exchange

**Files:**
- Create: `direct/producer.php`
- Create: `direct/consumer_info.php`
- Create: `direct/consumer_warning.php`
- Create: `direct/consumer_error.php`
- Create: `direct/consumer_critical.php`
- Create: `direct/README.md`

**Interfaces:**
- Consumes: `criarConexaoRabbitMQ()` from `config.php` (Task 1).

- [ ] **Step 1: Write `direct/producer.php`**

```php
<?php

/**
 * DIRECT EXCHANGE
 * ----------------
 * Uma exchange "direct" roteia a mensagem para a(s) fila(s) cuja binding
 * key seja EXATAMENTE IGUAL à routing key da mensagem. É o tipo de
 * roteamento mais simples: um "match" exato, como um switch/case.
 *
 * Cenário real: log de sistema, onde cada nível de severidade
 * (info/warning/error) deve ir para um handler diferente.
 */

require __DIR__ . '/../config.php';

use PhpAmqpLib\Message\AMQPMessage;

$connection = criarConexaoRabbitMQ();
$channel = $connection->channel();

$exchange = 'logs_direct';
$channel->exchange_declare($exchange, 'direct', false, true, false);

$mensagens = [
    ['routing_key' => 'info',    'corpo' => 'Usuário 42 fez login com sucesso'],
    ['routing_key' => 'warning', 'corpo' => 'Uso de memória em 82%'],
    ['routing_key' => 'error',   'corpo' => 'Falha ao conectar no banco de dados'],
];

foreach ($mensagens as $item) {
    $msg = new AMQPMessage($item['corpo'], [
        'delivery_mode' => AMQPMessage::DELIVERY_MODE_PERSISTENT,
    ]);

    $channel->basic_publish($msg, $exchange, $item['routing_key']);

    echo "[Producer] Publicado routing_key='{$item['routing_key']}' body=\"{$item['corpo']}\"\n";
    echo "  -> Deve ir para a(s) fila(s) com binding key == '{$item['routing_key']}'\n";
}

$channel->close();
$connection->close();

echo "\nTodas as mensagens foram publicadas.\n";
```

- [ ] **Step 2: Write `direct/consumer_info.php`**

```php
<?php

require __DIR__ . '/../config.php';

$connection = criarConexaoRabbitMQ();
$channel = $connection->channel();

$exchange = 'logs_direct';
$queue = 'fila_info';
$routingKey = 'info';

// Cada consumer declara sua própria topologia (idempotente): pode ser
// iniciado antes ou depois do producer sem dar erro.
$channel->exchange_declare($exchange, 'direct', false, true, false);
$channel->queue_declare($queue, false, true, false, false);
$channel->queue_bind($queue, $exchange, $routingKey);

echo "[{$queue}] Aguardando mensagens com routing_key='{$routingKey}'. CTRL+C para sair.\n";
flush();

$channel->basic_consume($queue, '', false, true, false, false, function ($msg) use ($queue) {
    $routingKeyRecebida = $msg->delivery_info['routing_key'];
    echo "[{$queue}] routing_key='{$routingKeyRecebida}' body=\"{$msg->getBody()}\"\n";
    flush();
});

while ($channel->is_consuming()) {
    $channel->wait();
}

$channel->close();
$connection->close();
```

- [ ] **Step 3: Write `direct/consumer_warning.php`**

Same as `consumer_info.php` but with `$queue = 'fila_warning'` and `$routingKey = 'warning'`.

```php
<?php

require __DIR__ . '/../config.php';

$connection = criarConexaoRabbitMQ();
$channel = $connection->channel();

$exchange = 'logs_direct';
$queue = 'fila_warning';
$routingKey = 'warning';

$channel->exchange_declare($exchange, 'direct', false, true, false);
$channel->queue_declare($queue, false, true, false, false);
$channel->queue_bind($queue, $exchange, $routingKey);

echo "[{$queue}] Aguardando mensagens com routing_key='{$routingKey}'. CTRL+C para sair.\n";
flush();

$channel->basic_consume($queue, '', false, true, false, false, function ($msg) use ($queue) {
    $routingKeyRecebida = $msg->delivery_info['routing_key'];
    echo "[{$queue}] routing_key='{$routingKeyRecebida}' body=\"{$msg->getBody()}\"\n";
    flush();
});

while ($channel->is_consuming()) {
    $channel->wait();
}

$channel->close();
$connection->close();
```

- [ ] **Step 4: Write `direct/consumer_error.php`**

Same pattern with `$queue = 'fila_error'` and `$routingKey = 'error'`.

```php
<?php

require __DIR__ . '/../config.php';

$connection = criarConexaoRabbitMQ();
$channel = $connection->channel();

$exchange = 'logs_direct';
$queue = 'fila_error';
$routingKey = 'error';

$channel->exchange_declare($exchange, 'direct', false, true, false);
$channel->queue_declare($queue, false, true, false, false);
$channel->queue_bind($queue, $exchange, $routingKey);

echo "[{$queue}] Aguardando mensagens com routing_key='{$routingKey}'. CTRL+C para sair.\n";
flush();

$channel->basic_consume($queue, '', false, true, false, false, function ($msg) use ($queue) {
    $routingKeyRecebida = $msg->delivery_info['routing_key'];
    echo "[{$queue}] routing_key='{$routingKeyRecebida}' body=\"{$msg->getBody()}\"\n";
    flush();
});

while ($channel->is_consuming()) {
    $channel->wait();
}

$channel->close();
$connection->close();
```

- [ ] **Step 5: Write `direct/consumer_critical.php` (fila com DOIS bindings)**

```php
<?php

/**
 * Demonstra que uma fila pode ter MÚLTIPLOS bindings: esta fila recebe
 * tanto mensagens 'error' quanto 'warning', porque foi feito um
 * queue_bind() para cada routing key.
 */

require __DIR__ . '/../config.php';

$connection = criarConexaoRabbitMQ();
$channel = $connection->channel();

$exchange = 'logs_direct';
$queue = 'fila_critical';

$channel->exchange_declare($exchange, 'direct', false, true, false);
$channel->queue_declare($queue, false, true, false, false);
$channel->queue_bind($queue, $exchange, 'error');
$channel->queue_bind($queue, $exchange, 'warning');

echo "[{$queue}] Aguardando mensagens com routing_key='error' OU 'warning'. CTRL+C para sair.\n";
flush();

$channel->basic_consume($queue, '', false, true, false, false, function ($msg) use ($queue) {
    $routingKeyRecebida = $msg->delivery_info['routing_key'];
    echo "[{$queue}] routing_key='{$routingKeyRecebida}' body=\"{$msg->getBody()}\"\n";
    flush();
});

while ($channel->is_consuming()) {
    $channel->wait();
}

$channel->close();
$connection->close();
```

- [ ] **Step 6: Write `direct/README.md`**

```markdown
# Direct Exchange

Uma exchange `direct` roteia a mensagem para a(s) fila(s) cuja **binding
key** seja **exatamente igual** à **routing key** da mensagem publicada.
É um match exato — sem padrões, sem wildcards.

## Cenário real

Sistema de log: cada nível de severidade (`info`, `warning`, `error) deve
ir para um handler diferente (console, alerta, etc.).

## Topologia deste exemplo

- Exchange: `logs_direct` (tipo `direct`)
- `fila_info`     <- binding `info`
- `fila_warning`  <- binding `warning`
- `fila_error`    <- binding `error`
- `fila_critical` <- bindings `error` E `warning` (uma fila pode ter mais de um binding)

## O que cada mensagem publicada deveria acionar

| routing_key da mensagem | filas que recebem              |
|--------------------------|--------------------------------|
| `info`                    | `fila_info`                    |
| `warning`                 | `fila_warning`, `fila_critical`|
| `error`                   | `fila_error`, `fila_critical`  |

## Como rodar

Em 4 terminais separados, deixe os consumers ouvindo:
```bash
php direct/consumer_info.php
php direct/consumer_warning.php
php direct/consumer_error.php
php direct/consumer_critical.php
```

Em um 5º terminal, publique as mensagens:
```bash
php direct/producer.php
```

Observe: `fila_info` recebe só a mensagem de info; `fila_critical` recebe
tanto a de warning quanto a de error.
```

- [ ] **Step 7: Testar o exemplo (consumers em background + producer)**

Run:
```bash
timeout 8 php direct/consumer_info.php     > /tmp/direct_info.log     2>&1 &
timeout 8 php direct/consumer_warning.php  > /tmp/direct_warning.log  2>&1 &
timeout 8 php direct/consumer_error.php    > /tmp/direct_error.log    2>&1 &
timeout 8 php direct/consumer_critical.php > /tmp/direct_critical.log 2>&1 &
sleep 2
php direct/producer.php
sleep 2
grep -q "login com sucesso" /tmp/direct_info.log && echo "PASS: fila_info recebeu info"
grep -q "memória em 82%" /tmp/direct_warning.log && echo "PASS: fila_warning recebeu warning"
grep -q "Falha ao conectar" /tmp/direct_error.log && echo "PASS: fila_error recebeu error"
grep -q "memória em 82%" /tmp/direct_critical.log && grep -q "Falha ao conectar" /tmp/direct_critical.log && echo "PASS: fila_critical recebeu warning E error"
wait
```
Expected: all four `PASS:` lines are printed.

- [ ] **Step 8: Commit**

```bash
git add direct/
git commit -m "feat: add direct exchange example (log routing by severity)"
```

---

## Task 3: Exemplo Topic Exchange

**Files:**
- Create: `topic/producer.php`
- Create: `topic/consumer_pedido_asterisco.php`
- Create: `topic/consumer_aprovado_asterisco.php`
- Create: `topic/consumer_pedido_hash.php`
- Create: `topic/README.md`

**Interfaces:**
- Consumes: `criarConexaoRabbitMQ()` from `config.php` (Task 1).

- [ ] **Step 1: Write `topic/producer.php`**

```php
<?php

/**
 * TOPIC EXCHANGE
 * ---------------
 * Uma exchange "topic" roteia por PADRÕES na routing key, que deve ter
 * o formato "palavra.palavra.palavra" (separado por pontos). Bindings
 * podem usar dois wildcards:
 *   *  -> substitui exatamente UMA palavra
 *   #  -> substitui ZERO ou MAIS palavras
 *
 * Cenário real: eventos de e-commerce (pedidos, pagamentos), onde cada
 * serviço assina só os padrões que lhe interessam.
 */

require __DIR__ . '/../config.php';

use PhpAmqpLib\Message\AMQPMessage;

$connection = criarConexaoRabbitMQ();
$channel = $connection->channel();

$exchange = 'eventos_topic';
$channel->exchange_declare($exchange, 'topic', false, true, false);

$mensagens = [
    ['routing_key' => 'pedido.criado',           'corpo' => "Pedido #1001 foi criado"],
    ['routing_key' => 'pedido.aprovado',         'corpo' => "Pedido #1001 foi aprovado"],
    ['routing_key' => 'pedido.cancelado',        'corpo' => "Pedido #1002 foi cancelado"],
    ['routing_key' => 'pagamento.aprovado',      'corpo' => "Pagamento do pedido #1001 foi aprovado"],
    ['routing_key' => 'pagamento.recusado',      'corpo' => "Pagamento do pedido #1003 foi recusado"],
    // Routing key com DOIS níveis depois de "pedido" -- serve para mostrar
    // na prática que "pedido.*" NÃO pega isso, mas "pedido.#" pega.
    ['routing_key' => 'pedido.item.adicionado',  'corpo' => "Item 'Teclado' foi adicionado ao pedido #1001"],
];

foreach ($mensagens as $item) {
    $msg = new AMQPMessage($item['corpo'], [
        'delivery_mode' => AMQPMessage::DELIVERY_MODE_PERSISTENT,
    ]);

    $channel->basic_publish($msg, $exchange, $item['routing_key']);

    echo "[Producer] Publicado routing_key='{$item['routing_key']}' body=\"{$item['corpo']}\"\n";
}

$channel->close();
$connection->close();

echo "\nTodas as mensagens foram publicadas.\n";
```

- [ ] **Step 2: Write `topic/consumer_pedido_asterisco.php` (binding `pedido.*`)**

```php
<?php

/**
 * Binding "pedido.*" -- o "*" substitui EXATAMENTE uma palavra.
 * Pega: pedido.criado, pedido.aprovado, pedido.cancelado
 * NÃO pega: pedido.item.adicionado (tem duas palavras depois de "pedido")
 */

require __DIR__ . '/../config.php';

$connection = criarConexaoRabbitMQ();
$channel = $connection->channel();

$exchange = 'eventos_topic';
$queue = 'fila_pedidos_asterisco';
$bindingKey = 'pedido.*';

$channel->exchange_declare($exchange, 'topic', false, true, false);
$channel->queue_declare($queue, false, true, false, false);
$channel->queue_bind($queue, $exchange, $bindingKey);

echo "[{$queue}] Aguardando mensagens que casem com '{$bindingKey}'. CTRL+C para sair.\n";
flush();

$channel->basic_consume($queue, '', false, true, false, false, function ($msg) use ($queue) {
    $routingKeyRecebida = $msg->delivery_info['routing_key'];
    echo "[{$queue}] routing_key='{$routingKeyRecebida}' body=\"{$msg->getBody()}\"\n";
    flush();
});

while ($channel->is_consuming()) {
    $channel->wait();
}

$channel->close();
$connection->close();
```

- [ ] **Step 3: Write `topic/consumer_aprovado_asterisco.php` (binding `*.aprovado`)**

```php
<?php

/**
 * Binding "*.aprovado" -- pega qualquer coisa de UMA palavra seguida de
 * ".aprovado". Pega: pedido.aprovado, pagamento.aprovado.
 */

require __DIR__ . '/../config.php';

$connection = criarConexaoRabbitMQ();
$channel = $connection->channel();

$exchange = 'eventos_topic';
$queue = 'fila_aprovados_asterisco';
$bindingKey = '*.aprovado';

$channel->exchange_declare($exchange, 'topic', false, true, false);
$channel->queue_declare($queue, false, true, false, false);
$channel->queue_bind($queue, $exchange, $bindingKey);

echo "[{$queue}] Aguardando mensagens que casem com '{$bindingKey}'. CTRL+C para sair.\n";
flush();

$channel->basic_consume($queue, '', false, true, false, false, function ($msg) use ($queue) {
    $routingKeyRecebida = $msg->delivery_info['routing_key'];
    echo "[{$queue}] routing_key='{$routingKeyRecebida}' body=\"{$msg->getBody()}\"\n";
    flush();
});

while ($channel->is_consuming()) {
    $channel->wait();
}

$channel->close();
$connection->close();
```

- [ ] **Step 4: Write `topic/consumer_pedido_hash.php` (binding `pedido.#`)**

```php
<?php

/**
 * Binding "pedido.#" -- o "#" substitui ZERO ou MAIS palavras.
 * Pega TODAS as mensagens que começam com "pedido.", não importa quantos
 * níveis vêm depois: pedido.criado, pedido.aprovado, pedido.cancelado
 * E TAMBÉM pedido.item.adicionado (2 níveis).
 */

require __DIR__ . '/../config.php';

$connection = criarConexaoRabbitMQ();
$channel = $connection->channel();

$exchange = 'eventos_topic';
$queue = 'fila_pedidos_hash';
$bindingKey = 'pedido.#';

$channel->exchange_declare($exchange, 'topic', false, true, false);
$channel->queue_declare($queue, false, true, false, false);
$channel->queue_bind($queue, $exchange, $bindingKey);

echo "[{$queue}] Aguardando mensagens que casem com '{$bindingKey}'. CTRL+C para sair.\n";
flush();

$channel->basic_consume($queue, '', false, true, false, false, function ($msg) use ($queue) {
    $routingKeyRecebida = $msg->delivery_info['routing_key'];
    echo "[{$queue}] routing_key='{$routingKeyRecebida}' body=\"{$msg->getBody()}\"\n";
    flush();
});

while ($channel->is_consuming()) {
    $channel->wait();
}

$channel->close();
$connection->close();
```

- [ ] **Step 5: Write `topic/README.md`**

```markdown
# Topic Exchange

Uma exchange `topic` roteia por **padrões** aplicados sobre a routing key,
que deve seguir o formato `palavra.palavra.palavra` (separada por
pontos). Dois wildcards são permitidos no binding:

- `*` substitui **exatamente uma** palavra
- `#` substitui **zero ou mais** palavras

## Cenário real

Eventos de e-commerce (pedidos, pagamentos) publicados por um serviço
central, onde cada outro serviço assina só os padrões que lhe interessam
(ex.: o serviço de auditoria assina tudo com `#`, o de notificação só
`*.aprovado`).

## Topologia deste exemplo

- Exchange: `eventos_topic` (tipo `topic`)
- `fila_pedidos_asterisco`   <- binding `pedido.*`
- `fila_aprovados_asterisco` <- binding `*.aprovado`
- `fila_pedidos_hash`        <- binding `pedido.#`

## Mensagens publicadas e para onde vão

| routing_key                | `pedido.*` | `*.aprovado` | `pedido.#` |
|-----------------------------|:----------:|:------------:|:----------:|
| `pedido.criado`             | ✅         |              | ✅         |
| `pedido.aprovado`           | ✅         | ✅           | ✅         |
| `pedido.cancelado`          | ✅         |              | ✅         |
| `pagamento.aprovado`        |            | ✅           |            |
| `pagamento.recusado`        |            |              |            |
| `pedido.item.adicionado`    |            |              | ✅         |

Repare em `pedido.item.adicionado`: só a fila com `#` recebe, porque `*`
substitui exatamente uma palavra e aqui há duas depois de `pedido`.

## Como rodar

Em 3 terminais separados:
```bash
php topic/consumer_pedido_asterisco.php
php topic/consumer_aprovado_asterisco.php
php topic/consumer_pedido_hash.php
```

Em outro terminal:
```bash
php topic/producer.php
```
```

- [ ] **Step 6: Testar o exemplo**

Run:
```bash
timeout 8 php topic/consumer_pedido_asterisco.php   > /tmp/topic_asterisco.log 2>&1 &
timeout 8 php topic/consumer_aprovado_asterisco.php > /tmp/topic_aprovado.log  2>&1 &
timeout 8 php topic/consumer_pedido_hash.php        > /tmp/topic_hash.log      2>&1 &
sleep 2
php topic/producer.php
sleep 2
grep -q "Pedido #1001 foi criado" /tmp/topic_asterisco.log && \
  grep -q "Pedido #1001 foi aprovado" /tmp/topic_asterisco.log && \
  grep -q "Pedido #1002 foi cancelado" /tmp/topic_asterisco.log && \
  ! grep -q "Teclado" /tmp/topic_asterisco.log && echo "PASS: pedido.* pegou os 3 de 1 nível e ignorou o de 2 níveis"

grep -q "Pedido #1001 foi aprovado" /tmp/topic_aprovado.log && \
  grep -q "Pagamento do pedido #1001 foi aprovado" /tmp/topic_aprovado.log && \
  ! grep -q "recusado" /tmp/topic_aprovado.log && echo "PASS: *.aprovado pegou só os aprovados"

grep -q "Teclado" /tmp/topic_hash.log && \
  grep -q "Pedido #1001 foi criado" /tmp/topic_hash.log && echo "PASS: pedido.# pegou tudo, incluindo o de 2 níveis"
wait
```
Expected: all three `PASS:` lines are printed.

- [ ] **Step 7: Commit**

```bash
git add topic/
git commit -m "feat: add topic exchange example (order/payment events with wildcard bindings)"
```

---

## Task 4: Exemplo Fanout Exchange

**Files:**
- Create: `fanout/producer.php`
- Create: `fanout/consumer_email.php`
- Create: `fanout/consumer_sms.php`
- Create: `fanout/consumer_log.php`
- Create: `fanout/README.md`

**Interfaces:**
- Consumes: `criarConexaoRabbitMQ()` from `config.php` (Task 1).

- [ ] **Step 1: Write `fanout/producer.php`**

```php
<?php

/**
 * FANOUT EXCHANGE
 * ----------------
 * Uma exchange "fanout" ignora completamente a routing key: toda
 * mensagem publicada é entregue a TODAS as filas ligadas (bound) a ela.
 * É um broadcast puro.
 *
 * Cenário real: evento "novo usuário cadastrado" que precisa disparar
 * várias ações independentes ao mesmo tempo (email de boas-vindas, SMS,
 * log de auditoria).
 */

require __DIR__ . '/../config.php';

use PhpAmqpLib\Message\AMQPMessage;

$connection = criarConexaoRabbitMQ();
$channel = $connection->channel();

$exchange = 'eventos_fanout';
$channel->exchange_declare($exchange, 'fanout', false, true, false);

$mensagens = [
    "Novo usuário 'maria@example.com' cadastrado",
    "Novo usuário 'joao@example.com' cadastrado",
];

foreach ($mensagens as $corpo) {
    $msg = new AMQPMessage($corpo, [
        'delivery_mode' => AMQPMessage::DELIVERY_MODE_PERSISTENT,
    ]);

    // A routing key é irrelevante para fanout -- publicamos com string
    // vazia de propósito, para deixar isso explícito.
    $channel->basic_publish($msg, $exchange, '');

    echo "[Producer] Publicado (broadcast) body=\"{$corpo}\"\n";
}

$channel->close();
$connection->close();

echo "\nTodas as mensagens foram publicadas para TODAS as filas ligadas.\n";
```

- [ ] **Step 2: Write `fanout/consumer_email.php`**

```php
<?php

require __DIR__ . '/../config.php';

$connection = criarConexaoRabbitMQ();
$channel = $connection->channel();

$exchange = 'eventos_fanout';
$queue = 'fila_email';

$channel->exchange_declare($exchange, 'fanout', false, true, false);
$channel->queue_declare($queue, false, true, false, false);
// Fanout ignora routing key -- o bind não recebe (nem precisa de) uma.
$channel->queue_bind($queue, $exchange);

echo "[{$queue}] Aguardando qualquer mensagem publicada na exchange fanout. CTRL+C para sair.\n";
flush();

$channel->basic_consume($queue, '', false, true, false, false, function ($msg) use ($queue) {
    echo "[{$queue}] body=\"{$msg->getBody()}\"\n";
    flush();
});

while ($channel->is_consuming()) {
    $channel->wait();
}

$channel->close();
$connection->close();
```

- [ ] **Step 3: Write `fanout/consumer_sms.php`**

Same pattern with `$queue = 'fila_sms'`.

```php
<?php

require __DIR__ . '/../config.php';

$connection = criarConexaoRabbitMQ();
$channel = $connection->channel();

$exchange = 'eventos_fanout';
$queue = 'fila_sms';

$channel->exchange_declare($exchange, 'fanout', false, true, false);
$channel->queue_declare($queue, false, true, false, false);
$channel->queue_bind($queue, $exchange);

echo "[{$queue}] Aguardando qualquer mensagem publicada na exchange fanout. CTRL+C para sair.\n";
flush();

$channel->basic_consume($queue, '', false, true, false, false, function ($msg) use ($queue) {
    echo "[{$queue}] body=\"{$msg->getBody()}\"\n";
    flush();
});

while ($channel->is_consuming()) {
    $channel->wait();
}

$channel->close();
$connection->close();
```

- [ ] **Step 4: Write `fanout/consumer_log.php`**

Same pattern with `$queue = 'fila_log'`.

```php
<?php

require __DIR__ . '/../config.php';

$connection = criarConexaoRabbitMQ();
$channel = $connection->channel();

$exchange = 'eventos_fanout';
$queue = 'fila_log';

$channel->exchange_declare($exchange, 'fanout', false, true, false);
$channel->queue_declare($queue, false, true, false, false);
$channel->queue_bind($queue, $exchange);

echo "[{$queue}] Aguardando qualquer mensagem publicada na exchange fanout. CTRL+C para sair.\n";
flush();

$channel->basic_consume($queue, '', false, true, false, false, function ($msg) use ($queue) {
    echo "[{$queue}] body=\"{$msg->getBody()}\"\n";
    flush();
});

while ($channel->is_consuming()) {
    $channel->wait();
}

$channel->close();
$connection->close();
```

- [ ] **Step 5: Write `fanout/README.md`**

```markdown
# Fanout Exchange

Uma exchange `fanout` **ignora a routing key**: toda mensagem publicada é
entregue a **todas** as filas ligadas (bound) a ela. É um broadcast puro
-- não há filtro nenhum.

## Cenário real

Evento "novo usuário cadastrado" que precisa disparar várias ações
independentes ao mesmo tempo: enviar email de boas-vindas, enviar SMS,
gravar log de auditoria.

## Topologia deste exemplo

- Exchange: `eventos_fanout` (tipo `fanout`)
- `fila_email`, `fila_sms`, `fila_log` -- todas ligadas sem routing key.

## O que acontece

Cada mensagem publicada chega às 3 filas ao mesmo tempo, mesmo que o
producer não informe (ou informe) uma routing key -- ela é ignorada.

## Como rodar

Em 3 terminais separados:
```bash
php fanout/consumer_email.php
php fanout/consumer_sms.php
php fanout/consumer_log.php
```

Em outro terminal:
```bash
php fanout/producer.php
```

Observe: as 2 mensagens publicadas aparecem nos 3 terminais dos
consumers.
```

- [ ] **Step 6: Testar o exemplo**

Run:
```bash
timeout 8 php fanout/consumer_email.php > /tmp/fanout_email.log 2>&1 &
timeout 8 php fanout/consumer_sms.php   > /tmp/fanout_sms.log   2>&1 &
timeout 8 php fanout/consumer_log.php   > /tmp/fanout_log.log   2>&1 &
sleep 2
php fanout/producer.php
sleep 2
for f in /tmp/fanout_email.log /tmp/fanout_sms.log /tmp/fanout_log.log; do
  grep -q "maria@example.com" "$f" && grep -q "joao@example.com" "$f" && echo "PASS: $f recebeu as 2 mensagens"
done
wait
```
Expected: three `PASS:` lines, one per log file.

- [ ] **Step 7: Commit**

```bash
git add fanout/
git commit -m "feat: add fanout exchange example (broadcast new-user event)"
```

---

## Task 5: Exemplo Headers Exchange

**Files:**
- Create: `headers/producer.php`
- Create: `headers/consumer_match_all.php`
- Create: `headers/consumer_match_any.php`
- Create: `headers/README.md`

**Interfaces:**
- Consumes: `criarConexaoRabbitMQ()` from `config.php` (Task 1).

- [ ] **Step 1: Write `headers/producer.php`**

```php
<?php

/**
 * HEADERS EXCHANGE
 * -----------------
 * Uma exchange "headers" ignora a routing key e roteia com base em
 * pares chave/valor colocados nos HEADERS da mensagem. O binding define
 * quais headers ele exige, e um argumento especial "x-match" decide a
 * regra:
 *   x-match = all -> a mensagem precisa bater em TODOS os headers do binding
 *   x-match = any -> a mensagem precisa bater em PELO MENOS UM
 *
 * Cenário real: roteamento por metadados quando a routing key não é
 * suficiente -- ex.: processar documentos por formato + prioridade.
 */

require __DIR__ . '/../config.php';

use PhpAmqpLib\Message\AMQPMessage;
use PhpAmqpLib\Wire\AMQPTable;

$connection = criarConexaoRabbitMQ();
$channel = $connection->channel();

$exchange = 'eventos_headers';
$channel->exchange_declare($exchange, 'headers', false, true, false);

$mensagens = [
    ['headers' => ['formato' => 'pdf',  'prioridade' => 'alta'],  'corpo' => "Relatório financeiro (PDF, alta prioridade)"],
    ['headers' => ['formato' => 'pdf',  'prioridade' => 'baixa'], 'corpo' => "Manual do usuário (PDF, baixa prioridade)"],
    ['headers' => ['formato' => 'docx', 'prioridade' => 'alta'],  'corpo' => "Contrato (DOCX, alta prioridade)"],
    ['headers' => ['formato' => 'docx', 'prioridade' => 'baixa'], 'corpo' => "Rascunho (DOCX, baixa prioridade)"],
];

foreach ($mensagens as $item) {
    $msg = new AMQPMessage($item['corpo'], [
        'application_headers' => new AMQPTable($item['headers']),
    ]);

    // Headers exchange ignora routing key -- publicamos com string vazia.
    $channel->basic_publish($msg, $exchange, '');

    $headersTexto = json_encode($item['headers']);
    echo "[Producer] Publicado headers={$headersTexto} body=\"{$item['corpo']}\"\n";
}

$channel->close();
$connection->close();

echo "\nTodas as mensagens foram publicadas.\n";
```

- [ ] **Step 2: Write `headers/consumer_match_all.php` (`x-match=all`)**

```php
<?php

/**
 * x-match=all -- a mensagem só é roteada para esta fila se ela tiver
 * TODOS os headers exigidos com os mesmos valores: formato=pdf E
 * prioridade=alta.
 */

require __DIR__ . '/../config.php';

use PhpAmqpLib\Wire\AMQPTable;

$connection = criarConexaoRabbitMQ();
$channel = $connection->channel();

$exchange = 'eventos_headers';
$queue = 'fila_match_all';

$channel->exchange_declare($exchange, 'headers', false, true, false);
$channel->queue_declare($queue, false, true, false, false);

$bindingArgs = new AMQPTable([
    'x-match' => 'all',
    'formato' => 'pdf',
    'prioridade' => 'alta',
]);
$channel->queue_bind($queue, $exchange, '', false, $bindingArgs);

echo "[{$queue}] Aguardando mensagens com formato=pdf E prioridade=alta. CTRL+C para sair.\n";
flush();

$channel->basic_consume($queue, '', false, true, false, false, function ($msg) use ($queue) {
    $headers = $msg->get('application_headers')->getNativeData();
    echo "[{$queue}] headers=" . json_encode($headers) . " body=\"{$msg->getBody()}\"\n";
    flush();
});

while ($channel->is_consuming()) {
    $channel->wait();
}

$channel->close();
$connection->close();
```

- [ ] **Step 3: Write `headers/consumer_match_any.php` (`x-match=any`)**

```php
<?php

/**
 * x-match=any -- a mensagem é roteada para esta fila se ela tiver
 * PELO MENOS UM dos headers exigidos: formato=pdf OU prioridade=alta.
 */

require __DIR__ . '/../config.php';

use PhpAmqpLib\Wire\AMQPTable;

$connection = criarConexaoRabbitMQ();
$channel = $connection->channel();

$exchange = 'eventos_headers';
$queue = 'fila_match_any';

$channel->exchange_declare($exchange, 'headers', false, true, false);
$channel->queue_declare($queue, false, true, false, false);

$bindingArgs = new AMQPTable([
    'x-match' => 'any',
    'formato' => 'pdf',
    'prioridade' => 'alta',
]);
$channel->queue_bind($queue, $exchange, '', false, $bindingArgs);

echo "[{$queue}] Aguardando mensagens com formato=pdf OU prioridade=alta. CTRL+C para sair.\n";
flush();

$channel->basic_consume($queue, '', false, true, false, false, function ($msg) use ($queue) {
    $headers = $msg->get('application_headers')->getNativeData();
    echo "[{$queue}] headers=" . json_encode($headers) . " body=\"{$msg->getBody()}\"\n";
    flush();
});

while ($channel->is_consuming()) {
    $channel->wait();
}

$channel->close();
$connection->close();
```

- [ ] **Step 4: Write `headers/README.md`**

```markdown
# Headers Exchange

Uma exchange `headers` ignora a routing key e roteia com base em pares
chave/valor colocados nos **headers** da mensagem. Cada binding define
quais headers ele exige e um argumento especial `x-match`:

- `x-match = all` -> a mensagem precisa bater em **todos** os headers do binding
- `x-match = any` -> a mensagem precisa bater em **pelo menos um**

## Cenário real

Roteamento por metadados quando a routing key não é suficiente -- ex.:
processar documentos por formato (pdf/docx) e prioridade (alta/baixa) ao
mesmo tempo.

## Topologia deste exemplo

- Exchange: `eventos_headers` (tipo `headers`)
- `fila_match_all` <- binding `x-match=all, formato=pdf, prioridade=alta`
- `fila_match_any` <- binding `x-match=any, formato=pdf, prioridade=alta`

## Mensagens publicadas e para onde vão

| headers da mensagem                     | `fila_match_all` | `fila_match_any` |
|-------------------------------------------|:-----------------:|:-----------------:|
| `formato=pdf, prioridade=alta`            | ✅                 | ✅                 |
| `formato=pdf, prioridade=baixa`           |                    | ✅ (bate em formato)|
| `formato=docx, prioridade=alta`           |                    | ✅ (bate em prioridade)|
| `formato=docx, prioridade=baixa`          |                    |                    |

## Como rodar

Em 2 terminais separados:
```bash
php headers/consumer_match_all.php
php headers/consumer_match_any.php
```

Em outro terminal:
```bash
php headers/producer.php
```
```

- [ ] **Step 5: Testar o exemplo**

Run:
```bash
timeout 8 php headers/consumer_match_all.php > /tmp/headers_all.log 2>&1 &
timeout 8 php headers/consumer_match_any.php > /tmp/headers_any.log 2>&1 &
sleep 2
php headers/producer.php
sleep 2
grep -q "Relatório financeiro" /tmp/headers_all.log && \
  ! grep -q "Manual do usuário" /tmp/headers_all.log && \
  ! grep -q "Contrato" /tmp/headers_all.log && \
  ! grep -q "Rascunho" /tmp/headers_all.log && echo "PASS: fila_match_all recebeu só a mensagem que bate nos 2 headers"

grep -q "Relatório financeiro" /tmp/headers_any.log && \
  grep -q "Manual do usuário" /tmp/headers_any.log && \
  grep -q "Contrato" /tmp/headers_any.log && \
  ! grep -q "Rascunho" /tmp/headers_any.log && echo "PASS: fila_match_any recebeu as 3 que batem em pelo menos 1 header"
wait
```
Expected: both `PASS:` lines are printed.

- [ ] **Step 6: Commit**

```bash
git add headers/
git commit -m "feat: add headers exchange example (document routing by format/priority)"
```

---

## Task 6: README raiz (conceitos gerais + guia de execução)

**Files:**
- Create: `README.md`

**Interfaces:**
- Consumes: the folder layout and run commands established in Tasks 1-5 (`direct/`, `topic/`, `fanout/`, `headers/`, `docker-compose.yml`).

- [ ] **Step 1: Write `README.md`**

```markdown
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
```

- [ ] **Step 2: Verificar links/comandos do README manualmente**

Run:
```bash
test -f direct/README.md && test -f topic/README.md && test -f fanout/README.md && test -f headers/README.md && echo "PASS: todos os READMEs de exemplo existem"
```
Expected: `PASS: todos os READMEs de exemplo existem`

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: add root README with RabbitMQ concepts and run instructions"
```
