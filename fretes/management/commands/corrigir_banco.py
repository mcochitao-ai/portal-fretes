from django.core.management.base import BaseCommand
from django.db import connection
from django.core.management import call_command
import os

class Command(BaseCommand):
    help = 'Corrige problemas no banco de dados'

    def handle(self, *args, **options):
        print('🔧 CORRIGINDO BANCO DE DADOS')
        print('=' * 50)
        
        # Verificar se está usando PostgreSQL
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            print('❌ Não está usando PostgreSQL')
            return
        
        print('✅ Usando PostgreSQL - corrigindo banco')
        
        try:
            # 1. Executar migrações
            print('\n📝 Executando migrações...')
            call_command('migrate', verbosity=0)
            print('✅ Migrações executadas')
            
            # 2. Verificar se a tabela fretes_userprofile existe
            print('\n🔍 Verificando tabela fretes_userprofile...')
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'fretes_userprofile'
                    );
                """)
                table_exists = cursor.fetchone()[0]
                
                if table_exists:
                    print('✅ Tabela fretes_userprofile existe')
                    
                    # Verificar se a coluna tipo_acesso existe
                    cursor.execute("""
                        SELECT EXISTS (
                            SELECT FROM information_schema.columns 
                            WHERE table_name = 'fretes_userprofile' 
                            AND column_name = 'tipo_acesso'
                        );
                    """)
                    column_exists = cursor.fetchone()[0]
                    
                    if column_exists:
                        print('✅ Coluna tipo_acesso existe')
                    else:
                        print('❌ Coluna tipo_acesso não existe')
                        print('💡 Executando migrações novamente...')
                        call_command('migrate', verbosity=0)
                        print('✅ Migrações executadas novamente')
                else:
                    print('❌ Tabela fretes_userprofile não existe')
                    print('💡 Executando migrações...')
                    call_command('migrate', verbosity=0)
                    print('✅ Migrações executadas')
            
            # 3. Criar usuário admin se não existir
            print('\n👑 Verificando usuário admin...')
            from django.contrib.auth.models import User
            
            if not User.objects.filter(username='admin').exists():
                admin = User.objects.create_user(
                    username='admin',
                    email='admin@portal.com',
                    password='admin123',
                    is_staff=True,
                    is_superuser=True,
                    is_active=True
                )
                print('✅ Usuário admin criado: admin / admin123')
            else:
                print('✅ Usuário admin já existe')
            
            print('\n✅ CORREÇÃO CONCLUÍDA!')
            print('🔑 Login: admin / admin123')
            
        except Exception as e:
            print(f'❌ ERRO: {e}')
            import traceback
            print(f'Detalhes: {traceback.format_exc()}')
        
        print('\n' + '=' * 50)
        print('🏁 CORREÇÃO FINALIZADA!')
