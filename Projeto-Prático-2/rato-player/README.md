# 🎵 Rato Player

API REST para gerenciamento de coleções musicais com Python + FastAPI.

## 🛠 Tecnologias

- **Poetry**: Gerenciador de dependências e ambientes virtuais Python
- **FastAPI**: Framework web moderno para criação de APIs REST com documentação automática
- **SQLAlchemy**: ORM para interação com banco de dados PostgreSQL
- **Pydantic**: Validação de dados e serialização com type hints
- **Ruff**: Linter e formatador de código Python ultra-rápido
- **pytest**: Framework de testes unitários

> **⚠️ Nota importante**: O projeto não possui testes unitários :(

## 🚀 Instalação

```bash
git clone https://github.com/gustaaragao/rato-player.git
cd rato-player
poetry install
poetry shell
```

## ⚙️ Configuração

Crie um `.env` como o `.env.example`:
```env
# Postgres
POSTGRES_HOST=
POSTGRES_PORT=
POSTGRES_DB_NAME=
POSTGRES_USER=
POSTGRES_PASSWORD=

# MongoDB
MONGODB_HOST=
MONGODB_PORT=
MONGODB_DB_NAME=
MONGODB_USER=
MONGODB_PASSWORD=
```

## 🏃‍♂️ Execução

```bash
# Desenvolvimento
task run

# Testes (⚠️ atualmente com problemas de configuração)
task test

# Formatar o código
task format
task lint
```

**API:** `http://localhost:8000`  
**Docs:** `http://localhost:8000/docs`

## 🛣 API Endpoints

### Gêneros
- `POST /generos/` - Criar
- `GET /generos/` - Listar (paginação)
- `GET /generos/search` - Buscar por nome/data
- `GET /generos/{id}` - Obter por ID
- `PUT/PATCH /generos/{id}` - Atualizar
- `DELETE /generos/{id}` - Excluir

### Coleções
- `POST /colecoes/` - Criar
- `GET /colecoes/` - Listar (paginação)
- `GET /colecoes/search` - Buscar por título/tipo/data
- `GET /colecoes/{id}` - Obter por ID
- `PUT/PATCH /colecoes/{id}` - Atualizar
- `DELETE /colecoes/{id}` - Excluir
- `POST/DELETE /colecoes/{id}/generos/{genero_id}` - Gerenciar relacionamentos

## 📖 Exemplo de Uso

```bash
# Criar gênero
curl -X POST "http://localhost:8000/generos/" \
     -H "Content-Type: application/json" \
     -d '{"nome": "Rock", "surgiu_em": "1950-01-01"}'

# Criar coleção
curl -X POST "http://localhost:8000/colecoes/" \
     -H "Content-Type: application/json" \
     -d '{
       "titulo": "Dark Side of the Moon",
       "tipo": "Album",
       "duracao": 2580,
       "caminho_capa": "/covers/dsotm.jpg",
       "data_lancamento": "1973-03-01"
     }'
```

## ‍💻 Autores

**Gustavo Aragão** - gustavo.aragao@dcomp.com

# TODO: Adicionar o nome do resto do pessoal e e-mails