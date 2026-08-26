<?php
## Fase 1 — Lógica, Algoritmos e Estruturas de Dados (4 semanas)

### Semana 2 — Algoritmos clássicos
// - [ ] Dia 1: Busca linear e binária — vídeo + implementar em PHP

$array = [1, 3, 5, 7, 9, 11, 13, 15];
// Busca linear: percorre o array elemento por elemento até achar o valor (funciona em array desordenado, mas é lenta)
function buscaLinear($array, $valor)
{
    foreach ($array as $indice => $elemento) {
        if ($elemento === $valor) {
            return $indice; // Retorna o índice do elemento encontrado
        }
    }
    return -1; // Retorna -1 se o elemento não for encontrado
}

echo "Resultado da busca linear: " . buscaLinear($array, 7) . "\n"; // Saída: 3


// Busca binária: divide o array ao meio repetidamente e descarta a metade que não pode conter o valor (exige array ordenado, é bem mais rápida)
function buscaBinaria($array, $valor)
{
    $inicio = 0;
    $fim = count($array) - 1;
    while ($inicio <= $fim) {
        $meio = intdiv($inicio + $fim, 2);
        if ($array[$meio] === $valor) {
            return $meio; // Retorna o índice do elemento encontrado
        } elseif ($array[$meio] < $valor) {
            $inicio = $meio + 1;
        } else {
            $fim = $meio - 1;
        }
    }
    return -1; // Retorna -1 se o elemento não for encontrado
}

echo "Resultado da busca binária: " . buscaBinaria($array, 7) . "\n"; // Saída: 3

// - [ ] Dia 2: Ordenação — bubble, selection, insertion — vídeo + implementar

$array = [64, 34, 25, 12, 22, 11, 90];
// Bubble Sort: compara pares de elementos vizinhos e troca de lugar quando estão fora de ordem, "borbulhando" o maior valor até o fim a cada passada
function bubbleSort($array)
{
    $n = count($array);
    for ($i = 0; $i < $n - 1; $i++) {
        for ($j = 0; $j < $n - $i - 1; $j++) {
            if ($array[$j] > $array[$j + 1]) {
                // Troca os elementos
                $temp = $array[$j];
                $array[$j] = $array[$j + 1];
                $array[$j + 1] = $temp;
            }
        }
    }
    return $array;
}

echo "Array ordenado com Bubble Sort: " . implode(", ", bubbleSort($array)) . "\n"; // Saída: 11, 12, 22, 25, 34, 64, 90

$array = [64, 34, 25, 12, 22, 11, 90];
// Selection Sort: a cada passada, encontra o menor elemento restante e o coloca na posição correta
function selectionSort($array)
{
    $n = count($array);
    for ($i = 0; $i < $n - 1; $i++) {
        $minIndex = $i;
        for ($j = $i + 1; $j < $n; $j++) {
            if ($array[$j] < $array[$minIndex]) {
                $minIndex = $j;
            }
        }
        // Troca os elementos
        $temp = $array[$minIndex];
        $array[$minIndex] = $array[$i];
        $array[$i] = $temp;
    }
    return $array;
}

echo "Array ordenado com Selection Sort: " . implode(", ", selectionSort($array)) . "\n"; // Saída: 11, 12, 22, 25, 34, 64, 90

$array = [64, 34, 25, 12, 22, 11, 90];
// Insertion Sort: pega cada elemento e o insere na posição correta dentro da parte já ordenada do array (como organizar cartas na mão)
function insertionSort($array)
{
    $n = count($array);
    for ($i = 1; $i < $n; $i++) {
        $key = $array[$i];
        $j = $i - 1;
        while ($j >= 0 && $array[$j] > $key) {
            $array[$j + 1] = $array[$j];
            $j--;
        }
        $array[$j + 1] = $key;
    }
    return $array;
}

echo "Array ordenado com Insertion Sort: " . implode(", ", insertionSort($array)) . "\n"; // Saída: 11, 12, 22, 25, 34, 64, 90


