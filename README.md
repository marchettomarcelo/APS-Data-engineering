# News Aggregation Pipeline

Pipeline automatizado de agregação de notícias usando Apache Airflow. Faz scraping de sites de notícias brasileiras, gera emails com IA e envia para destinatários.

## 🛠️ Stack Tecnológica

-   **Backend**: FastAPI + PostgreSQL
-   **Frontend**: React + TypeScript + Vite + Shadcn UI
-   **Orquestração**: Apache Airflow (CeleryExecutor + Redis)
-   **IA**: OpenAI GPT para geração de conteúdo
-   **Email**: Resend para envio de emails
-   **Scraping**: BeautifulSoup + Requests

## 📋 Requisitos

-   Docker e Docker Compose
-   Chaves de API:
    -   OpenAI (para geração de conteúdo)
    -   Resend (para envio de emails)

## 🚀 Configuração Rápida

1. **Clone o repositório e entre no diretório**

2. **Configure as variáveis de ambiente**

    ```bash
    cp env.example .env
    ```

    Edite o arquivo `.env` e adicione suas chaves de API:

    ```
    OPENAI_API_KEY=sua-chave-openai
    RESEND_API_KEY=sua-chave-resend
    ```

3. **Inicie os serviços**

    ```bash
    docker-compose up -d
    ```

4. **Acesse as interfaces**
    - **Airflow UI**: http://localhost:8080 (usuário: `airflow`, senha: `airflow`)
    - **Frontend**: http://localhost:5173 (visualização de destinatários)
    - **API**: http://localhost:8000 (FastAPI docs em `/docs`)

## 📊 Pipeline

O DAG `news_pipeline_dag` executa diariamente às 8h (UTC) e realiza:

1. **Inicializa banco de dados** - Cria tabelas e dados iniciais
2. **Scraping de notícias** - Coleta artigos do IstoÉDinheiro e MoneyTimes (até 5 de cada fonte)
3. **Geração de email** - Usa OpenAI para criar conteúdo do email
4. **Envio de emails** - Envia para destinatários cadastrados no banco

### Executar Manualmente

Para testar o pipeline imediatamente:

1. Acesse o Airflow UI em http://localhost:8080
2. Localize o DAG `news_pipeline_dag`
3. Clique no botão de "play" (▶️) para executar manualmente
4. Acompanhe o progresso na interface do Airflow

## 📁 Estrutura

```
.
├── apps/
│   ├── airflow/               # Apache Airflow
│   │   ├── dags/              # DAGs
│   │   │   ├── news_pipeline_dag.py
│   │   │   └── utils/         # Utilitários (scraper, LLM, email, DB)
│   │   └── sql/               # Scripts SQL
│   ├── api/                   # FastAPI Backend
│   │   └── app/               # Código da API
│   └── frontend/              # React + Vite Frontend
│       └── src/               # Código React
├── docker-compose.yaml        # Configuração Docker
└── .env                       # Variáveis de ambiente
```

## 🛑 Parar os Serviços

```bash
docker-compose down
```

## 🎨 Interface Web

O frontend React possui 3 páginas principais:

### Recipients (Destinatários)
- Visualizar lista completa de destinatários
- Adicionar novos destinatários via modal
- Remover destinatários
- Atualizar lista em tempo real

### Articles (Artigos)
- Visualizar todos os artigos coletados pelo scraper
- Ver título e URL de cada artigo
- Links clicáveis para acessar as notícias originais

### Email Content (Conteúdo de Email)
- Histórico completo de emails gerados
- Preview do conteúdo HTML de cada email
- Ordenação por data (mais recente primeiro)
- Modal para visualização detalhada do email

## 🔌 API Endpoints

Documentação interativa disponível em: http://localhost:8000/docs

### Recipients (Destinatários)
- `GET /recipients` - Lista todos os destinatários
- `GET /recipients/{recipient_id}` - Busca destinatário por ID
- `POST /recipients` - Adiciona novo destinatário
- `PUT /recipients/{recipient_id}` - Atualiza destinatário
- `DELETE /recipients/by-email/{email}` - Remove destinatário por email

### Articles (Artigos)
- `GET /articles` - Lista todos os artigos
- `GET /articles/{article_id}` - Busca artigo por ID
- `GET /articles/by-url/{url}` - Busca artigo por URL
- `POST /articles` - Adiciona novo artigo
- `PUT /articles/{article_id}` - Atualiza artigo
- `DELETE /articles/{article_id}` - Remove artigo

### Email Content (Conteúdo de Email)
- `GET /email-content` - Lista todos os emails gerados
- `GET /email-content/latest` - Retorna o email mais recente
- `GET /email-content/{email_content_id}` - Busca email por ID
- `POST /email-content` - Adiciona novo email
- `PUT /email-content/{email_content_id}` - Atualiza email
- `DELETE /email-content/{email_content_id}` - Remove email

## 📝 Notas

-   O pipeline coleta até 5 artigos de cada fonte
-   Destinatários são gerenciados no banco de dados PostgreSQL
-   Logs disponíveis no diretório `logs/`
-   Frontend usa Shadcn UI para componentes modernos

# Vídeo de demonstração


[Vídeo de demonstração](https://youtu.be/78Cj1DWUDUA)
