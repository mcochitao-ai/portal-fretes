from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
import os

class Command(BaseCommand):
    help = 'Força a execução das migrações no PostgreSQL'

    def handle(self, *args, **options):
        self.stdout.write('🔄 Forçando execução das migrações...')
        self.stdout.write('=' * 60)
        
        # Verificar conexão
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                self.stdout.write('✅ Conexão com banco: OK')
        except Exception as e:
            self.stdout.write(f'❌ Erro na conexão: {e}')
            return
        
        # Verificar se é PostgreSQL
        db_config = connection.settings_dict
        if 'postgresql' not in db_config['ENGINE']:
            self.stdout.write('❌ Não é PostgreSQL, abortando...')
            return
        
        self.stdout.write('✅ Usando PostgreSQL')
        
        # Executar makemigrations
        self.stdout.write('\n📝 Executando makemigrations...')
        try:
            call_command('makemigrations', verbosity=0)
            self.stdout.write('✅ makemigrations executado')
        except Exception as e:
            self.stdout.write(f'⚠️ makemigrations: {e}')
        
        # Executar migrate
        self.stdout.write('\n🔄 Executando migrate...')
        try:
            call_command('migrate', verbosity=0)
            self.stdout.write('✅ migrate executado')
        except Exception as e:
            self.stdout.write(f'❌ Erro no migrate: {e}')
            return
        
        # Verificar se tabelas foram criadas
        self.stdout.write('\n📋 Verificando tabelas criadas...')
        try:
            with connection.cursor() as cursor:
                # Verificar tabela auth_user
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'auth_user'
                    );
                """)
                auth_user_exists = cursor.fetchone()[0]
                
                if auth_user_exists:
                    self.stdout.write('✅ Tabela auth_user: Criada')
                else:
                    self.stdout.write('❌ Tabela auth_user: NÃO criada')
                
                # Verificar tabela fretes_freterequest
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'fretes_freterequest'
                    );
                """)
                fretes_exists = cursor.fetchone()[0]
                
                if fretes_exists:
                    self.stdout.write('✅ Tabela fretes_freterequest: Criada')
                else:
                    self.stdout.write('❌ Tabela fretes_freterequest: NÃO criada')
                
                # Listar todas as tabelas
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    ORDER BY table_name;
                """)
                tables = cursor.fetchall()
                
                self.stdout.write(f'\n📊 Total de tabelas: {len(tables)}')
                for table in tables:
                    self.stdout.write(f'   - {table[0]}')
                
        except Exception as e:
            self.stdout.write(f'❌ Erro ao verificar tabelas: {e}')
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('🎯 Migrações forçadas!')
