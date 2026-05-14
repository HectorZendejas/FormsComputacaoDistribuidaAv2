# FormsCompDistri

Este projeto implementa a arquitetura da imagem da questão usando Docker Compose e uma ferramenta de carga (Locust).

A proposta é criar um `docker-compose.yml` que reflita:

- um serviço `Product page` que atende requisições externas
- três serviços `Reviews-v1`, `Reviews-v2` e `Reviews-v3`
- um serviço `Details`
- um serviço `Ratings`
- um gerador de carga que ataca apenas o serviço `Product page`

O propósito é demonstrar a conexão entre microserviços e controlar o acesso conforme o diagrama.

## Estrutura e implementação

### Serviços

- `productpage`: aplicação em Python que representa o front-end de comércio eletrônico
- `reviews-v1`, `reviews-v2`, `reviews-v3`: serviços de avaliação em Java
- `details`: serviço de detalhes do produto em Ruby
- `ratings`: serviço de notas em Node.js
- `locust`: serviço Locust que gera carga apenas contra `productpage`

### Redes e isolamento

Para que a arquitetura siga o diagrama, o `docker-compose.yml` define quatro redes:

- `frontend-net`
  - conecta `productpage` e `locust`
  - permite que o gerador de carga acesse apenas o front-end
- `reviews-net`
  - conecta `productpage` aos três serviços de reviews
  - permite que `productpage` busque avaliações
- `details-net`
  - conecta `productpage` ao serviço `details`
  - garante acesso direto a detalhes do produto
- `ratings-net`
  - conecta `reviews-v1`, `reviews-v2`, `reviews-v3` ao serviço `ratings`
  - impede que `details` e `productpage` acessem `ratings` diretamente

### Fluxo de requisições

Com essa configuração:

- O cliente (via `locust`) acessa `productpage`.
- `productpage` pode encaminhar chamadas para `reviews-v1`, `reviews-v2`, `reviews-v3` e `details`.
- Cada serviço de `reviews` pode chamar `ratings`.
- `details` não tem rota para `ratings`.
- `locust` não tem acesso direto a `reviews`, `details` ou `ratings`.

Isso reproduz o isolamento de rede do diagrama e mantém a topologia de dependências correta.

## Imagens de container usadas

As imagens seguem o enunciado e representam as tecnologias indicadas:

- `docker.io/istio/examples-bookinfo-productpage-v1:1.20.0`
- `docker.io/istio/examples-bookinfo-reviews-v1:1.20.0`
- `docker.io/istio/examples-bookinfo-reviews-v2:1.20.0`
- `docker.io/istio/examples-bookinfo-reviews-v3:1.20.0`
- `docker.io/istio/examples-bookinfo-details-v1:1.20.0`
- `docker.io/istio/examples-bookinfo-ratings-v1:1.20.0`
- `locustio/locust:2.24.0`

## Como usar o projeto

1. Abra um terminal na pasta do projeto.
2. Suba todos os serviços com:

```powershell
docker compose up -d
```

3. Verifique se os containers foram iniciados:

```powershell
docker compose ps
```

4. Abra o Locust no navegador em:

```text
http://localhost:8089
```

5. No formulário do Locust, configure o host como:

```text
http://productpage:9080
```

6. Escolha:

- número de usuários simulados
- taxa de criação de usuários (spawn rate)

7. Clique em **Start swarming** para iniciar a carga.

## Como o Locust está configurado

O `locustfile.py` usa a classe `ProductPageUser` e define três tipos de requisição:

- `GET /productpage` (peso 5): acesso à página principal
- `GET /productpage?u=normal` (peso 2): acesso à página de produto com usuário normal
- `GET /health` (peso 1): verificação de saúde do serviço

Essa configuração simula um padrão de uso realista, com foco no tráfego do front-end.

## Métricas de carga e análise

Durante o teste, observe estas métricas no painel do Locust:

- Requests por segundo (RPS)
- Tempo de resposta médio
- Percentis de latência: `p50`, `p95`, `p99`
- Taxa de erros (failures)
- Número de usuários ativos

### Como identificar saturação

A aplicação é considerada saturada quando:

- o RPS deixa de subir mesmo com mais usuários
- a latência `p95` cresce muito rápido
- a taxa de erros aumenta

Nesse caso, o serviço não consegue atender mais requisições de forma estável.

## Comandos úteis

- Parar e remover os containers:

```powershell
docker compose down
```

- Exibir os logs de um serviço:

```powershell
docker compose logs <servico>
```

- Atualizar imagens manualmente:

```powershell
docker compose pull
```

- Fazer login no Docker Hub se houver erro de pull:

```powershell
docker login
```

## Observações importantes

- A chave `version` no `docker-compose.yml` é obsoleta e pode ser removida.
- A arquitetura está montada de forma que o `productpage` é o único ponto de entrada para a carga, como exige o enunciado.
- O ponto de saturação deve ser identificado no painel do Locust, não apenas pelo número de usuários.
- Se houver falha de autenticação no Docker Hub (`failed to fetch oauth token`, `status 522`), aguarde alguns minutos e tente novamente.

## Arquivos principais

- `docker-compose.yml`: define serviços, redes e dependências
- `locustfile.py`: define o cenário de carga para `productpage`
