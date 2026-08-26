## Fase 1 — Lógica, Algoritmos e Estruturas de Dados (4 semanas)

### Semana 1 — Lógica de programação
- [ ] Dia 1: Variáveis, tipos e escopo — vídeo + revisão em PHP
- [ ] Dia 2: Operadores (aritméticos, lógicos, relacionais) — vídeo + prática
- [ ] Dia 3: Estruturas condicionais (if/else, switch/match) — vídeo + prática
- [ ] Dia 4: Laços (for, while, do-while, foreach) — vídeo + prática
- [ ] Dia 5: Funções e modularização — vídeo + prática

### Semana 2 — Algoritmos clássicos
- [ ] Dia 1: Busca linear e binária — vídeo + implementar em PHP
- [ ] Dia 2: Ordenação — bubble, selection, insertion — vídeo + implementar
- [ ] Dia 3: Merge sort e quick sort — vídeo + implementar
- [ ] Dia 4: Complexidade — Big O — vídeo + aplicar a código PHP real seu
- [ ] Dia 5: Recursão e backtracking — vídeo + exercício

### Semana 3 — Estruturas de dados lineares
- [ ] Dia 1: Arrays — vídeo + revisão
- [ ] Dia 2: Listas ligadas — vídeo + implementar em PHP
- [ ] Dia 3: Pilhas (stack) — vídeo + SplStack na prática
- [ ] Dia 4: Filas (queue) — vídeo + SplQueue na prática
- [ ] Dia 5: Exercício combinando pilha e fila (ex: validar parênteses, fila de atendimento)

### Semana 4 — Estruturas de dados não lineares
- [ ] Dia 1: Árvores (BST) — vídeo
- [ ] Dia 2: Árvores balanceadas (AVL) — vídeo conceitual
- [ ] Dia 3: Grafos — representação — vídeo
- [ ] Dia 4: BFS/DFS — vídeo + implementar um dos dois
- [ ] Dia 5: Hash tables e colisões — vídeo + fechar entrega

💡 *Dica:* mesmo já sabendo o básico, o ganho aqui é enxergar essas estruturas dentro do código que você já escreve (índice de banco é árvore, array do PHP é hash table).

*Entrega:* 2-3 desafios de algoritmos (estilo LeetCode easy/medium) + 1 exercício combinando estruturas, tudo em PHP puro.

---

## Fase 2 — Paradigmas de Programação (4 semanas)

### Semana 5 — Orientação a objetos
- [ ] Dia 1: Classes e objetos — vídeo + revisão
- [ ] Dia 2: Herança — vídeo + exemplo
- [ ] Dia 3: Polimorfismo — vídeo + exemplo
- [ ] Dia 4: Interfaces — vídeo + exemplo
- [ ] Dia 5: Encapsulamento e abstração — vídeo + exemplo

### Semana 6 — SOLID aplicado
- [ ] Dia 1: Single Responsibility — vídeo com exemplo Laravel
- [ ] Dia 2: Open/Closed — vídeo com exemplo Laravel
- [ ] Dia 3: Liskov Substitution — vídeo com exemplo Laravel
- [ ] Dia 4: Interface Segregation — vídeo com exemplo Laravel
- [ ] Dia 5: Dependency Inversion + Service Container do Laravel — vídeo + iniciar entrega

*Entrega:* refatorar um trecho de código legado seu aplicando ao menos 2 princípios SOLID.

### Semana 7 — Programação funcional e PHP moderno
- [ ] Dia 1: Funções puras e imutabilidade — vídeo
- [ ] Dia 2: Map/filter/reduce e Collections do Laravel — vídeo + prática
- [ ] Dia 3: Closures e higher-order functions — vídeo
- [ ] Dia 4: Generators e first-class callable syntax — vídeo
- [ ] Dia 5: Tipagem estrita, enums, readonly properties (PHP 8.1+) — vídeo + fechar entrega

*Entrega:* reescrever um trecho imperativo do seu código usando Collections/pipeline funcional.

