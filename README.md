# Documentação de Patrimônio

> _Nome do projeto a decidir_

## Integrantes

- Gabriel Fernandes
- Anna Liz
- Kauan Ferreira

## Tema Recebido

- Documentação de Patrimônio

## Objetivo

__

## Requisitos

- F01: Upload de arquivos com metadados.
- F02: Listagem de documentos.
- F03: Busca de documento por ID.
- F04: Download do arquivo físico.
- F05: Atualização de metadados.
- F06: Exclusão de documentos.
- F09: Verificação de Integridade (SHA-256).
- F12: Configuração (Leitura de variáveis via config.yaml).
- F14: Geração de Backup Compactado (.zip).
- F17: Tratamento de Exceções.

## Bibliotecas Utilizadas

| Biblioteca | Versão | Finalidade |
|------------|--------|------------|
| `fastapi` | 0.141.1 | Framework web principal para roteamento e construção da API REST. |
| `uvicorn` | 0.52.4 | Servidor ASGI para rodar a aplicação FastAPI de forma assíncrona. |
| `python-multipart` | 0.0.32 | Processamento de formulários (`Form`) e recepção de arquivos físicos (`UploadFile`). |
| `pydantic` | 2.13.5 | Serialização, validação e estruturação dos modelos de dados. |
| `PyYAML` | 6.0.3 | Leitura e mapeamento de configurações dinâmicas a partir do arquivo. |

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

## Estrutura do Projeto

```
documentacao-de-patrimonio/
├── config.yaml          
├── main.py              
├── core/                
├── models/              
├── routes/              
├── services/            
├── storage/             
│   ├── arquivos/        
│   ├── backups/         
│   ├── logs/            
│   └── metadata/        
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

## Exemplos de Utilização

```bash
# Exemplo 1: Criar um novo registro de patrimônio fazendo o upload de um arquivo (Nota Fiscal ou Foto)
curl -X 'POST' \
  '[http://127.0.0.1:8000/documentos/](http://127.0.0.1:8000/documentos/)' \
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
  '[http://127.0.0.1:8000/documentos](http://127.0.0.1:8000/documentos)' \
  -H 'accept: application/json'

# Exemplo 3: Gerar um backup de segurança de todo o cofre digital
curl -X 'POST' \
  '[http://127.0.0.1:8000/backup/](http://127.0.0.1:8000/backup/)' \
  -H 'accept: application/json' \
  -d ''

## Metadados Específicos do Domínio

| Campo | Descrição | Exemplos |
|-------|-----------|----------|
| `numero_patrimonial` | Identificador único (geralmente uma plaqueta, código de barras ou tombamento) fixado fisicamente no bem. | — |
| `setor` | Departamento ou localização física onde o bem está alocado no momento. | TI, Diretoria, Almoxarifado |
| `situacao` | Status de uso e conservação do item. | Ativo, Em Manutenção, Emprestado, Baixado |
| `categoria` | Classificação geral do ativo para fins de inventário. | Mobiliário, Equipamentos de TI, Veículos |
| `sha256` | Assinatura digital única do arquivo salvo, essencial para fins de auditoria, comprovando que o documento (como uma nota fiscal ou termo de garantia) não foi adulterado desde o upload. | — |

## Descrição da Funcionalidade Específica do Tema

_funcionalidade central relacionada ao tema recebido._
