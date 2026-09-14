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