### Semana 8 — Outros paradigmas
- [ ] Dia 1: Programação procedural — vídeo (quando ainda faz sentido usar)
- [ ] Dia 2: Programação reativa — vídeo conceitual
- [ ] Dia 3: Event-driven programming — vídeo + exemplo (Events/Listeners do Laravel)
- [ ] Dia 4: Programação declarativa — vídeo (SQL, Blade, Eloquent como exemplos)
- [ ] Dia 5: Quando usar cada paradigma — reflexão e notas

💡 *Dica:* resolva o mesmo problema em POO e em estilo funcional. O contraste é o aprendizado.

---

## Fase 3 — Sistemas e Infraestrutura, Docker incluso (6 semanas)

### Semana 9 — Fundamentos de containers (usar antes de configurar)
- [ ] Dia 1: O que é um container e diferença pra uma VM — vídeo
- [ ] Dia 2: Imagens vs containers, registries (Docker Hub) — vídeo
- [ ] Dia 3: Rodar e operar um docker-compose já pronto (subir, entrar no container, ver logs) — prática
- [ ] Dia 4: Comandos do dia a dia (ps, logs, exec, volumes) — prática
- [ ] Dia 5: Ler um Dockerfile existente de outro projeto, linha por linha — prática

💡 *Dica:* essa semana é a diferença entre "sei rodar Docker" e "sei o que o Docker está fazendo". Não pule mesmo se já usa Docker há um tempo.

### Semana 10 — Sistemas operacionais e Linux essencial
- [ ] Dia 1: Processos e threads — vídeo
- [ ] Dia 2: Concorrência e gerenciamento de memória — vídeo
- [ ] Dia 3: Sistema de arquivos e I/O — vídeo
- [ ] Dia 4: Signals — vídeo
- [ ] Dia 5: Linux CLI essencial (permissões, systemd, logs) — vídeo + prática no terminal

### Semana 11 — Redes e protocolos
- [ ] Dia 1: Modelo OSI e TCP/IP — vídeo
- [ ] Dia 2: HTTP/HTTPS em profundidade — vídeo
- [ ] Dia 3: DNS — vídeo
- [ ] Dia 4: TLS e certificados — vídeo
- [ ] Dia 5: REST vs gRPC vs WebSocket + sockets — vídeo

### Semana 12 — Git avançado e Docker na prática
- [ ] Dia 1: Git branching e merge — vídeo + prática
- [ ] Dia 2: Git rebase e resolução de conflitos — vídeo + prática
- [ ] Dia 3: Shell scripting e SSH/chaves — vídeo + prática
- [ ] Dia 4: Dockerfile multi-stage otimizado para PHP — vídeo + prática
- [ ] Dia 5: docker-compose completo (php-fpm, nginx, mysql, redis, mailhog) — vídeo + fechar entrega

*Entrega:* dockerizar um projeto Laravel do zero (agora configurando de verdade, já com a base da Semana 9).

### Semana 13 — Deploy e CI/CD
- [ ] Dia 1: Nginx — virtual host e proxy reverso — vídeo + prática
- [ ] Dia 2: SSL com Let's Encrypt/Certbot — vídeo + prática
- [ ] Dia 3: Supervisor para queues e workers — vídeo + prática
- [ ] Dia 4: GitHub Actions — lint e testes — vídeo + prática
- [ ] Dia 5: GitHub Actions — build e deploy automático — vídeo + fechar entrega

*Entrega:* subir o projeto dockerizado numa VPS real (DigitalOcean/Hetzner/Lightsail) com pipeline de CI/CD funcionando.

### Semana 14 — Observabilidade e segurança de infra
- [ ] Dia 1: Logs estruturados — vídeo
- [ ] Dia 2: Sentry/Bugsnag — vídeo + integrar no projeto
- [ ] Dia 3: Segredos fora do repo/imagem e rate limiting — vídeo
- [ ] Dia 4: Least privilege em containers — vídeo
- [ ] Dia 5: Kubernetes — noções conceituais — vídeo + fechar entrega

*Entrega:* integrar Sentry no projeto + escrever um runbook simples ("o que fazer se o servidor cair").

