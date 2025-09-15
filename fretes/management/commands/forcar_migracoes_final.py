from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'FORÇA migrações e cria usuário de teste'

    def handle(self, *args, **options):
        self.stdout.write('🚨 FORÇANDO MIGRAÇÕES E CRIAÇÃO DE USUÁRIO...')
        self.stdout.write('=' * 60)
        
        # 1. Verificar conexão
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                self.stdout.write('✅ Conexão com PostgreSQL: OK')
        except Exception as e:
            self.stdout.write(f'❌ Erro na conexão: {e}')
            return
        
        # 2. Verificar tabelas antes
        self.stdout.write('\n📋 TABELAS ANTES:')
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    ORDER BY table_name;
                """)
                tables_before = cursor.fetchall()
                self.stdout.write(f'   {len(tables_before)} tabelas encontradas')
        except Exception as e:
            self.stdout.write(f'   Erro: {e}')
        
        # 3. Executar makemigrations
        self.stdout.write('\n🔄 EXECUTANDO MAKEMIGRATIONS...')
        try:
            call_command('makemigrations', verbosity=2)
            self.stdout.write('✅ makemigrations executado')
        except Exception as e:
            self.stdout.write(f'❌ Erro no makemigrations: {e}')
        
        # 4. Executar migrate
        self.stdout.write('\n🔄 EXECUTANDO MIGRATE...')
        try:
            call_command('migrate', verbosity=2)
            self.stdout.write('✅ migrate executado')
        except Exception as e:
            self.stdout.write(f'❌ Erro no migrate: {e}')
        
        # 5. Verificar tabelas depois
        self.stdout.write('\n📋 TABELAS DEPOIS:')
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    ORDER BY table_name;
                """)
                tables_after = cursor.fetchall()
                self.stdout.write(f'   {len(tables_after)} tabelas encontradas')
                for table in tables_after:
                    self.stdout.write(f'   - {table[0]}')
        except Exception as e:
            self.stdout.write(f'   Erro: {e}')
        
        # 6. Criar usuário de teste
        self.stdout.write('\n👤 CRIANDO USUÁRIO DE TESTE...')
        try:
            # Deletar se existir
            if User.objects.filter(username='teste').exists():
                User.objects.filter(username='teste').delete()
                self.stdout.write('   Usuário teste antigo removido')
            
            # Criar novo
            user = User.objects.create_user(
                username='teste',
                email='teste@teste.com',
                password='123456',
                first_name='Usuario',
                last_name='Teste',
                is_staff=True,
                is_superuser=True,
                is_active=True
            )
            
            self.stdout.write('✅ Usuário teste criado!')
            self.stdout.write('   Username: teste')
            self.stdout.write('   Password: 123456')
            
            # Verificar se foi criado
            user_check = User.objects.get(username='teste')
            self.stdout.write(f'   ID: {user_check.id}')
            self.stdout.write(f'   is_staff: {user_check.is_staff}')
            self.stdout.write(f'   is_superuser: {user_check.is_superuser}')
            self.stdout.write(f'   is_active: {user_check.is_active}')
            
        except Exception as e:
            self.stdout.write(f'❌ Erro ao criar usuário: {e}')
        
        # 7. Testar autenticação
        self.stdout.write('\n🔐 TESTANDO AUTENTICAÇÃO...')
        try:
            from django.contrib.auth import authenticate
            auth_user = authenticate(username='teste', password='123456')
            if auth_user:
                self.stdout.write('✅ Autenticação funcionando!')
            else:
                self.stdout.write('❌ Autenticação falhou!')
        except Exception as e:
            self.stdout.write(f'❌ Erro na autenticação: {e}')
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('🏁 PROCESSO FINALIZADO!')
