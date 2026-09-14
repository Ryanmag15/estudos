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
