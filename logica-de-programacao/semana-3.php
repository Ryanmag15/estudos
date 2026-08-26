<?php
## Fase 1 — Lógica, Algoritmos e Estruturas de Dados (4 semanas)
// - [ ] Dia 1: Arrays — vídeo + revisão
// Funções nativas de array do PHP: filter (filtra), map (transforma cada item), reduce (agrega tudo em um valor único)
$array = [1, 2, 3, 4, 5];
// Acessando elementos do array
echo "Primeiro elemento: " . $array[0] . "\n"; // Saída: 1
echo "Último elemento: " . $array[count($array) - 1] . "\n"; // Saída: 5
echo "Tamanho do array: " . count($array) . "\n"; // Saída: 5
echo "Array completo: " . implode(", ", $array) . "\n"; // Saída: 1, 2, 3, 4, 5
echo "Array invertido: " . implode(", ", array_reverse($array)) . "\n"; // Saída: 5, 4, 3, 2, 1
echo "Array ordenado: " . implode(", ", $array) . "\n"; // Saída: 1, 2, 3, 4, 5
echo "Array filtrado (pares): " . implode(", ", array_filter($array, fn($x) => $x % 2 === 0)) . "\n"; // Saída: 2, 4
echo "Array mapeado (quadrados): " . implode(", ", array_map(fn($x) => $x * $x, $array)) . "\n"; // Saída: 1, 4, 9, 16, 25
echo "Array reduzido (soma): " . array_reduce($array, fn($carry, $item) => $carry + $item, 0) . "\n"; // Saída: 15
echo "Array filtrado e mapeado (pares ao quadrado): " . implode(", ", array_map(fn($x) => $x * $x, array_filter($array, fn($x) => $x % 2 === 0))) . "\n"; // Saída: 4, 16
echo "Array ordenado em ordem decrescente: " . implode(", ", array_reverse($array)) . "\n"; // Saída: 5, 4, 3, 2, 1
echo "Array com elementos únicos: " . implode(", ", array_unique([1, 2, 2, 3, 4, 4, 5])) . "\n"; // Saída: 1, 2, 3, 4, 5

$arraySortido = [5, 3, 1, 4, 2];
echo "Array sortido: " . implode(", ", $arraySortido) . "\n"; // Saída: 5, 3, 1, 4, 2
sort($arraySortido);
echo "Array sortido após sort(): " . implode(", ", $arraySortido) . "\n"; // Saída: 1, 2, 3, 4, 5
rsort($arraySortido);
echo "Array sortido após rsort(): " . implode(", ", $arraySortido) . "\n"; // Saída: 5, 4, 3, 2,
echo "Array sortido após sort() e rsort(): " . implode(", ", $arraySortido) . "\n"; // Saída: 5, 4, 3, 2, 1

// - [ ] Dia 2: Listas ligadas — vídeo + implementar em PHP
// Lista ligada: cada elemento aponta para o próximo (e o anterior, no caso duplamente ligada); SplDoublyLinkedList é a implementação nativa do PHP
$lista1 = new SplDoublyLinkedList();
$lista1->push(1);
$lista1->push(2);
$lista1->push(3);
echo "Lista ligada (SplDoublyLinkedList): ";
foreach ($lista1 as $item) {
    echo $item . " " . "\n"; // Saída: 1 2 3
}

// - [ ] Dia 3: Pilhas (stack) — vídeo + SplStack na prática
// Pilha (LIFO — last in, first out): o último elemento inserido é o primeiro a sair (push/pop no topo)
$pilha = new SplStack();
$pilha->push(1);
$pilha->push(2);
echo "Topo da pilha: " . $pilha->top() . "\n"; // Saída: 2
$pilha->pop();
echo "Topo da pilha após pop: " . $pilha->top() . "\n"; // Saída: 1
echo "Tamanho da pilha: " . $pilha->count() . "\n"; // Saída: 1

// - [ ] Dia 4: Filas (queue) — vídeo + SplQueue na prática
// Fila (FIFO — first in, first out): o primeiro elemento inserido é o primeiro a sair (enqueue no fim, dequeue no início)
$fila = new SplQueue();
$fila->enqueue(1);
$fila->enqueue(2);
$fila->enqueue(3);
echo "Primeiro elemento da fila: " . $fila->bottom() . "\n"; // Saída: 1
$fila->dequeue();
echo "Primeiro elemento da fila após dequeue: " . $fila->bottom() . "\n"; // Saída: 2
echo "Tamanho da fila: " . $fila->count() . "\n"; // Saída: 2


// - [ ] Dia 5: Exercício combinando pilha e fila (ex: validar parênteses, fila de atendimento)
// Fila de atendimento (FIFO) simula um caixa/suporte; a pilha abaixo valida parênteses empilhando "(" e desempilhando a cada ")"
$filaDeAtendimento = new SplQueue();
$filaDeAtendimento->enqueue("Cliente 1");
$filaDeAtendimento->enqueue("Cliente 2");
echo "Atendendo: " . $filaDeAtendimento->dequeue() . "\n"; // Saída: Cliente 1
echo "Atendendo: " . $filaDeAtendimento->dequeue() . "\n"; // Saída: Cliente 2
echo "Fila de atendimento vazia? " . ($filaDeAtendimento->isEmpty() ? "Sim" : "Não") . "\n"; // Saída: Sim

$pilhaDeParenteses = new SplStack();
$expressao = "((a + b) * c)";
$validaParenteses = true;
for ($i = 0; $i < strlen($expressao); $i++) {
    $char = $expressao[$i];
    if ($char === '(') {
        $pilhaDeParenteses->push($char);
    } elseif ($char === ')') {
        if ($pilhaDeParenteses->isEmpty()) {    
            $validaParenteses = false;
            break;
        }
        $pilhaDeParenteses->pop();
    }
}
if (!$pilhaDeParenteses->isEmpty()) {
    $validaParenteses = false;
}
echo "Expressão '$expressao' é válida? " . ($validaParenteses ? "Sim" : "Não") . "\n"; // Saída: Sim
