# FormsCompDistri

Projeto de exemplo que implementa a arquitetura apresentada na imagem usando Docker Compose e Locust.

## Como foi feito

O `docker-compose.yml` modela a aplicação Bookinfo como uma arquitetura de microserviços:

- `productpage` representa a página de compras (frontend Python)
- `reviews-v1`, `reviews-v2`, `reviews-v3` representam os serviços de avaliação (Java)
- `details` representa o serviço de detalhes do produto (Ruby)
- `ratings` representa o serviço de notas/ratings (Node.js)
- `locust` é o gerador de carga para testar apenas o `productpage`

A separação de redes foi definida para respeitar as regras de acesso da imagem:

- `frontend-net` conecta `productpage` e `locust`
- `reviews-net` conecta `productpage` a `reviews-v*`
- `details-net` conecta `productpage` a `details`
- `ratings-net` conecta `reviews-v*` a `ratings`

Com isso:

- `productpage` consegue acessar `reviews-v1`, `reviews-v2`, `reviews-v3` e `details`
- `reviews-v*` conseguem acessar `ratings`
- `details` não acessa `ratings`
- `locust` ataca apenas o `productpage`

## Imagens utilizadas

As imagens de container são as mesmas indicadas no enunciado:

- `docker.io/istio/examples-bookinfo-productpage-v1:1.20.0`
- `docker.io/istio/examples-bookinfo-reviews-v1:1.20.0`
- `docker.io/istio/examples-bookinfo-reviews-v2:1.20.0`
- `docker.io/istio/examples-bookinfo-reviews-v3:1.20.0`
- `docker.io/istio/examples-bookinfo-details-v1:1.20.0`
- `docker.io/istio/examples-bookinfo-ratings-v1:1.20.0`
- `locustio/locust:2.24.0`

## Como usar

1. Abra um terminal na pasta do projeto.
2. Suba os serviços:

```powershell
docker compose up -d
```

3. Verifique se os containers estão ativos:

```powershell
docker compose ps
```

4. Acesse o painel do Locust em:

```text
http://localhost:8089
```

5. No Locust, configure o host como:

```text
http://productpage:9080
```

6. Defina o número de usuários e a taxa de spawn. Em seguida, inicie o teste.

## Como o Locust foi configurado

O arquivo `locustfile.py` cria um usuário virtual `ProductPageUser` com estas tarefas:

- `GET /productpage` (peso 5)
- `GET /productpage?u=normal` (peso 2)
- `GET /health` (peso 1)

Isso simula uma carga onde o acesso à página principal é o mais frequente, e o health check também é monitorado.

## Métricas importantes

Durante o teste de carga, use o Locust para observar:

- Requests por segundo (RPS)
- Tempo de resposta médio e percentis (`p50`, `p95`, `p99`)
- Taxa de falhas (HTTP 4xx/5xx)
- Número de usuários ativos
- Curva de RPS versus usuários, para detectar saturação

### Ponto de saturação

O serviço está saturado quando:

- RPS para de crescer ou diminui com mais usuários
- latência `p95` aumenta fortemente
- taxa de erros sobe acima de 1–2%

## Comandos úteis

- Parar e remover containers:

```powershell
docker compose down
```

- Ver logs de um serviço:

```powershell
docker compose logs <servico>
```

- Fazer login no Docker Hub se o pull falhar:

```powershell
docker login
```

## Observações

O compose define redes específicas para garantir os acessos do diagrama. Essa configuração foi feita propositalmente para corresponder à arquitetura pedida na imagem.

Se o Docker Hub retornar erro de autenticação temporária (`failed to fetch oauth token`, `status 522`), aguarde alguns minutos e tente novamente.
