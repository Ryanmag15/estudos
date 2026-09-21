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
python3 topic/consumer_pedido_asterisco.py
python3 topic/consumer_aprovado_asterisco.py
python3 topic/consumer_pedido_hash.py
```

Em outro terminal:
```bash
python3 topic/producer.py
```
