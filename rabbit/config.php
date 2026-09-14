<?php

/**
 * Configuração de conexão com o RabbitMQ.
 *
 * Os valores podem ser sobrescritos por variáveis de ambiente
 * (RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USER, RABBITMQ_PASS,
 * RABBITMQ_VHOST), mas os defaults já batem com o docker-compose.yml
 * deste projeto, então "docker compose up -d" + rodar os scripts
 * já funciona sem configurar nada.
 */

require_once __DIR__ . '/vendor/autoload.php';

use PhpAmqpLib\Connection\AMQPStreamConnection;

function criarConexaoRabbitMQ(): AMQPStreamConnection
{
    $host = getenv('RABBITMQ_HOST') ?: 'localhost';
    $port = (int) (getenv('RABBITMQ_PORT') ?: 5672);
    $user = getenv('RABBITMQ_USER') ?: 'guest';
    $pass = getenv('RABBITMQ_PASS') ?: 'guest';
    $vhost = getenv('RABBITMQ_VHOST') ?: '/';

    return new AMQPStreamConnection($host, $port, $user, $pass, $vhost);
}
