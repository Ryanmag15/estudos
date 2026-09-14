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
