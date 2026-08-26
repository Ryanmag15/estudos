<?php
## Fase 1 — Lógica, Algoritmos e Estruturas de Dados (4 semanas)

### Semana 1 — Lógica de programação
// - [ ] Dia 1: Variáveis, tipos e escopo — vídeo + revisão em PHP
// Tipos básicos do PHP: string = "texto entre aspas" | integer = número inteiro | float = número com casas decimais | boolean = true/false
$dinheiro = 1000;
$mensagem = "Olá, mundo!";
$tipo = gettype($dinheiro);
$tipoMensagem = gettype($mensagem);
echo "O tipo da variável dinheiro é: $tipo\n"; // Saída: integer
echo "O tipo da variável mensagem é: $tipoMensagem\n"; // Saída: string


// - [ ] Dia 2: Operadores (aritméticos, lógicos, relacionais) — vídeo + prática
// Operadores lógicos combinam booleanos (|| = OU, && = E); operadores relacionais comparam valores (==, <, >, etc.)
$verdadeira = true;
$falsa = false;
$ou = $verdadeira || $falsa; // true
$e = $verdadeira && $falsa; // false
$igual = (5 == 5); // true

echo "Resultado do operador OU: $ou\n"; // Saída: true
echo "Resultado do operador E: $e\n"; // Saída: false


// - [ ] Dia 3: Estruturas condicionais (if/else, switch/match) — vídeo + prática
// if/elseif/else testa condições em sequência; switch/match comparam um valor contra vários casos possíveis
$numero = -1;
if ($numero > 0) {
    echo "$numero é positivo\n";
} elseif ($numero < 0) {
    echo "$numero é negativo\n";
} else {
    echo "$numero é zero\n";
}

$teste = true;
$teste = true;
switch ($teste) {
    case true:
        echo "O valor é verdadeiro\n";
        break;
    case false:
        echo "O valor é falso\n";
        break;
    default:
        echo "Valor desconhecido\n";
}

$matchValue = 2;
$resultado = match ($matchValue) {
    1 => "Um",
    2 => "Dois",
    3 => "Três",
    default => "Outro número",
};
echo "Resultado do match: $resultado\n"; // Saída: Dois

// - [ ] Dia 4: Laços (for, while, do-while, foreach) — vídeo + prática
// Laços repetem um bloco de código; while checa a condição antes, do-while depois, for controla um contador, foreach percorre arrays
$teste = 0;
while ($teste < 5) {
    echo "Valor de teste: $teste\n";
    $teste++;
}

$teste2 = 0;
do {
    echo "Valor de teste2: $teste2\n";
    $teste2++;
} while ($teste2 < 5);

$teste3 = 0;
for ($teste3 = 0; $teste3 < 5; $teste3++) {
    echo "Valor de teste3: $teste3\n";
}

$teste4Array = [1, 2, 3, 4, 5];
foreach ($teste4Array as $valor) {
    echo "Valor do array: $valor\n";
}

$teste5Array = ["a" => 1, "b" => 2, "c" => 3];
foreach ($teste5Array as $chave => $valor) {
    echo "Chave: $chave, Valor: $valor\n";
}

$teste6Array = [1, 2, 3, 4, 5];
foreach ($teste6Array as $valor) {
    if ($valor === 3) {
        continue; // Pula o valor 3
    }
    echo "Valor do array (sem o 3): $valor\n";
}

$teste7Array = [1, 2, 3, 4, 5];
foreach ($teste7Array as $valor) {
    if ($valor === 4) {
        break; // Interrompe o loop quando o valor é 4
    }
    echo "Valor do array (até o 4): $valor\n";
}

// - [ ] Dia 5: Funções e modularização — vídeo + prática
// Funções isolam um pedaço de lógica reutilizável, recebendo parâmetros e retornando um valor
function somar($a, $b) {
    return $a + $b;
}

$resultadoSoma = somar(5, 10);
echo "Resultado da soma: $resultadoSoma\n"; // Saída: 15

function saudacao($nome) {
    return "Olá, $nome! \n";
}

$mensagemSaudacao = saudacao("Ryan");
echo $mensagemSaudacao; // Saída: Olá, Ryan!

