# Documentação de Patrimônio

> _Nome do projeto a decidir_

## Integrantes

- Gabriel Fernandes
- Anna Liz
- Kauan Ferreira

## Tema Recebido

- Documentação de Patrimônio

## Objetivo

Desenvolver uma API REST que funcione como um **Cofre Digital de Arquivos** para a documentação de bens patrimoniais, garantindo persistência, integridade e segurança dos dados sem o uso de bancos de dados.

## Requisitos

- F01: Upload de arquivos com metadados.
- F02: Listagem de documentos.
- F03: Busca de documento por ID.
- F04: Download do arquivo físico.
- F05: Atualização de metadados.
- F06: Exclusão de documentos.
- F09: Verificação de Integridade (SHA-256).
- F12: Configuração (leitura de variáveis via `config.yaml`).
- F14: Geração de Backup Compactado (`.zip`).
- F17: Tratamento de Exceções.

## Bibliotecas Utilizadas

| Biblioteca | Versão | Finalidade |
|------------|--------|------------|
| `fastapi` | 0.141.1 | Framework web principal para roteamento e construção da API REST. |
| `uvicorn` | 0.52.4 | Servidor ASGI para rodar a aplicação FastAPI de forma assíncrona. |
| `python-multipart` | 0.0.32 | Processamento de formulários (`Form`) e recepção de arquivos físicos (`UploadFile`). |
| `pydantic` | 2.13.5 | Serialização, validação e estruturação dos modelos de dados. |
| `PyYAML` | 6.0.3 | Leitura e mapeamento de configurações dinâmicas a partir do arquivo `config.yaml`. |

## Instruções de Instalação

```bash
# Clone o repositório
git clone <url-do-repositorio>

# Acesse a pasta do projeto
cd <nome-do-projeto>

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows use: venv\Scripts\activate

# Instale as dependências contidas no requirements.txt
pip install -r requirements.txt

# Inicie o servidor
uvicorn main:app --reload
```

Após iniciar, a documentação interativa estará disponível em `http://127.0.0.1:8000/docs`.

## Estrutura do Projeto

```
documentacao-de-patrimonio/
├── config.yaml          # Configurações da aplicação
├── main.py              # Ponto de entrada da API
├── core/                # Configurações e utilitários centrais
├── models/              # Modelos de dados (Pydantic)
├── routes/              # Rotas / endpoints
├── services/            # Regras de negócio
├── storage/             # Persistência (sem banco de dados)
│   ├── arquivos/        # Arquivos binários enviados
│   ├── backups/         # Backups .zip gerados
│   ├── logs/            # Logs da aplicação
│   └── metadata/        # Arquivos .json de metadados
└── requirements.txt
```

## Principais Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/documentos/` | Realiza o upload de um arquivo físico e cadastra seus metadados. |
| `GET` | `/documentos/` | Retorna a lista de todos os documentos cadastrados (com suporte a filtros). |
| `GET` | `/documentos/{id}` | Busca os metadados de um documento específico através do seu ID. |
| `GET` | `/documentos/{id}/download` | Realiza o download do arquivo físico correspondente ao ID. |
| `PUT` | `/documentos/{id}` | Atualiza as informações (metadados) de um documento patrimonial existente. |
| `DELETE` | `/documentos/{id}` | Remove o registro do documento e o seu arquivo físico correspondente. |
| `POST` | `/backup/` | Gera um arquivo compactado (`.zip`) contendo o backup seguro de todo o sistema. |

## Exemplos de Utilização

```bash
# Exemplo 1: Criar um novo registro de patrimônio fazendo o upload de um arquivo (Nota Fiscal ou Foto)
curl -X 'POST' \
  'http://127.0.0.1:8000/documentos/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'arquivo=@/caminho/para/nota_fiscal.pdf' \
  -F 'categoria=Eletrônicos' \
  -F 'descricao=Notebook Dell Latitude para uso do setor de desenvolvimento' \
  -F 'numero_patrimonial=PAT-2026-001' \
  -F 'setor=TI' \
  -F 'situacao=Ativo'

# Exemplo 2: Listar todos os documentos patrimoniais cadastrados
curl -X 'GET' \
  'http://127.0.0.1:8000/documentos/' \
  -H 'accept: application/json'

# Exemplo 3: Gerar um backup de segurança de todo o cofre digital
curl -X 'POST' \
  'http://127.0.0.1:8000/backup/' \
  -H 'accept: application/json' \
  -d ''
```

## Metadados Específicos do Domínio

| Campo | Descrição | Exemplos |
|-------|-----------|----------|
| `numero_patrimonial` | Identificador único (geralmente uma plaqueta, código de barras ou tombamento) fixado fisicamente no bem. | `PAT-2026-001` |
| `setor` | Departamento ou localização física onde o bem está alocado no momento. | TI, Diretoria, Almoxarifado |
| `situacao` | Status de uso e conservação do item. | Ativo, Em Manutenção, Emprestado, Baixado |
| `categoria` | Classificação geral do ativo para fins de inventário. | Mobiliário, Equipamentos de TI, Veículos |
| `descricao` | Descrição textual do bem ou do documento. | Notebook |
| `sha256` | Assinatura digital única do arquivo salvo, essencial para auditoria, comprovando que o documento não foi adulterado desde o upload. | — |

## Descrição da Funcionalidade Específica do Tema
__