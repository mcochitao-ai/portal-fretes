# 🚛 Portal de Fretes

Sistema web desenvolvido em Django para gestão de solicitações de frete entre lojas, com interface moderna e funcionalidades completas.

## 🌐 **Demo**

**Acesse o projeto:** [https://portal-fretes.onrender.com](https://portal-fretes.onrender.com)

## ✨ **Funcionalidades**

- 🔐 **Sistema de Autenticação** - Login e cadastro de usuários
- 📊 **Dashboard Administrativo** - Visão geral do sistema
- 🏪 **Gestão de Lojas** - Cadastro e visualização de lojas
- 📍 **Gestão de Destinos** - Configuração de destinos
- 🚛 **Solicitação de Fretes** - Interface para solicitar transportes
- 📈 **Relatórios Excel** - Exportação de dados
- 📱 **Interface Responsiva** - Funciona em desktop e mobile
- 🚀 **Deploy Automático** - Integração com GitHub

## 🛠️ **Tecnologias Utilizadas**

- **Backend:** Django 5.2.5
- **Frontend:** HTML5, CSS3, Bootstrap
- **Banco de Dados:** SQLite
- **Servidor:** Gunicorn
- **Deploy:** Render
- **Versionamento:** Git/GitHub

## 🚀 **Como Executar Localmente**

### **Pré-requisitos**
- Python 3.11+
- pip

### **Instalação**

1. **Clone o repositório**
```bash
git clone https://github.com/mcochitao-ai/portal-fretes.git
cd portal-fretes
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Execute as migrações**
```bash
python manage.py migrate
```

5. **Crie um superusuário**
```bash
python manage.py createsuperuser
```

6. **Execute o servidor**
```bash
python manage.py runserver
```

7. **Acesse:** http://127.0.0.1:8000

## 📁 **Estrutura do Projeto**

```
portal-fretes/
├── fretes/                 # App principal
│   ├── models.py          # Modelos de dados
│   ├── views.py           # Views e lógica
│   ├── urls.py            # URLs da aplicação
│   ├── templates/         # Templates HTML
│   └── static/            # Arquivos estáticos
├── portal_fretes/         # Configurações do projeto
│   ├── settings.py        # Configurações
│   └── urls.py            # URLs principais
├── requirements.txt       # Dependências
├── render.yaml           # Configuração do Render
└── README.md             # Este arquivo
```

## 🔧 **Configuração de Produção**

O projeto está configurado para deploy no Render com:

- **Deploy automático** via GitHub
- **SSL automático** (HTTPS)
- **Banco SQLite** persistente
- **Static files** otimizados
- **Health check** endpoint

## 📊 **Endpoints Principais**

- `/` - Página inicial
- `/login/` - Login de usuários
- `/signup/` - Cadastro de usuários
- `/dashboard/` - Dashboard administrativo
- `/solicitar-frete/` - Solicitar frete
- `/meus-fretes/` - Visualizar fretes
- `/health/` - Health check

## 🎯 **Funcionalidades Técnicas**

### **Autenticação**
- Sistema de login/logout
- Cadastro de usuários
- Formulários customizados

### **Gestão de Dados**
- CRUD completo para fretes
- Relacionamentos entre modelos
- Validação de dados

### **Interface**
- Design responsivo
- Componentes reutilizáveis
- UX otimizada

### **Deploy**
- Configuração para produção
- Variáveis de ambiente
- Static files otimizados

## 📈 **Métricas do Projeto**

- **Linhas de código:** 500+
- **Funcionalidades:** 8+ features
- **Templates:** 8 páginas
- **Modelos:** 4 entidades
- **Deploy:** Automático

## 🤝 **Contribuição**

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📝 **Licença**

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 **Autor**

**Murilo Cochito**
- GitHub: [@mcochitao-ai](https://github.com/mcochitao-ai)
- LinkedIn: [Seu LinkedIn]

## 🙏 **Agradecimentos**

- Django Community
- Render Platform
- Bootstrap Framework

---

⭐ **Se este projeto te ajudou, deixe uma estrela!**