---

## Fase 4 — Banco de Dados (4 semanas)

### Semana 15 — Modelagem e SQL
- [ ] Dia 1: Entidades e relacionamentos — vídeo
- [ ] Dia 2: Normalização — vídeo
- [ ] Dia 3: DDL/DML/DCL — vídeo + prática
- [ ] Dia 4: JOINs e subqueries — vídeo + prática
- [ ] Dia 5: CTEs, transactions e ACID — vídeo + fechar entrega

*Entrega:* modelar um sistema real (e-commerce ou blog) do zero antes de sair escrevendo queries.

### Semana 16 — NoSQL e CAP theorem
- [ ] Dia 1: Documento (MongoDB) — vídeo
- [ ] Dia 2: Chave-valor (Redis) — vídeo
- [ ] Dia 3: Colunar e grafo — vídeo conceitual
- [ ] Dia 4: CAP theorem — vídeo
- [ ] Dia 5: Quando usar SQL vs NoSQL — estudo de caso

### Semana 17 — Performance de queries
- [ ] Dia 1: Índices e B-tree — vídeo
- [ ] Dia 2: Composite index — vídeo
- [ ] Dia 3: EXPLAIN na prática — vídeo + prática
- [ ] Dia 4: N+1 problem com Telescope/Debugbar — vídeo + prática
- [ ] Dia 5: Connection pooling e cache de queries com Redis — vídeo + fechar entrega

*Entrega:* auditar um projeto seu, achar 3 queries lentas ou N+1 e corrigi-las com métricas de antes/depois.

### Semana 18 — Filas e replicação
- [ ] Dia 1: Queues com Redis — vídeo + prática
- [ ] Dia 2: Queues com SQS — vídeo
- [ ] Dia 3: Retries e failed jobs — vídeo + prática
- [ ] Dia 4: Sharding — vídeo conceitual
- [ ] Dia 5: Replicação (read replicas) — vídeo + fechar entrega

*Entrega:* mover uma tarefa pesada (e-mail, relatório) para uma queue com tratamento de falhas.

---

## Fase 5 — Arquitetura de Software (6 semanas)

### Semana 19 — Patterns Criacionais (5 padrões)
- [ ] Dia 1: Factory Method — vídeo + exemplo
- [ ] Dia 2: Abstract Factory — vídeo + exemplo
- [ ] Dia 3: Builder — vídeo + exemplo
- [ ] Dia 4: Prototype — vídeo + exemplo
- [ ] Dia 5: Singleton (e por que evitar na maioria dos casos) — vídeo + entrega

*Entrega:* implementar Factory Method ou Builder num fluxo real do seu projeto.

### Semana 20 — Patterns Estruturais (7 padrões)
- [ ] Dia 1: Adapter — vídeo + exemplo
- [ ] Dia 2: Bridge + Composite — vídeo
- [ ] Dia 3: Decorator — vídeo + exemplo
- [ ] Dia 4: Facade + Flyweight — vídeo
- [ ] Dia 5: Proxy — vídeo + entrega

*Entrega:* implementar Adapter ou Decorator num fluxo real (ex: integração com gateway externo).

### Semana 21 — Patterns Comportamentais (11 padrões)
- [ ] Dia 1: Chain of Responsibility + Command — vídeo
- [ ] Dia 2: Interpreter + Iterator — vídeo
- [ ] Dia 3: Mediator + Memento — vídeo
- [ ] Dia 4: Observer + State — vídeo + exemplo
- [ ] Dia 5: Strategy + Template Method + Visitor — vídeo + entrega

*Entrega:* implementar Strategy ou Observer num fluxo real (gateways de pagamento, notificações). Repository pattern aplicado ao Eloquent entra aqui como padrão adicional de acesso a dados.

💡 *Dica:* não tente decorar os 23. Domine bem Factory, Builder, Strategy, Observer, Adapter e Decorator — são os que mais aparecem em código real. Os outros, saiba reconhecer quando vir.

