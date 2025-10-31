# News Aggregation Pipeline

Pipeline automatizado de agregação de notícias usando Apache Airflow. Faz scraping de sites de notícias brasileiras, gera emails com IA e envia para destinatários.

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

4. **Acesse o Airflow**
    - URL: http://localhost:8080
    - Usuário: `airflow`
    - Senha: `airflow`

## 📊 Pipeline

O DAG `news_pipeline_dag` executa diariamente às 8h (UTC) e realiza:

1. **Inicializa banco de dados** - Cria tabelas e dados iniciais
2. **Scraping de notícias** - Coleta artigos do IstoÉDinheiro e MoneyTimes
3. **Geração de email** - Usa OpenAI para criar conteúdo do email
4. **Envio de emails** - Envia para destinatários cadastrados no banco

## 📁 Estrutura

```
.
├── dags/                      # DAGs do Airflow
│   ├── news_pipeline_dag.py   # DAG principal
│   ├── utils/                 # Utilitários
│   │   ├── scraper.py         # Scraper de notícias
│   │   ├── llm_utils.py       # Integração OpenAI
│   │   ├── email_utils.py     # Envio de emails
│   │   └── db_utils.py        # Operações de banco
│   └── sql/
│       └── init_db.py         # Inicialização do BD
├── docker-compose.yaml        # Configuração Docker
└── .env                       # Variáveis de ambiente
```

## 🛑 Parar os Serviços

```bash
docker-compose down
```

## 📝 Notas

-   O pipeline coleta até 5 artigos de cada fonte
-   Destinatários são gerenciados no banco de dados PostgreSQL
-   Logs disponíveis no diretório `logs/`