// - [ ] Dia 3: Merge sort e quick sort — vídeo + implementar
$mergeArray = [38, 27, 43, 3, 9, 82, 10];
// Merge Sort: divide o array ao meio recursivamente até sobrar 1 elemento, depois intercala (merge) as metades já ordenadas
function mergeSort($array)
{
    if (count($array) <= 1) {
        return $array;
    }
    $meio = intdiv(count($array), 2);
    $esquerda = array_slice($array, 0, $meio);
    $direita = array_slice($array, $meio);
    return merge(mergeSort($esquerda), mergeSort($direita));
}

function merge($esquerda, $direita)
{
    $resultado = [];
    while (count($esquerda) > 0 && count($direita) > 0) {
        if ($esquerda[0] <= $direita[0]) {
            $resultado[] = array_shift($esquerda);
        } else {
            $resultado[] = array_shift($direita);
        }
    }
    return array_merge($resultado, $esquerda, $direita);
}

echo "Array ordenado com Merge Sort: " . implode(", ", mergeSort($mergeArray)) . "\n"; // Saída: 3, 9, 10, 27, 38, 43, 82

$quickArray = [10, 7, 8, 9, 1, 5];
// Quick Sort: escolhe um pivô, separa os menores e os maiores que ele, e ordena cada grupo recursivamente
function quickSort($array)
{
    if (count($array) <= 1) {
        return $array;
    }
    $pivo = $array[0];
    $menores = [];
    $maiores = [];
    for ($i = 1; $i < count($array); $i++) {
        if ($array[$i] < $pivo) {
            $menores[] = $array[$i];
        } else {
            $maiores[] = $array[$i];
        }
    }
    return array_merge(quickSort($menores), [$pivo], quickSort($maiores));
}

echo "Array ordenado com Quick Sort: " . implode(", ", quickSort($quickArray)) . "\n"; // Saída: 1, 5, 7, 8, 9, 10

// - [ ] Dia 4: Complexidade — Big O — vídeo + aplicar a código PHP real seu
// Big O mede como o tempo de execução cresce conforme o tamanho da entrada (n) aumenta

function medirTempo(callable $funcao): float
{
    $inicio = microtime(true);

    $funcao();

    return microtime(true) - $inicio;
}

$array = range(1, 10000);

// Complexidade O(n)
$tempoLinear = medirTempo(function () use ($array) {
    foreach ($array as $valor) {
        $valor * 2;
    }
});

// Complexidade O(n²)
$tempoQuadratico = medirTempo(function () use ($array) {
    foreach ($array as $i) {
        foreach ($array as $j) {
            $i + $j;
        }
    }
});

// Complexidade O(log n) e O(n log n) são mais difíceis de medir diretamente em PHP, mas podem ser inferidas a partir de algoritmos conhecidos, como busca binária (O(log n)) e merge sort (O(n log n)).
$tempoLogaritmico = medirTempo(function () use ($array) {
    $inicio = 0;
    $fim = count($array) - 1;
    $valorProcurado = 5000;
    while ($inicio <= $fim) {
        $meio = intdiv($inicio + $fim, 2);
        if ($array[$meio] === $valorProcurado) {
            break;
        } elseif ($array[$meio] < $valorProcurado) {
            $inicio = $meio + 1;
        } else {
            $fim = $meio - 1;
        }
    }
});

$tempoNLogN = medirTempo(function () use ($array) {
    mergeSort($array);
});

echo "O(n): {$tempoLinear}s\n";
echo "O(n²): {$tempoQuadratico}s\n";
echo "O(log n): {$tempoLogaritmico}s\n";
echo "O(n log n): {$tempoNLogN}s\n";

// - [ ] Dia 5: Recursão e backtracking — vídeo + exercício
// Recursão: função que chama a si mesma até atingir um caso base, que interrompe as chamadas
function fatorial($n)
{
    if ($n <= 1) {
        return 1;
    }
    return $n * fatorial($n - 1);
}

function fibonacci($n)
{
    if ($n <= 1) {
        return $n;
    }
    return fibonacci($n - 1) + fibonacci($n - 2);
}

echo "Fatorial de 5: " . fatorial(5) . "\n"; // Saída: 120
echo "Fibonacci de 5: " . fibonacci(5) . "\n"; // Saída: 5