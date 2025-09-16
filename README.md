# 🚚 Portal de Fretes

Sistema completo para gestão de solicitações de frete, cotações e aprovações entre empresas e transportadoras.

## 🚀 Funcionalidades

### 👥 **Gestão de Usuários**
- Sistema de login/cadastro com reset de senha
- Perfis diferenciados: Master, Gerente, Solicitante, Transportadora
- Controle de permissões granular

### 📦 **Gestão de Fretes**
- Solicitação de fretes com múltiplos destinos
- Upload de anexos (notas fiscais, documentos)
- Controle de ajudantes e tipo de veículo
- Status completo do ciclo de vida do frete

### 💰 **Sistema de Cotações**
- Envio para múltiplas transportadoras
- Comparação de propostas
- Aprovação/rejeição com justificativas
- Histórico completo de cotações

### 📊 **Relatórios e Exportação**
- Relatórios em Excel
- Filtros por status, data, usuário
- Histórico de aprovações

## 🛠️ **Tecnologias**

- **Backend:** Django 5.2.5
- **Banco de Dados:** PostgreSQL (produção) / SQLite (desenvolvimento)
- **Frontend:** HTML5, CSS3, Bootstrap
- **Deploy:** Render.com
- **Cache:** Django Cache Framework

## 📋 **Pré-requisitos**

- Python 3.11+
- pip
- Git

## 🚀 **Instalação e Configuração**

### 1. **Clone o repositório**
```bash
git clone <url-do-repositorio>
cd portal-fretes
```

### 2. **Crie um ambiente virtual**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

### 4. **Configure as variáveis de ambiente**
```bash
# Copie o arquivo de exemplo
copy env_example.txt .env
# Edite o .env com suas configurações
```

### 5. **Execute as migrações**
```bash
python manage.py migrate
```

### 6. **Crie um usuário administrador**
```bash
python manage.py createsuperuser
```

### 7. **Execute o servidor**
```bash
python manage.py runserver
```

## 🌐 **Acesso**

- **Desenvolvimento:** http://localhost:8000
- **Produção:** https://portal-fretes.onrender.com

## 👤 **Usuários Padrão (Desenvolvimento)**

Após executar `python manage.py init_deploy`:
- **Admin:** admin / admin123
- **Tipo:** Master (acesso total)

## 📁 **Estrutura do Projeto**

```
portal-fretes/
├── fretes/                    # App principal
│   ├── management/commands/   # Comandos Django
│   ├── migrations/           # Migrações do banco
│   ├── static/              # Arquivos estáticos
│   ├── templates/           # Templates HTML
│   ├── models.py           # Modelos de dados
│   ├── views.py            # Views da aplicação
│   └── urls.py             # URLs da aplicação
├── portal_fretes/          # Configurações do projeto
├── media/                  # Arquivos de upload
├── staticfiles/           # Arquivos estáticos coletados
├── docs/                  # Documentação
├── scripts/               # Scripts auxiliares
├── requirements.txt       # Dependências Python
├── render.yaml           # Configuração do Render
└── gunicorn.conf.py      # Configuração do Gunicorn
```

## 🔧 **Comandos Úteis**

### **Desenvolvimento**
```bash
# Executar migrações
python manage.py migrate

# Criar migrações
python manage.py makemigrations

# Coletar arquivos estáticos
python manage.py collectstatic

# Executar testes
python manage.py test
```

### **Produção**
```bash
# Setup inicial de produção
python manage.py init_deploy

# Importar lojas do Excel
python manage.py importar_lojas_automatico

# Listar usuários
python manage.py listar_usuarios
```

## 📊 **Performance e Otimizações**

### **Implementadas:**
- ✅ Consultas otimizadas com `select_related` e `prefetch_related`
- ✅ Sistema de cache para dados estáticos
- ✅ Índices de banco de dados para consultas rápidas
- ✅ Compressão de arquivos estáticos
- ✅ Configuração otimizada do Gunicorn

### **Capacidade Estimada:**
- **Plano Gratuito:** 10-20 usuários simultâneos
- **Plano Starter ($7/mês):** 20-50 usuários simultâneos
- **Plano Standard ($25/mês):** 50-100 usuários simultâneos

## 🚀 **Deploy no Render**

### **Configuração Automática:**
1. Conecte o repositório GitHub ao Render
2. O `render.yaml` configura automaticamente:
   - Serviço web Django
   - Banco PostgreSQL
   - Variáveis de ambiente
   - Build e deploy automático

### **Variáveis de Ambiente (Opcionais):**
```bash
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-de-app
DEFAULT_FROM_EMAIL=seu-email@gmail.com
```

## 📚 **Documentação**

- [Configuração de Email](docs/EMAIL_CONFIG.md)
- [Setup do Banco de Dados](docs/DATABASE_SETUP.md)
- [Status do Deploy](docs/DEPLOY_STATUS.md)
- [Correções Implementadas](docs/CORRECOES_RENDER.md)

## 🤝 **Contribuição**

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 **Licença**

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 **Suporte**

Para suporte, entre em contato através dos issues do GitHub ou email.

---

**Desenvolvido com ❤️ para otimizar a gestão de fretes empresariais**