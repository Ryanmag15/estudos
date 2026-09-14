<?php

/**
 * TOPIC EXCHANGE
 * ---------------
 * Uma exchange "topic" roteia por PADRÕES na routing key, que deve ter
 * o formato "palavra.palavra.palavra" (separado por pontos). Bindings
 * podem usar dois wildcards:
 *   *  -> substitui exatamente UMA palavra
 *   #  -> substitui ZERO ou MAIS palavras
 *
 * Cenário real: eventos de e-commerce (pedidos, pagamentos), onde cada
 * serviço assina só os padrões que lhe interessam.
 */

require __DIR__ . '/../config.php';

use PhpAmqpLib\Message\AMQPMessage;

$connection = criarConexaoRabbitMQ();
$channel = $connection->channel();

$exchange = 'eventos_topic';
$channel->exchange_declare($exchange, 'topic', false, true, false);

$mensagens = [
    ['routing_key' => 'pedido.criado',           'corpo' => "Pedido #1001 foi criado"],
    ['routing_key' => 'pedido.aprovado',         'corpo' => "Pedido #1001 foi aprovado"],
    ['routing_key' => 'pedido.cancelado',        'corpo' => "Pedido #1002 foi cancelado"],
    ['routing_key' => 'pagamento.aprovado',      'corpo' => "Pagamento do pedido #1001 foi aprovado"],
    ['routing_key' => 'pagamento.recusado',      'corpo' => "Pagamento do pedido #1003 foi recusado"],
    // Routing key com DOIS níveis depois de "pedido" -- serve para mostrar
    // na prática que "pedido.*" NÃO pega isso, mas "pedido.#" pega.
    ['routing_key' => 'pedido.item.adicionado',  'corpo' => "Item 'Teclado' foi adicionado ao pedido #1001"],
];

foreach ($mensagens as $item) {
    $msg = new AMQPMessage($item['corpo'], [
        'delivery_mode' => AMQPMessage::DELIVERY_MODE_PERSISTENT,
    ]);

    $channel->basic_publish($msg, $exchange, $item['routing_key']);

    echo "[Producer] Publicado routing_key='{$item['routing_key']}' body=\"{$item['corpo']}\"\n";
}

$channel->close();
$connection->close();

echo "\nTodas as mensagens foram publicadas.\n";
