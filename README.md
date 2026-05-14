# FormsCompDistri

Projeto de exemplo para executar a aplicação Istio Bookinfo em Docker Compose e testar carga com Locust.

## Descrição

Este repositório contém um `docker-compose.yml` que orquestra os serviços da aplicação Bookinfo e um `locustfile.py` para executar testes de carga contra o serviço `productpage`.

O objetivo é validar o comportamento da aplicação distribuída e gerar métricas de desempenho usando Locust.

## Serviços

- `productpage` - front-end do Bookinfo
- `reviews-v1`, `reviews-v2`, `reviews-v3` - serviços de avaliações
- `details` - serviço de detalhes do produto
- `ratings` - serviço de classificação
- `locust` - gerador de carga para a página de produto

## Requisitos

- Docker
- Docker Compose
- Acesso à internet para baixar imagens do Docker Hub

## Como executar

1. Abra um terminal na pasta do projeto.
2. Inicie os serviços:

```powershell
docker compose up -d
```

3. Verifique os containers:

```powershell
docker compose ps
```

4. Acesse o Locust no navegador:

```text
http://localhost:8089
```

5. Inicie o teste de carga configurando o host como:

```text
http://productpage:9080
```

## Locust

O `locustfile.py` define um usuário virtual `ProductPageUser` com três tarefas:

- `GET /productpage` (peso 5)
- `GET /productpage?u=normal` (peso 2)
- `GET /health` (peso 1)

O foco do teste é medir:

- RPS (requests por segundo)
- tempos de resposta (p50, p95, p99)
- taxa de erros
- comportamento sob aumento de usuários

## Observações

- O arquivo `docker-compose.yml` usa sintaxe do Compose V2 e a chave `version` é obsoleta. O Compose atual a ignora, mas é recomendado removê-la do arquivo.
- Caso haja falha no pull das imagens do Docker Hub, execute novamente ou faça login com:

```powershell
docker login
```

## Problemas comuns

- `failed to fetch oauth token` / `status 522`: pode ser um problema temporário de autenticação do Docker Hub.
- Se um serviço não subir, use:

```powershell
docker compose logs <servico>
```

- Para parar e remover containers:

```powershell
docker compose down
```

## Arquivos principais

- `docker-compose.yml` - configuração dos serviços e redes
- `locustfile.py` - definição do cenário de carga Locust
