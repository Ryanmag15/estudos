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
