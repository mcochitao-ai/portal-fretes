from django.core.management.base import BaseCommand
from django.db import connection
import os

class Command(BaseCommand):
    help = 'Verifica a estrutura do SQLite local para comparação'

    def handle(self, *args, **options):
        print('🔍 VERIFICANDO ESTRUTURA DO SQLITE LOCAL')
        print('=' * 60)
        
        # Verificar se está usando SQLite
        database_url = os.environ.get('DATABASE_URL')
        if database_url and 'postgresql' in database_url:
            print('❌ Está usando PostgreSQL, não SQLite')
            return
        
        print('✅ Usando SQLite - verificando estrutura local')
        
        try:
            with connection.cursor() as cursor:
                # 1. LISTAR TODAS AS TABELAS
                print('\n📋 TABELAS EXISTENTES:')
                cursor.execute("""
                    SELECT name 
                    FROM sqlite_master 
                    WHERE type='table' 
                    ORDER BY name;
                """)
                tables = cursor.fetchall()
                print(f'   Total de tabelas: {len(tables)}')
                for table in tables:
                    print(f'   ✅ {table[0]}')
                
                # 2. VERIFICAR ESTRUTURA DA TABELA AUTH_USER
                print('\n👤 ESTRUTURA DA TABELA AUTH_USER:')
                cursor.execute("PRAGMA table_info(auth_user);")
                columns = cursor.fetchall()
                print(f'   Total de colunas: {len(columns)}')
                for column in columns:
                    print(f'   - {column[1]} ({column[2]}) - Null: {column[3]} - Default: {column[4]}')
                
                # 3. VERIFICAR ESTRUTURA DA TABELA FRETES_LOJA
                print('\n🏪 ESTRUTURA DA TABELA FRETES_LOJA:')
                cursor.execute("PRAGMA table_info(fretes_loja);")
                columns = cursor.fetchall()
                print(f'   Total de colunas: {len(columns)}')
                for column in columns:
                    print(f'   - {column[1]} ({column[2]}) - Null: {column[3]} - Default: {column[4]}')
                
                # 4. VERIFICAR ESTRUTURA DA TABELA FRETES_FRETEREQUEST
                print('\n📦 ESTRUTURA DA TABELA FRETES_FRETEREQUEST:')
                cursor.execute("PRAGMA table_info(fretes_freterequest);")
                columns = cursor.fetchall()
                print(f'   Total de colunas: {len(columns)}')
                for column in columns:
                    print(f'   - {column[1]} ({column[2]}) - Null: {column[3]} - Default: {column[4]}')
                
                # 5. VERIFICAR ESTRUTURA DA TABELA FRETES_USERPROFILE
                print('\n👥 ESTRUTURA DA TABELA FRETES_USERPROFILE:')
                cursor.execute("PRAGMA table_info(fretes_userprofile);")
                columns = cursor.fetchall()
                print(f'   Total de colunas: {len(columns)}')
                for column in columns:
                    print(f'   - {column[1]} ({column[2]}) - Null: {column[3]} - Default: {column[4]}')
                
                # 6. VERIFICAR ESTRUTURA DA TABELA FRETES_DESTINO
                print('\n🎯 ESTRUTURA DA TABELA FRETES_DESTINO:')
                cursor.execute("PRAGMA table_info(fretes_destino);")
                columns = cursor.fetchall()
                print(f'   Total de colunas: {len(columns)}')
                for column in columns:
                    print(f'   - {column[1]} ({column[2]}) - Null: {column[3]} - Default: {column[4]}')
                
                # 7. VERIFICAR ESTRUTURA DA TABELA FRETES_COTACAOFRETE
                print('\n💰 ESTRUTURA DA TABELA FRETES_COTACAOFRETE:')
                cursor.execute("PRAGMA table_info(fretes_cotacaofrete);")
                columns = cursor.fetchall()
                print(f'   Total de colunas: {len(columns)}')
                for column in columns:
                    print(f'   - {column[1]} ({column[2]}) - Null: {column[3]} - Default: {column[4]}')
                
                # 8. VERIFICAR ESTRUTURA DA TABELA FRETES_TRANSPORTADORA
                print('\n🚛 ESTRUTURA DA TABELA FRETES_TRANSPORTADORA:')
                cursor.execute("PRAGMA table_info(fretes_transportadora);")
                columns = cursor.fetchall()
                print(f'   Total de colunas: {len(columns)}')
                for column in columns:
                    print(f'   - {column[1]} ({column[2]}) - Null: {column[3]} - Default: {column[4]}')
                
                # 9. VERIFICAR ÍNDICES
                print('\n🔍 ÍNDICES CRIADOS:')
                cursor.execute("""
                    SELECT name, tbl_name, sql
                    FROM sqlite_master 
                    WHERE type='index' 
                    ORDER BY tbl_name, name;
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
