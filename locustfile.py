"""
locustfile.py — Teste de carga para a aplicação BookInfo
Alvo: apenas o serviço Product Page (http://productpage:9080)

Métricas coletadas pelo Locust úteis para identificar saturação:
  - Requests/s (RPS)       : taxa de requisições por segundo
  - Response Time (ms)     : tempo de resposta médio / percentis (p50, p95, p99)
  - Failure rate (%)       : percentual de erros HTTP (5xx, timeout)
  - Number of Users        : usuários virtuais simultâneos ativos
  - RPS vs Users chart     : plateau indica que o serviço atingiu saturação

Ponto de saturação:
  O serviço está saturado quando, ao aumentar o número de usuários,
  o RPS para de crescer (ou cai) enquanto o p95 de latência dispara
  e/ou a taxa de erros ultrapassa ~1-2%.
"""

from locust import HttpUser, task, between


class ProductPageUser(HttpUser):
    """Simula um usuário navegando na página de produtos."""

    # Tempo de espera entre requisições (simula leitura humana)
    wait_time = between(1, 3)

    @task(5)
    def ver_pagina_inicial(self):
        """Acessa a página principal — caminho mais frequente."""
        self.client.get("/productpage", name="GET /productpage")

    @task(2)
    def ver_produto_especifico(self):
        """Acessa um produto com avaliações e detalhes."""
        self.client.get(
            "/productpage?u=normal",
            name="GET /productpage?u=normal",
        )

    @task(1)
    def health_check(self):
        """Verifica health do serviço."""
        self.client.get("/health", name="GET /health")
