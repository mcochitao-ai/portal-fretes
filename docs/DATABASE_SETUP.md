# Configuração do Banco de Dados - Portal de Fretes

## Problema Identificado
O Render estava usando SQLite local que é perdido a cada deploy. Agora foi configurado PostgreSQL persistente.

## Configuração Aplicada

### 1. Dependências Atualizadas
- Adicionado `psycopg2-binary==2.9.9` ao `requirements.txt`

### 2. Banco de Dados PostgreSQL
- Configurado PostgreSQL no `render.yaml`
- Banco persistente que mantém dados entre deploys

### 3. Comando de Setup Automático
- Criado comando `setup_producao.py` que:
  - Cria usuário admin padrão
  - Cria transportadoras básicas
  - Verifica configuração inicial

## Como Aplicar no Render

### Opção 1: Deploy Automático (Recomendado)
1. Faça commit e push das alterações
2. O Render detectará as mudanças no `render.yaml`
3. Criará automaticamente o banco PostgreSQL
4. Executará as migrações e setup inicial

### Opção 2: Configuração Manual
1. Acesse o dashboard do Render
2. Vá em "New" > "PostgreSQL"
3. Configure:
   - Name: `portal-fretes-db`
   - Plan: Free
4. Vá no serviço web e adicione a variável:
   - Key: `DATABASE_URL`
   - Value: (copie da conexão do PostgreSQL)

## Dados Iniciais
Após o deploy, você terá:
- **Usuário Admin:**
  - Username: `admin`
  - Password: `admin123`
  - Tipo: Master (acesso total)

- **Transportadoras:**
  - Transportadora ABC
  - Logística XYZ
  - Frete Express

## Importar Lojas
Para importar as lojas do Excel:
1. Acesse o admin: `/admin/`
2. Vá em "Lojas" > "Importar"
3. Ou execute: `python manage.py import_lojas`

## Verificação
Após o deploy, verifique:
1. Login com admin/admin123
2. Dados persistem após novo deploy
3. Banco PostgreSQL ativo no dashboard