### Semana 22 — Padrões arquiteturais
- [ ] Dia 1: MVC — vídeo
- [ ] Dia 2: MVP e MVVM — vídeo
- [ ] Dia 3: Clean Architecture / Hexagonal — vídeo
- [ ] Dia 4: CQRS e Event Sourcing (introdução — aprofunda na Fase 7) — vídeo
- [ ] Dia 5: Monólito vs microservices — estudo de caso

### Semana 23 — Testes e qualidade
- [ ] Dia 1: PHPUnit — testes unitários — vídeo + prática
- [ ] Dia 2: PHPUnit/Pest — testes de feature — vídeo + prática
- [ ] Dia 3: Mocks e fakes — vídeo + prática
- [ ] Dia 4: TDD e BDD — vídeo conceitual
- [ ] Dia 5: Code review e refactoring — vídeo + fechar entrega

*Entrega:* suíte de testes cobrindo o módulo dos patterns (semanas 19-21), meta 70%+ de cobertura.

### Semana 24 — Segurança de aplicação
- [ ] Dia 1: OWASP Top 10 (parte 1) — vídeo
- [ ] Dia 2: OWASP Top 10 (parte 2) — vídeo
- [ ] Dia 3: JWT — vídeo + prática
- [ ] Dia 4: OAuth2 — vídeo
- [ ] Dia 5: Mass assignment e sanitização de input (Laravel específico) — vídeo + prática

💡 *Dica:* estude system designs reais (Twitter, Uber, YouTube) nessa fase — reverse engineering de arquitetura é ouro para entrevista.

---

## Fase 6 — Fullstack e Projeto Final (2 semanas)

### Semana 25 — Frontend para backend developers
- [ ] Dia 1: Fundamentos Vue.js/Inertia.js ou Livewire avançado — vídeo
- [ ] Dia 2: Componentização — vídeo + prática
- [ ] Dia 3: Consumo da própria API — vídeo + prática
- [ ] Dia 4: Estado simples — vídeo + prática
- [ ] Dia 5: Fechar entrega

*Entrega:* CRUD funcional consumindo sua própria API Laravel.

### Semana 26 — Capstone: projeto integrador
- [ ] Dia 1: Planejamento da arquitetura do projeto final
- [ ] Dia 2: Build — API + banco + regras de negócio
- [ ] Dia 3: Build — Docker + CI/CD
- [ ] Dia 4: Build — frontend + monitoramento + segurança aplicada
- [ ] Dia 5: Documentação técnica (README, decisões de arquitetura) + deploy final

*Entrega final:* projeto no ar, com link público, repositório documentado e pipeline de CI/CD visível. Isso — não um certificado — é a prova concreta de que os 6 meses de gás viraram qualidade real.

---

## Fase 7 — Bônus, fora dos 6 meses (3 semanas, opcional)

> Aqui termina o prazo dos 6 meses. Isso não é requisito para nada — é o que você estuda depois, se quiser continuar o embalo rumo a arquitetura de sistemas de escala real (staff/arquiteto) ou entrevistas mais puxadas.

### Semana 27 — CQRS e Event Sourcing
- [ ] Dia 1: CQRS — conceito e motivação — vídeo
- [ ] Dia 2: CQRS na prática (exemplo em Laravel/PHP) — vídeo
- [ ] Dia 3: Event Sourcing — conceito e motivação — vídeo
- [ ] Dia 4: Event Sourcing na prática — vídeo
- [ ] Dia 5: Estudo de caso real + notas

### Semana 28 — Sharding e CAP theorem em profundidade
- [ ] Dia 1: Estratégias de particionamento (sharding) — vídeo
- [ ] Dia 2: Consistent hashing — vídeo
- [ ] Dia 3: CAP theorem aprofundado — CP vs AP na prática — vídeo
- [ ] Dia 4: PACELC e trade-offs reais — vídeo
- [ ] Dia 5: Estudo de caso (sharding em sistemas de larga escala) + notas

