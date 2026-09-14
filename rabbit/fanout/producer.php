<?php

/**
 * FANOUT EXCHANGE
 * ----------------
 * Uma exchange "fanout" ignora completamente a routing key: toda
 * mensagem publicada é entregue a TODAS as filas ligadas (bound) a ela.
 * É um broadcast puro.
 *
 * Cenário real: evento "novo usuário cadastrado" que precisa disparar
 * várias ações independentes ao mesmo tempo (email de boas-vindas, SMS,
 * log de auditoria).
 */

require __DIR__ . '/../config.php';

use PhpAmqpLib\Message\AMQPMessage;

$connection = criarConexaoRabbitMQ();
$channel = $connection->channel();

$exchange = 'eventos_fanout';
$channel->exchange_declare($exchange, 'fanout', false, true, false);

$mensagens = [
    "Novo usuário 'maria@example.com' cadastrado",
    "Novo usuário 'joao@example.com' cadastrado",
];

foreach ($mensagens as $corpo) {
    $msg = new AMQPMessage($corpo, [
        'delivery_mode' => AMQPMessage::DELIVERY_MODE_PERSISTENT,
    ]);

    // A routing key é irrelevante para fanout -- publicamos com string
    // vazia de propósito, para deixar isso explícito.
    $channel->basic_publish($msg, $exchange, '');

    echo "[Producer] Publicado (broadcast) body=\"{$corpo}\"\n";
}

$channel->close();
$connection->close();

echo "\nTodas as mensagens foram publicadas para TODAS as filas ligadas.\n";
