# Direct Exchange

Uma exchange `direct` roteia a mensagem para a(s) fila(s) cuja **binding
key** seja **exatamente igual** à **routing key** da mensagem publicada.
É um match exato — sem padrões, sem wildcards.

## Cenário real

Sistema de log: cada nível de severidade (`info`, `warning`, `error`) deve
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