### Semana 29 — gRPC e Kubernetes avançado
- [ ] Dia 1: gRPC — protocol buffers — vídeo
- [ ] Dia 2: gRPC — streaming e casos de uso reais — vídeo
- [ ] Dia 3: Kubernetes — pods, deployments, services — vídeo
- [ ] Dia 4: Kubernetes — ConfigMaps, Secrets e scaling — vídeo
- [ ] Dia 5: Kubernetes — ingress + estudo de caso + notas

---

## Fase 8 — Tópicos de Mercado Avançados (bônus, opcional, 4 semanas)

> Continuação da Fase 7. Fecha as lacunas que costumam aparecer em vagas sênior/staff: DDD, mensageria com RabbitMQ, tuning de performance PHP, observabilidade de verdade e SRE. Pré-requisito: Fases 1-7 concluídas.

### Semana 30 — Arquitetura avançada e qualidade de código
- [ ] Dia 1: DDD — conceitos táticos (entidades, value objects, agregados, bounded context) — vídeo
- [ ] Dia 2: Onion Architecture — vídeo + comparar com Clean/Hexagonal (Semana 22)
- [ ] Dia 3: Object Calisthenics — as 9 regras — vídeo + refatorar uma classe sua aplicando 3-4 regras
- [ ] Dia 4: Code Smells — catálogo (long method, god class, feature envy, shotgun surgery) — vídeo + identificar no seu código
- [ ] Dia 5: Repository pattern revisitado com lente DDD (agregados vs Eloquent) — vídeo + fechar entrega

*Entrega:* modelar um bounded context simples do projeto capstone com DDD tático (entidade + value object + repository).

### Semana 31 — RabbitMQ e Redis avançado
- [ ] Dia 1: RabbitMQ — conceitos (broker, filas, exchanges, bindings) — vídeo
- [ ] Dia 2: RabbitMQ — routing key e tipos de exchange (direct, topic, fanout) — vídeo + prática
- [ ] Dia 3: RabbitMQ — Dead Letter Queue (DLQ) e estratégias de retry — vídeo + prática
- [ ] Dia 4: RabbitMQ — ACK/NACK e garantias de entrega — vídeo + prática
- [ ] Dia 5: Redis — Pub/Sub e locks distribuídos (Redlock) — vídeo + fechar entrega

*Entrega:* worker PHP consumindo uma fila RabbitMQ com DLQ e retry configurados, tratando falha de processamento.

### Semana 32 — Performance e Observabilidade avançada
- [ ] Dia 1: Opcache — funcionamento e configuração de produção — vídeo + prática
- [ ] Dia 2: PHP-FPM — pools, processos (pm.max_children etc.) e tuning — vídeo + prática
- [ ] Dia 3: Redis — rate limiting (token bucket / sliding window) aplicado a uma API — vídeo + prática
- [ ] Dia 4: Métricas e tracing distribuído — Prometheus/StatsD e OpenTelemetry — vídeo
- [ ] Dia 5: APM na prática — Dynatrace (ou New Relic/Datadog como alternativa) — vídeo + fechar entrega

*Entrega:* instrumentar o projeto capstone com Opcache/PHP-FPM tunados + métricas básicas e um trace de uma requisição ponta a ponta.

### Semana 33 — SRE e CI/CD alternativos
- [ ] Dia 1: SLI, SLO e SLA — conceitos e diferenças — vídeo
- [ ] Dia 2: Error Budget — vídeo + definir um SLO real para o projeto capstone
- [ ] Dia 3: GitLab CI — pipelines (.gitlab-ci.yml) — vídeo + prática
- [ ] Dia 4: Jenkins — pipelines (Jenkinsfile) — vídeo + prática (pode ser conceitual se não tiver ambiente)
- [ ] Dia 5: GitHub Actions vs GitLab CI vs Jenkins — comparação e trade-offs — notas + fechar bônus

*Entrega:* SLO/SLA documentado para o projeto capstone + pipeline alternativo (GitLab CI ou Jenkins) rodando em paralelo ao GitHub Actions.

💡 *Dica:* essa fase é a diferença entre "sei usar Laravel" e "sei operar um sistema PHP em produção, em escala, com gente de plantão". É o que separa pleno de sênior/staff nas entrevistas.
