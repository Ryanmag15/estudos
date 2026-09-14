<?php

/**
 * DIRECT EXCHANGE
 * ----------------
 * Uma exchange "direct" roteia a mensagem para a(s) fila(s) cuja binding
 * key seja EXATAMENTE IGUAL à routing key da mensagem. É o tipo de
 * roteamento mais simples: um "match" exato, como um switch/case.
 *
 * Cenário real: log de sistema, onde cada nível de severidade
 * (info/warning/error) deve ir para um handler diferente.
 */

require __DIR__ . '/../config.php';

use PhpAmqpLib\Message\AMQPMessage;

$connection = criarConexaoRabbitMQ();
$channel = $connection->channel();

$exchange = 'logs_direct';
$channel->exchange_declare($exchange, 'direct', false, true, false);

$mensagens = [
    ['routing_key' => 'info',    'corpo' => 'Usuário 42 fez login com sucesso'],
    ['routing_key' => 'warning', 'corpo' => 'Uso de memória em 82%'],
    ['routing_key' => 'error',   'corpo' => 'Falha ao conectar no banco de dados'],
];

foreach ($mensagens as $item) {
    $msg = new AMQPMessage($item['corpo'], [
        'delivery_mode' => AMQPMessage::DELIVERY_MODE_PERSISTENT,
    ]);

    $channel->basic_publish($msg, $exchange, $item['routing_key']);

    echo "[Producer] Publicado routing_key='{$item['routing_key']}' body=\"{$item['corpo']}\"\n";
    echo "  -> Deve ir para a(s) fila(s) com binding key == '{$item['routing_key']}'\n";
}

$channel->close();
$connection->close();

echo "\nTodas as mensagens foram publicadas.\n";
