import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal_fretes.settings')

application = get_wsgi_application()

# Auto-criar tabelas se não existirem
try:
    from django.db import connection
    from django.contrib.auth.models import User
    
    # Verificar se auth_user existe
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'auth_user'
            );
        """)
        table_exists = cursor.fetchone()[0]
        
        if not table_exists:
            print("🔧 CRIANDO TABELAS AUTOMATICAMENTE...")
            
            # Criar auth_user
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS auth_user (
                    id SERIAL PRIMARY KEY,
                    password VARCHAR(128) NOT NULL,
                    last_login TIMESTAMP WITH TIME ZONE,
                    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
                    username VARCHAR(150) NOT NULL UNIQUE,
                    first_name VARCHAR(150) NOT NULL DEFAULT '',
                    last_name VARCHAR(150) NOT NULL DEFAULT '',
                    email VARCHAR(254) NOT NULL DEFAULT '',
                    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
                    is_active BOOLEAN NOT NULL DEFAULT TRUE,
                    date_joined TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
                );
            """)
            
            # Criar django_session
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS django_session (
                    session_key VARCHAR(40) NOT NULL PRIMARY KEY,
                    session_data TEXT NOT NULL,
                    expire_date TIMESTAMP WITH TIME ZONE NOT NULL
                );
            """)
            
            # Criar outras tabelas essenciais
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS fretes_transportadora (
                    id SERIAL PRIMARY KEY,
                    nome VARCHAR(255) NOT NULL,
                    email VARCHAR(254) NOT NULL
                );
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS fretes_userprofile (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
                    tipo_usuario VARCHAR(50) NOT NULL DEFAULT 'solicitador',
                    transportadora_id INTEGER REFERENCES fretes_transportadora(id) ON DELETE SET NULL
                );
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS fretes_loja (
                    id SERIAL PRIMARY KEY,
                    nome VARCHAR(255) NOT NULL,
                    endereco TEXT NOT NULL,
                    cep VARCHAR(10) NOT NULL,
                    regional VARCHAR(100) NOT NULL
                );
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS fretes_freterequest (
                    id SERIAL PRIMARY KEY,
                    solicitador_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
                    origem_id INTEGER NOT NULL REFERENCES fretes_loja(id) ON DELETE CASCADE,
                    data_solicitacao TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                    status VARCHAR(50) NOT NULL DEFAULT 'pendente',
                    observacoes TEXT DEFAULT '',
                    anexo_origem VARCHAR(100) DEFAULT '',
                    anexo_nota_fiscal VARCHAR(100) DEFAULT '',
                    tipo_veiculo VARCHAR(50) DEFAULT '',
                    precisa_ajudante BOOLEAN DEFAULT FALSE,
                    horario_coleta TIMESTAMP WITH TIME ZONE,
                    data_cotacao TIMESTAMP WITH TIME ZONE,
                    data_aprovacao TIMESTAMP WITH TIME ZONE,
                    data_cancelamento TIMESTAMP WITH TIME ZONE,
                    aprovador_id INTEGER REFERENCES auth_user(id) ON DELETE SET NULL,
                    centro_custo VARCHAR(100) DEFAULT '',
                    observacoes_origem TEXT DEFAULT ''
                );
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS fretes_destino (
                    id SERIAL PRIMARY KEY,
                    frete_id INTEGER NOT NULL REFERENCES fretes_freterequest(id) ON DELETE CASCADE,
                    loja_id INTEGER NOT NULL REFERENCES fretes_loja(id) ON DELETE CASCADE,
                    endereco TEXT NOT NULL,
                    numero VARCHAR(20) DEFAULT '',
                    cep VARCHAR(10) NOT NULL,
                    observacao TEXT DEFAULT '',
                    anexo VARCHAR(100) DEFAULT '',
                    data_entrega TIMESTAMP WITH TIME ZONE,
                    volume VARCHAR(100) DEFAULT ''
                );
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS fretes_cotacaofrete (
                    id SERIAL PRIMARY KEY,
                    frete_id INTEGER NOT NULL REFERENCES fretes_freterequest(id) ON DELETE CASCADE,
                    transportadora_id INTEGER NOT NULL REFERENCES fretes_transportadora(id) ON DELETE CASCADE,
                    valor DECIMAL(10,2) NOT NULL,
                    observacoes TEXT DEFAULT '',
                    data_cotacao TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                    status VARCHAR(50) NOT NULL DEFAULT 'pendente'
                );
            """)
            
            print("✅ TABELAS CRIADAS COM SUCESSO!")
            
            # Criar usuário admin se não existir
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser(
                    username='admin',
                    email='admin@portal.com',
                    password='admin123'
                )
                print("✅ USUÁRIO ADMIN CRIADO: admin / admin123")
            
            # Criar usuário cochit0 se não existir
            if not User.objects.filter(username='cochit0').exists():
                User.objects.create_superuser(
                    username='cochit0',
                    email='cochit0@portal.com',
                    password='123456'
                )
                print("✅ USUÁRIO COCHIT0 CRIADO: cochit0 / 123456")
                
except Exception as e:
    print(f"❌ ERRO NA CRIAÇÃO AUTOMÁTICA: {e}")
