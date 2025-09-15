from django.core.management.base import BaseCommand
from django.db import connection
import os

class Command(BaseCommand):
    help = 'Verifica se a estrutura do PostgreSQL está igual ao SQLite'

    def handle(self, *args, **options):
        print('🔍 VERIFICANDO ESTRUTURA DO POSTGRESQL')
        print('=' * 60)
        
        # Verificar se está usando PostgreSQL
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            print('❌ Não está usando PostgreSQL')
            return
        
        print('✅ Usando PostgreSQL - verificando estrutura')
        
        try:
            with connection.cursor() as cursor:
                # 1. LISTAR TODAS AS TABELAS
                print('\n📋 TABELAS EXISTENTES:')
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    ORDER BY table_name;
                """)
                tables = cursor.fetchall()
                print(f'   Total de tabelas: {len(tables)}')
                for table in tables:
                    print(f'   ✅ {table[0]}')
                
                # 2. VERIFICAR ESTRUTURA DA TABELA AUTH_USER
                print('\n👤 ESTRUTURA DA TABELA AUTH_USER:')
                cursor.execute("""
                    SELECT column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns 
                    WHERE table_name = 'auth_user' 
                    ORDER BY ordinal_position;
                """)
                columns = cursor.fetchall()
                print(f'   Total de colunas: {len(columns)}')
                for column in columns:
                    print(f'   - {column[0]} ({column[1]}) - Null: {column[2]} - Default: {column[3]}')
                
                # 3. VERIFICAR ESTRUTURA DA TABELA FRETES_LOJA
                print('\n🏪 ESTRUTURA DA TABELA FRETES_LOJA:')
                cursor.execute("""
                    SELECT column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns 
                    WHERE table_name = 'fretes_loja' 
                    ORDER BY ordinal_position;
                """)
                columns = cursor.fetchall()
                print(f'   Total de colunas: {len(columns)}')
                for column in columns:
                    print(f'   - {column[0]} ({column[1]}) - Null: {column[2]} - Default: {column[3]}')
                
                # 4. VERIFICAR ESTRUTURA DA TABELA FRETES_FRETEREQUEST
                print('\n📦 ESTRUTURA DA TABELA FRETES_FRETEREQUEST:')
                cursor.execute("""
                    SELECT column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns 
                    WHERE table_name = 'fretes_freterequest' 
                    ORDER BY ordinal_position;
                """)
                columns = cursor.fetchall()
                print(f'   Total de colunas: {len(columns)}')
                for column in columns:
                    print(f'   - {column[0]} ({column[1]}) - Null: {column[2]} - Default: {column[3]}')
                
                # 5. VERIFICAR ESTRUTURA DA TABELA FRETES_USERPROFILE
                print('\n👥 ESTRUTURA DA TABELA FRETES_USERPROFILE:')
                cursor.execute("""
                    SELECT column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns 
                    WHERE table_name = 'fretes_userprofile' 
                    ORDER BY ordinal_position;
                """)
                columns = cursor.fetchall()
                print(f'   Total de colunas: {len(columns)}')
                for column in columns:
                    print(f'   - {column[0]} ({column[1]}) - Null: {column[2]} - Default: {column[3]}')
                
                # 6. VERIFICAR ESTRUTURA DA TABELA FRETES_DESTINO
                print('\n🎯 ESTRUTURA DA TABELA FRETES_DESTINO:')
                cursor.execute("""
                    SELECT column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns 
                    WHERE table_name = 'fretes_destino' 
                    ORDER BY ordinal_position;
                """)
                columns = cursor.fetchall()
                print(f'   Total de colunas: {len(columns)}')
                for column in columns:
                    print(f'   - {column[0]} ({column[1]}) - Null: {column[2]} - Default: {column[3]}')
                
                # 7. VERIFICAR ESTRUTURA DA TABELA FRETES_COTACAOFRETE
                print('\n💰 ESTRUTURA DA TABELA FRETES_COTACAOFRETE:')
                cursor.execute("""
                    SELECT column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns 
                    WHERE table_name = 'fretes_cotacaofrete' 
                    ORDER BY ordinal_position;
                """)
                columns = cursor.fetchall()
                print(f'   Total de colunas: {len(columns)}')
                for column in columns:
                    print(f'   - {column[0]} ({column[1]}) - Null: {column[2]} - Default: {column[3]}')
                
                # 8. VERIFICAR ESTRUTURA DA TABELA FRETES_TRANSPORTADORA
                print('\n🚛 ESTRUTURA DA TABELA FRETES_TRANSPORTADORA:')
                cursor.execute("""
                    SELECT column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns 
                    WHERE table_name = 'fretes_transportadora' 
                    ORDER BY ordinal_position;
                """)
                columns = cursor.fetchall()
                print(f'   Total de colunas: {len(columns)}')
                for column in columns:
                    print(f'   - {column[0]} ({column[1]}) - Null: {column[2]} - Default: {column[3]}')
                
                # 9. VERIFICAR ÍNDICES
                print('\n🔍 ÍNDICES CRIADOS:')
                cursor.execute("""
                    SELECT indexname, tablename, indexdef
                    FROM pg_indexes 
                    WHERE schemaname = 'public' 
                    ORDER BY tablename, indexname;
                """)
                indexes = cursor.fetchall()
                print(f'   Total de índices: {len(indexes)}')
                for index in indexes:
                    print(f'   - {index[0]} em {index[1]}')
                
                # 10. VERIFICAR USUÁRIO ADMIN
                print('\n👑 VERIFICANDO USUÁRIO ADMIN:')
                cursor.execute("SELECT id, username, email, is_staff, is_superuser FROM auth_user WHERE username = 'admin';")
                admin = cursor.fetchone()
                if admin:
                    print(f'   ✅ Admin encontrado: ID={admin[0]}, Username={admin[1]}, Email={admin[2]}, Staff={admin[3]}, Superuser={admin[4]}')
                    
                    # Verificar profile do admin
                    cursor.execute("SELECT tipo_acesso, is_master, tipo_usuario FROM fretes_userprofile WHERE user_id = %s;", [admin[0]])
                    profile = cursor.fetchone()
                    if profile:
                        print(f'   ✅ Profile do admin: Acesso={profile[0]}, Master={profile[1]}, Tipo={profile[2]}')
                    else:
                        print('   ❌ Profile do admin não encontrado')
                else:
                    print('   ❌ Usuário admin não encontrado')
                
                print('\n🎉 VERIFICAÇÃO COMPLETA!')
                
        except Exception as e:
            print(f'❌ ERRO: {e}')
            import traceback
            print(f'Detalhes: {traceback.format_exc()}')
        
        print('\n' + '=' * 60)
        print('🏁 VERIFICAÇÃO FINALIZADA!')
