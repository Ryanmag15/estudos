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
