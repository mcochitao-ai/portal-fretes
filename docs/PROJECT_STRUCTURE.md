# 📁 Estrutura do Projeto - Portal de Fretes

## 🏗️ **Arquitetura Geral**

```
portal-fretes/
├── 📁 fretes/                    # App principal Django
├── 📁 portal_fretes/            # Configurações do projeto
├── 📁 media/                    # Arquivos de upload
├── 📁 staticfiles/              # Arquivos estáticos coletados
├── 📁 docs/                     # Documentação
├── 📁 scripts/                  # Scripts auxiliares
├── 📄 requirements.txt          # Dependências Python
├── 📄 render.yaml              # Configuração do Render
├── 📄 gunicorn.conf.py         # Configuração do Gunicorn
└── 📄 README.md                # Documentação principal
```

## 📱 **App Principal (fretes/)**

### **Modelos (models.py)**
- `Loja` - Lojas/centros de distribuição
- `Transportadora` - Empresas de transporte
- `FreteRequest` - Solicitações de frete
- `CotacaoFrete` - Cotações das transportadoras
- `Destino` - Destinos dos fretes
- `UserProfile` - Perfis de usuário com permissões

### **Views (views.py)**
- **Autenticação:** login, signup, reset password
- **Fretes:** criar, editar, visualizar, aprovar
- **Cotações:** enviar, receber, aprovar
- **Usuários:** gerenciar, criar, editar
- **Relatórios:** exportar Excel

### **Templates (templates/fretes/)**
- `base.html` - Template base
- `login.html`, `signup.html` - Autenticação
- `home.html` - Dashboard principal
- `meus_fretes.html` - Lista de fretes
- `frete_detalhe.html` - Detalhes do frete
- `solicitar_frete.html` - Fluxo de criação
- `gerenciar_*.html` - Páginas administrativas

### **Comandos Management (management/commands/)**
- `init_deploy.py` - Setup inicial de produção
- `importar_lojas_automatico.py` - Importar lojas do Excel
- `listar_usuarios.py` - Listar usuários do sistema
- `deploy_fix.py` - Correções de deploy
- `setup_completo.py` - Setup completo do sistema

## ⚙️ **Configurações (portal_fretes/)**

### **settings.py**
- Configurações Django
- Banco de dados (PostgreSQL/SQLite)
- Cache e sessões
- Configurações de segurança
- Configurações de email

### **urls.py**
- URLs principais do projeto
- Inclui URLs da app fretes

## 📊 **Banco de Dados**

### **Desenvolvimento**
- SQLite (`db.sqlite3`)
- Migrações em `fretes/migrations/`

### **Produção**
- PostgreSQL no Render
- Índices otimizados para performance

## 🎨 **Arquivos Estáticos**

### **CSS (fretes/static/css/)**
- `style.css` - Estilos principais
- `cotacao.css` - Estilos específicos para cotações

### **Uploads (media/)**
- `anexos/origem/` - Anexos da origem
- `anexos/destino/` - Anexos do destino
- `anexos/nota_fiscal/` - Notas fiscais

## 🚀 **Deploy e Produção**

### **Render.com**
- `render.yaml` - Configuração automática
- `gunicorn.conf.py` - Configuração do servidor
- `Procfile` - Comando de inicialização

### **Variáveis de Ambiente**
- `SECRET_KEY` - Chave secreta Django
- `DEBUG` - Modo debug
- `DATABASE_URL` - URL do banco PostgreSQL
- `EMAIL_*` - Configurações de email

## 📚 **Documentação (docs/)**

- `README.md` - Documentação principal
- `PROJECT_STRUCTURE.md` - Este arquivo
- `DEPLOY_STATUS.md` - Status do deploy
- `DATABASE_SETUP.md` - Setup do banco
- `EMAIL_CONFIG.md` - Configuração de email
- `CORRECOES_RENDER.md` - Correções implementadas

## 🔧 **Scripts Auxiliares (scripts/)**

- `import_lojas.py` - Importar lojas do Excel
- `check_deploy_status.py` - Verificar status do deploy

## 📋 **Arquivos de Configuração**

### **Desenvolvimento**
- `.env` - Variáveis de ambiente (não versionado)
- `env_example.txt` - Exemplo de configuração

### **Produção**
- `requirements.txt` - Dependências Python
- `render.yaml` - Configuração do Render
- `gunicorn.conf.py` - Configuração do Gunicorn

## 🎯 **Fluxo de Desenvolvimento**

1. **Desenvolvimento Local**
   - Usar SQLite
   - DEBUG=True
   - Configurações em `.env`

2. **Teste**
   - Executar migrações
   - Testar funcionalidades
   - Verificar logs

3. **Deploy**
   - Push para GitHub
   - Render detecta mudanças
   - Deploy automático

4. **Produção**
   - PostgreSQL
   - DEBUG=False
   - Configurações seguras

## 🔍 **Monitoramento**

### **Logs**
- Render Dashboard
- Django logs
- Gunicorn logs

### **Performance**
- Cache implementado
- Consultas otimizadas
- Índices de banco

## 🛡️ **Segurança**

- HTTPS em produção
- Cookies seguros
- Validação de dados
- Controle de permissões
- CSRF protection
