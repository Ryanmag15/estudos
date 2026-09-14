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
