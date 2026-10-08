# Documentação de Patrimônio

- Cofre de Bens Patrimoniais

## Integrantes

- Gabriel Fernandes
- Anna Liz
- Kauan Ferreira

## Tema Recebido

- Documentação de Patrimônio

## Objetivo

Desenvolver uma API REST que funcione como um **Cofre Digital de Arquivos** para a documentação de bens patrimoniais, garantindo persistência, integridade e segurança dos dados sem o uso de bancos de dados.

## Requisitos

- FT01: Upload de arquivos com metadados.
- FT02: Listagem de documentos.
- FT03: Busca de documento por ID.
- FT04: Download do arquivo fisico.
- FT05: Atualização de metadados.
- FT06: Exclusão de documentos.
- FT07: Filtros.
- FT08: Estatisticas do Cofre
- FT09: Verificação de Integridade (SHA-256).
- FT11: Sistema de Loggings.
- FT12: Configuração (leitura de variáveis via `archive_config.yaml`).
- FT13: Exportação de documento para CSV.
- FT14: Geração de Backup Compactado.
- FT16: Funcionalidade especifica do tema(listar com filtro de numero patrimonial).
- FT17: Tratamento de Exceções.

## Bibliotecas Utilizadas

| Biblioteca | Versão | Finalidade |
|------------|--------|------------|
| `fastapi` | 0.141.1 | Framework web principal para roteamento e construção da API REST. |
| `uvicorn` | 0.52.4 | Servidor ASGI para rodar a aplicação FastAPI de forma assíncrona. |
| `python-multipart` | 0.0.32 | Processamento de formulários (`Form`) e recepção de arquivos físicos (`UploadFile`). |
| `pydantic` | 2.13.5 | Serialização, validação e estruturação dos modelos de dados. |
| `PyYAML` | 6.0.3 | Leitura e mapeamento de configurações a partir do arquivo `archive_config.yaml`. |

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
├── archive_config.yaml          
├── logging.yaml
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
| `POST` | `/documentos/` | Realiza o upload de um arquivo físico e cadastra seus metadados (categoria, descrição, número patrimonial, setor, situação, equipamento/bem e responsável). Limite de tamanho configurável (padrão 10 MB). |
| `GET` | `/documentos` | Retorna a lista de documentos cadastrados, com filtros opcionais: `extensao`, `numero_patrimonial`, `setor`, `categoria` e `situacao`. |
| `GET` | `/documentos/estatisticas` | Retorna estatísticas gerais: total de documentos, tamanho total em bytes e contagem por extensão, categoria, setor e situação. |
| `GET` | `/documentos/{id}` | Busca os metadados de um documento específico através do seu ID. |
| `GET` | `/documentos/{id}/download` | Realiza o download do arquivo físico correspondente ao ID. |
| `GET` | `/documentos/{id}/integridade` | Recalcula o SHA-256 do arquivo físico e compara com o hash registrado, informando se o arquivo está íntegro. |
| `PUT` | `/documentos/{id}` | Atualiza os metadados de um documento patrimonial existente. |
| `DELETE` | `/documentos/{id}` | Remove o registro do documento. |
| `GET` | `/exportar/csv` | Gera e baixa um arquivo `documentos.csv` com todos os documentos cadastrados. Retorna 404 se não houver nenhum registro. |
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
| `equipamento_bem` | Nome ou tipo do equipamento/bem patrimonial ao qual o documento se refere. | Notebook Dell Latitude, Projetor, Cadeira de escritório |
| `responsavel` | Pessoa responsável pela guarda e uso do bem. | Maria Silva, João Pereira |
| `setor` | Departamento ou localização física onde o bem está alocado no momento. | TI, Diretoria, Almoxarifado |
| `situacao` | Status de uso e conservação do item. | Ativo, Em Manutenção, Emprestado, Baixado |
| `categoria` | Classificação geral do ativo para fins de inventário. | Mobiliário, Equipamentos de TI, Veículos |
| `descricao` | Descrição textual do documento ou observações sobre o bem. | Nota fiscal de compra, Termo de garantia |
| `sha256` | Assinatura digital única do arquivo salvo, essencial para auditoria, comprovando que o documento não foi adulterado desde o upload. | — |

## Descrição da Funcionalidade Específica do Tema

- Filtragem na listagem do documento com número patrimonial.