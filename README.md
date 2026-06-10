# World Cup Chatbot

Este repositório contém uma API em FastAPI com suporte a banco Postgres e uma interface/integração estática.

## Requisitos

- Docker & Docker Compose (recomendado)
- Python 3.13 (se for rodar localmente)
- Poetry (opcional, para instalação local)

## Variáveis de ambiente

Crie um arquivo `.env` na raiz com as variáveis necessárias (exemplo):

```
POSTGRES_USER=wc_user
POSTGRES_PASSWORD=wc_password
DB_NAME=wc_db
PG_DATA=/var/lib/postgresql/data
PGADMIN4_EMAIL=admin@example.com
PGADMIN4_PASSWORD=admin
SQLALCHEMY_DATABASE_URL=postgresql://wc_user:wc_password@postgres:5432/wc_db
```

A aplicação lê as variáveis via `python-dotenv` e `src/config.py`.

## Como rodar (recomendado): Docker Compose

1. Certifique-se de que o `.env` está configurado.
2. Na raiz do projeto, execute:

```bash
docker compose up --build
```

- A API ficará disponível em `http://localhost:8000`.
- O PostgreSQL ficará na porta `5432` (mapeado localmente).
- O pgAdmin ficará na porta `5050`.

Para parar e remover volumes:

```bash
docker compose down -v
```

## Como rodar localmente (sem Docker)

1. Instale Python 3.13.
2. Crie e ative um ambiente virtual:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
```

3. Instale o Poetry e as dependências:

```bash
pip install poetry
poetry config virtualenvs.create false
poetry install
```

4. Configure o arquivo `.env` com as variáveis do banco.

5. Inicie a aplicação:

```bash
uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
```

## Testes

Há uma suíte de testes em `tests/`. Para executar:

```bash
pytest
# ou via taskipy (se instalado)
# task test
```

## Observações

- O `Dockerfile` usa `uvicorn src.app:app` como comando de inicialização.
- O `pyproject.toml` define dependências e tasks (`run` usa `docker compose up --build`).
- Ajuste `SQLALCHEMY_DATABASE_URL` para apontar para o serviço Postgres quando rodar com Docker (exemplo acima usa `postgres` como hostname do serviço Docker).

Se quiser, eu posso adicionar um `.env.example` automático baseado nas variáveis detectadas ou melhorar instruções de migração com Alembic.