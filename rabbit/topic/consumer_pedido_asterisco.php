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
    $routingKeyRecebida = $msg->getRoutingKey();
    echo "[{$queue}] routing_key='{$routingKeyRecebida}' body=\"{$msg->getBody()}\"\n";
    flush();
});

while ($channel->is_consuming()) {
    $channel->wait();
}

$channel->close();
$connection->close();
