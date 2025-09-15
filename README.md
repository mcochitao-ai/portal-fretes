# 🚛 Portal de Fretes

Sistema completo de gestão de fretes com cotação automática e aprovação de transportadoras.

## 🚀 Acesso Rápido

- **🌐 Site em Produção**: [https://portal-fretes.onrender.com](https://portal-fretes.onrender.com)
- **👤 Login**: `admin` / `admin123`

## 📋 Funcionalidades

### 👥 Para Usuários
- ✅ Solicitar fretes com origem e destino
- ✅ Anexar documentos (nota fiscal, anexos)
- ✅ Acompanhar status dos fretes
- ✅ Visualizar histórico de solicitações

### 🚛 Para Transportadoras
- ✅ Receber cotações de fretes
- ✅ Enviar propostas de preço
- ✅ Gerenciar usuários da transportadora
- ✅ Visualizar histórico de cotações

### 👨‍💼 Para Gerentes
- ✅ Aprovar/rejeitar fretes
- ✅ Gerenciar transportadoras
- ✅ Gerenciar usuários do sistema
- ✅ Visualizar relatórios e métricas

## 🛠️ Tecnologias

- **Backend**: Django 5.2.5
- **Frontend**: HTML, CSS, Bootstrap
- **Banco Local**: SQLite
- **Banco Produção**: PostgreSQL
- **Deploy**: Render.com
- **Email**: SMTP Gmail

## 📁 Estrutura do Projeto

```
Portal de Fretes/
├── 📁 docs/                    # Documentação
├── 📁 data/                    # Dados e planilhas
├── 📁 scripts/                 # Scripts utilitários
├── 📁 fretes/                  # App principal Django
│   ├── 📁 templates/           # Templates HTML
│   ├── 📁 static/              # CSS e JS
│   ├── 📁 management/          # Comandos Django
│   └── 📁 migrations/          # Migrações do banco
├── 📁 portal_fretes/           # Configurações Django
├── 📁 media/                   # Uploads de usuários
├── 📄 manage.py                # Comando Django
├── 📄 requirements.txt         # Dependências Python
├── 📄 render.yaml              # Configuração Render
└── 📄 README.md                # Este arquivo
```

## 🚀 Como Executar Localmente

1. **Clone o repositório**
   ```bash
   git clone https://github.com/mcochitao-ai/portal-fretes.git
   cd portal-fretes
   ```

2. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute as migrações**
   ```bash
   python manage.py migrate
   ```

4. **Crie um superusuário**
   ```bash
   python manage.py createsuperuser
   ```

5. **Execute o servidor**
   ```bash
   python manage.py runserver
   ```

6. **Acesse**: http://127.0.0.1:8000

## 📊 Status do Deploy

Para verificar o status do deploy em produção:
```bash
python scripts/check_deploy_status.py
```

## 📚 Documentação

- [📖 Documentação Completa](docs/README.md)
- [🔧 Configuração de Deploy](docs/DEPLOY_STATUS.md)
- [📧 Configuração de Email](docs/EMAIL_CONFIG.md)
- [🗄️ Setup do Banco](docs/DATABASE_SETUP.md)
- [🎯 Apresentação LinkedIn](docs/LINKEDIN_PRESENTATION.md)

## 👨‍💻 Desenvolvedor

**Marcos Cochitao** - [GitHub](https://github.com/mcochitao-ai)

---

*Sistema desenvolvido para otimizar o processo de cotação e gestão de fretes empresariais.*
