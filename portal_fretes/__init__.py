# Auto-criar tabelas se não existirem
import os
import django
from django.conf import settings

# Só executar se não estiver em modo de teste
if not os.environ.get('DJANGO_SETTINGS_MODULE', '').endswith('test'):
    try:
        # Configurar Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal_fretes.settings')
        django.setup()
        
        from django.db import connection
        
        # Verificar se auth_user existe
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'auth_user'
                );
            """)
            auth_user_exists = cursor.fetchone()[0]
            
            if not auth_user_exists:
                print("🚨 EMERGÊNCIA: Tabela auth_user não existe - CRIANDO...")
                
                # Criar tabela auth_user
                cursor.execute("""
                    CREATE TABLE auth_user (
                        id SERIAL PRIMARY KEY,
                        password VARCHAR(128) NOT NULL,
                        last_login TIMESTAMP WITH TIME ZONE,
                        is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
                        username VARCHAR(150) UNIQUE NOT NULL,
                        first_name VARCHAR(150) NOT NULL DEFAULT '',
                        last_name VARCHAR(150) NOT NULL DEFAULT '',
                        email VARCHAR(254) NOT NULL DEFAULT '',
                        is_staff BOOLEAN NOT NULL DEFAULT FALSE,
                        is_active BOOLEAN NOT NULL DEFAULT TRUE,
                        date_joined TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
                    );
                """)
                print("✅ Tabela auth_user criada")
                
                # Criar tabela django_migrations
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS django_migrations (
                        id SERIAL PRIMARY KEY,
                        app VARCHAR(255) NOT NULL,
                        name VARCHAR(255) NOT NULL,
                        applied TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
                    );
                """)
                print("✅ Tabela django_migrations criada")
                
                # Criar tabela django_content_type
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS django_content_type (
                        id SERIAL PRIMARY KEY,
                        app_label VARCHAR(100) NOT NULL,
                        model VARCHAR(100) NOT NULL,
                        UNIQUE(app_label, model)
                    );
                """)
                print("✅ Tabela django_content_type criada")
                
                # Criar tabela auth_permission
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS auth_permission (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        content_type_id INTEGER NOT NULL,
                        codename VARCHAR(100) NOT NULL,
                        UNIQUE(content_type_id, codename)
                    );
                """)
                print("✅ Tabela auth_permission criada")
                
                # Criar tabela auth_group
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS auth_group (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(150) UNIQUE NOT NULL
                    );
                """)
                print("✅ Tabela auth_group criada")
                
                # Criar tabela django_session
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS django_session (
                        session_key VARCHAR(40) PRIMARY KEY,
                        session_data TEXT NOT NULL,
                        expire_date TIMESTAMP WITH TIME ZONE NOT NULL
                    );
                """)
                print("✅ Tabela django_session criada")
                
                # Criar tabela fretes_userprofile
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS fretes_userprofile (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER UNIQUE NOT NULL,
                        tipo_usuario VARCHAR(20) NOT NULL DEFAULT 'solicitador',
                        is_master BOOLEAN NOT NULL DEFAULT FALSE,
                        transportadora_id INTEGER,
                        FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE
                    );
                """)
                print("✅ Tabela fretes_userprofile criada")
                
                # Criar tabela fretes_transportadora
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS fretes_transportadora (
                        id SERIAL PRIMARY KEY,
                        nome VARCHAR(200) NOT NULL,
                        cnpj VARCHAR(18) UNIQUE NOT NULL,
                        telefone VARCHAR(20),
                        email VARCHAR(254),
                        endereco TEXT,
                        ativa BOOLEAN NOT NULL DEFAULT TRUE,
                        data_criacao TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
                    );
                """)
                print("✅ Tabela fretes_transportadora criada")
                
                # Criar tabela fretes_loja
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS fretes_loja (
                        id SERIAL PRIMARY KEY,
                        nome VARCHAR(200) NOT NULL,
                        cep VARCHAR(10),
                        endereco TEXT,
                        cidade VARCHAR(100),
                        estado VARCHAR(2),
                        regional VARCHAR(100),
                        ativa BOOLEAN NOT NULL DEFAULT TRUE
                    );
                """)
                print("✅ Tabela fretes_loja criada")
                
                # Criar tabela fretes_freterequest
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS fretes_freterequest (
                        id SERIAL PRIMARY KEY,
                        solicitador_id INTEGER NOT NULL,
                        origem_id INTEGER NOT NULL,
                        destino_id INTEGER NOT NULL,
                        volume DECIMAL(10,2),
                        tipo_veiculo VARCHAR(50),
                        horario_coleta TIMESTAMP WITH TIME ZONE,
                        data_entrega DATE,
                        observacoes_origem TEXT,
                        observacoes_destino TEXT,
                        status VARCHAR(20) NOT NULL DEFAULT 'pendente',
                        aprovador_id INTEGER,
                        centro_custo VARCHAR(100),
                        data_cotacao TIMESTAMP WITH TIME ZONE,
                        data_aprovacao TIMESTAMP WITH TIME ZONE,
                        data_cancelamento TIMESTAMP WITH TIME ZONE,
                        precisa_ajudante BOOLEAN NOT NULL DEFAULT FALSE,
                        anexo_origem VARCHAR(100),
                        anexo_destino VARCHAR(100),
                        anexo_nota_fiscal VARCHAR(100),
                        data_criacao TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                        FOREIGN KEY (solicitador_id) REFERENCES auth_user(id) ON DELETE CASCADE,
                        FOREIGN KEY (origem_id) REFERENCES fretes_loja(id) ON DELETE CASCADE,
                        FOREIGN KEY (destino_id) REFERENCES fretes_loja(id) ON DELETE CASCADE,
                        FOREIGN KEY (aprovador_id) REFERENCES auth_user(id) ON DELETE SET NULL
                    );
                """)
                print("✅ Tabela fretes_freterequest criada")
                
                # Criar tabela fretes_destino
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS fretes_destino (
                        id SERIAL PRIMARY KEY,
                        frete_id INTEGER NOT NULL,
                        loja_id INTEGER NOT NULL,
                        volume DECIMAL(10,2),
                        numero VARCHAR(20),
                        observacao TEXT,
                        anexo VARCHAR(100),
                        data_entrega DATE,
                        FOREIGN KEY (frete_id) REFERENCES fretes_freterequest(id) ON DELETE CASCADE,
                        FOREIGN KEY (loja_id) REFERENCES fretes_loja(id) ON DELETE CASCADE
                    );
                """)
                print("✅ Tabela fretes_destino criada")
                
                # Criar tabela fretes_cotacaofrete
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS fretes_cotacaofrete (
                        id SERIAL PRIMARY KEY,
                        frete_id INTEGER NOT NULL,
                        transportadora_id INTEGER NOT NULL,
                        valor DECIMAL(10,2) NOT NULL,
                        observacoes TEXT,
                        data_cotacao TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                        FOREIGN KEY (frete_id) REFERENCES fretes_freterequest(id) ON DELETE CASCADE,
                        FOREIGN KEY (transportadora_id) REFERENCES fretes_transportadora(id) ON DELETE CASCADE
                    );
                """)
                print("✅ Tabela fretes_cotacaofrete criada")
                
                print("🎉 SUCESSO! Todas as tabelas foram criadas!")
                
                # Criar usuário cochit0 se não existir
                try:
                    from django.contrib.auth.models import User
                    from fretes.models import UserProfile
                    
                    if not User.objects.filter(username='cochit0').exists():
                        user = User.objects.create_user(
                            username='cochit0',
                            email='mcochitao@gmail.com',
                            password='1357',
                            first_name='Marcos',
                            last_name='Cochitao',
                            is_staff=True,
                            is_superuser=True,
                            is_active=True
                        )
                        
                        UserProfile.objects.create(
                            user=user,
                            tipo_usuario='master',
                            is_master=True,
                            tipo_acesso='completo'
                        )
                        print("✅ Usuário cochit0 criado automaticamente!")
                    else:
                        # Garantir permissões
                        user = User.objects.get(username='cochit0')
                        if not user.is_staff or not user.is_superuser:
                            user.is_staff = True
                            user.is_superuser = True
                            user.is_active = True
                            user.save()
                            print("✅ Permissões do cochit0 atualizadas!")
                        
                except Exception as user_error:
                    print(f"⚠️ Erro ao criar usuário cochit0: {user_error}")
                
    except Exception as e:
        print(f"❌ Erro ao criar tabelas automaticamente: {e}")
        pass  # Não falhar a aplicação se houver erro
