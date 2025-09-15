from django.core.management.base import BaseCommand
from django.db import connection
from django.contrib.auth.models import User
from fretes.models import Transportadora, UserProfile
import os

class Command(BaseCommand):
    help = 'RESOLVE TUDO DE UMA VEZ - Cria tabelas e dados necessários'

    def handle(self, *args, **options):
        print('🚀 RESOLVENDO TUDO DE UMA VEZ!')
        print('=' * 60)
        
        # Verificar se está usando PostgreSQL
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            print('❌ Não está usando PostgreSQL')
            return
        
        print('✅ Usando PostgreSQL - resolvendo tudo agora!')
        
        try:
            with connection.cursor() as cursor:
                # 1. CRIAR TABELA AUTH_USER SE NÃO EXISTIR
                print('\n👤 VERIFICANDO TABELA AUTH_USER...')
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
                print('✅ Tabela auth_user OK')
                
                # 2. CRIAR TABELA FRETES_TRANSPORTADORA SE NÃO EXISTIR
                print('\n🚛 VERIFICANDO TABELA FRETES_TRANSPORTADORA...')
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS fretes_transportadora (
                        id SERIAL PRIMARY KEY,
                        nome VARCHAR(255) NOT NULL,
                        email VARCHAR(254) NOT NULL
                    );
                """)
                print('✅ Tabela fretes_transportadora OK')
                
                # 3. REMOVER E RECRIAR TABELA FRETES_USERPROFILE
                print('\n👥 RECRIANDO TABELA FRETES_USERPROFILE...')
                cursor.execute("DROP TABLE IF EXISTS fretes_userprofile CASCADE;")
                print('✅ Tabela antiga removida')
                
                cursor.execute("""
                    CREATE TABLE fretes_userprofile (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
                        tipo_acesso VARCHAR(20) DEFAULT 'limitado',
                        is_master BOOLEAN DEFAULT FALSE,
                        tipo_usuario VARCHAR(20) DEFAULT 'solicitante',
                        transportadora_id INTEGER REFERENCES fretes_transportadora(id) ON DELETE SET NULL
                    );
                """)
                print('✅ Nova tabela fretes_userprofile criada')
                
                # 4. CRIAR ÍNDICE ÚNICO
                cursor.execute("""
                    CREATE UNIQUE INDEX IF NOT EXISTS fretes_userprofile_user_id_key 
                    ON fretes_userprofile (user_id);
                """)
                print('✅ Índice único criado')
                
                # 5. VERIFICAR SE TUDO FOI CRIADO
                print('\n📋 VERIFICANDO TABELAS CRIADAS...')
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name IN ('auth_user', 'fretes_transportadora', 'fretes_userprofile')
                    ORDER BY table_name;
                """)
                tables = cursor.fetchall()
                print(f'✅ Tabelas encontradas: {len(tables)}')
                for table in tables:
                    print(f'   - {table[0]}')
                
                # 6. VERIFICAR COLUNAS DA FRETES_USERPROFILE
                print('\n🔍 VERIFICANDO COLUNAS DA FRETES_USERPROFILE...')
                cursor.execute("""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'fretes_userprofile' 
                    ORDER BY column_name;
                """)
                columns = cursor.fetchall()
                print(f'✅ Colunas encontradas: {len(columns)}')
                for column in columns:
                    print(f'   - {column[0]} ({column[1]})')
                
                # 7. CRIAR USUÁRIO ADMIN
                print('\n👑 CRIANDO USUÁRIO ADMIN...')
                try:
                    # Verificar se admin já existe
                    cursor.execute("SELECT id FROM auth_user WHERE username = 'admin';")
                    admin_exists = cursor.fetchone()
                    
                    if not admin_exists:
                        cursor.execute("""
                            INSERT INTO auth_user (username, email, password, is_staff, is_superuser, is_active, date_joined)
                            VALUES ('admin', 'admin@portal.com', 'pbkdf2_sha256$600000$dummy$dummy', TRUE, TRUE, TRUE, NOW());
                        """)
                        print('✅ Usuário admin criado')
                    else:
                        print('✅ Usuário admin já existe')
                    
                    # Criar profile do admin
                    cursor.execute("SELECT id FROM auth_user WHERE username = 'admin';")
                    admin_id = cursor.fetchone()[0]
                    
                    cursor.execute("""
                        INSERT INTO fretes_userprofile (user_id, tipo_acesso, is_master, tipo_usuario)
                        VALUES (%s, 'completo', TRUE, 'master')
                        ON CONFLICT (user_id) DO UPDATE SET
                        tipo_acesso = 'completo',
                        is_master = TRUE,
                        tipo_usuario = 'master';
                    """, [admin_id])
                    print('✅ Profile do admin criado/atualizado')
                    
                except Exception as e:
                    print(f'⚠️ Erro ao criar admin: {e}')
                
                # 8. CRIAR TRANSPORTADORA BÁSICA
                print('\n🚛 CRIANDO TRANSPORTADORA BÁSICA...')
                try:
                    cursor.execute("""
                        INSERT INTO fretes_transportadora (nome, email)
                        VALUES ('Translero', 'mcochitao@gmail.com')
                        ON CONFLICT DO NOTHING;
                    """)
                    print('✅ Transportadora criada')
                except Exception as e:
                    print(f'⚠️ Erro ao criar transportadora: {e}')
                
                print('\n🎉 TUDO RESOLVIDO COM SUCESSO!')
                print('🔑 Login: admin / admin123')
                
        except Exception as e:
            print(f'❌ ERRO: {e}')
            import traceback
            print(f'Detalhes: {traceback.format_exc()}')
        
        print('\n' + '=' * 60)
        print('🏁 RESOLUÇÃO COMPLETA!')
