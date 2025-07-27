# API BedRock - Documentação

## 📋 Índice

- [API BedRock - Documentação](#api-bedrock---documentação)
  - [📋 Índice](#-índice)
  - [🌟 Visão Geral](#-visão-geral)
  - [🛠️ Pré-requisitos](#️-pré-requisitos)
  - [🔧 Instalação](#-instalação)
  - [Subir Banco de dados](#subir-banco-de-dados)
  - [Subindo Backend](#subindo-backend)
  - [iniciando migração do Banco de dados](#iniciando-migração-do-banco-de-dados)
    - [🚀 Execução](#-execução)
    - [Documentação](#documentação)

## 🌟 Visão Geral

API completa para gerenciamento de universos fictícios com sistema de anotações categorizadas. Documentação Swagger/OpenAPI integrada.

## 🛠️ Pré-requisitos

- Python 3.8+
- PostgreSQL 12+
- docker / docker-compose

## 🔧 Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/api-bedrock.git
cd api-bedrock
```

## Subir Banco de dados

```bash
# subir docker-composer
docker composer up
```

## Subindo Backend

```bash
# setup de ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

## iniciando migração do Banco de dados

```bash
flask db init
flask db migrate
flask db upgrade
```

### 🚀 Execução

```bash
# Modo desenvolvimento
flask run --debug
```

### Documentação

```text
# acesse
http://localhost:5000/api/docs/
```
