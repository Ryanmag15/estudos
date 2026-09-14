<?php

/**
 * HEADERS EXCHANGE
 * -----------------
 * Uma exchange "headers" ignora a routing key e roteia com base em
 * pares chave/valor colocados nos HEADERS da mensagem. O binding define
 * quais headers ele exige, e um argumento especial "x-match" decide a
 * regra:
 *   x-match = all -> a mensagem precisa bater em TODOS os headers do binding
 *   x-match = any -> a mensagem precisa bater em PELO MENOS UM
 *
 * Cenário real: roteamento por metadados quando a routing key não é
 * suficiente -- ex.: processar documentos por formato + prioridade.
 */

require __DIR__ . '/../config.php';

use PhpAmqpLib\Message\AMQPMessage;
use PhpAmqpLib\Wire\AMQPTable;

$connection = criarConexaoRabbitMQ();
$channel = $connection->channel();

$exchange = 'eventos_headers';
$channel->exchange_declare($exchange, 'headers', false, true, false);

$mensagens = [
    ['headers' => ['formato' => 'pdf',  'prioridade' => 'alta'],  'corpo' => "Relatório financeiro (PDF, alta prioridade)"],
    ['headers' => ['formato' => 'pdf',  'prioridade' => 'baixa'], 'corpo' => "Manual do usuário (PDF, baixa prioridade)"],
    ['headers' => ['formato' => 'docx', 'prioridade' => 'alta'],  'corpo' => "Contrato (DOCX, alta prioridade)"],
    ['headers' => ['formato' => 'docx', 'prioridade' => 'baixa'], 'corpo' => "Rascunho (DOCX, baixa prioridade)"],
];

foreach ($mensagens as $item) {
    $msg = new AMQPMessage($item['corpo'], [
        'application_headers' => new AMQPTable($item['headers']),
        'delivery_mode' => AMQPMessage::DELIVERY_MODE_PERSISTENT,
    ]);

    // Headers exchange ignora routing key -- publicamos com string vazia.
    $channel->basic_publish($msg, $exchange, '');

    $headersTexto = json_encode($item['headers']);
    echo "[Producer] Publicado headers={$headersTexto} body=\"{$item['corpo']}\"\n";
}

$channel->close();
$connection->close();

echo "\nTodas as mensagens foram publicadas.\n";
