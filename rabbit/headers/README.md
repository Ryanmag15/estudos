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
