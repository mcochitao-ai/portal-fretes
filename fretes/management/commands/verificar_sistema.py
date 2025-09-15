from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import connection
import os

class Command(BaseCommand):
    help = 'Verifica se o sistema está funcionando'

    def handle(self, *args, **options):
        self.stdout.write('🔍 VERIFICANDO SISTEMA COMPLETO...')
        self.stdout.write('=' * 60)
        
        # 1. Verificar configuração do banco
        self.stdout.write('\n📊 CONFIGURAÇÃO DO BANCO:')
        db_config = connection.settings_dict
        self.stdout.write(f'   Engine: {db_config["ENGINE"]}')
        self.stdout.write(f'   Name: {db_config["NAME"]}')
        
        # 2. Testar conexão
        self.stdout.write('\n🔌 TESTE DE CONEXÃO:')
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                self.stdout.write('   ✅ Conexão com banco: OK')
        except Exception as e:
            self.stdout.write(f'   ❌ Erro na conexão: {e}')
            return
        
        # 3. Verificar tabelas
        self.stdout.write('\n📋 TABELAS NO BANCO:')
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' 
                    ORDER BY name;
                """)
                tables = cursor.fetchall()
                
                if tables:
                    self.stdout.write(f'   Total: {len(tables)} tabelas')
                    for table in tables:
                        self.stdout.write(f'   - {table[0]}')
                else:
                    self.stdout.write('   ❌ Nenhuma tabela encontrada!')
        except Exception as e:
            self.stdout.write(f'   ❌ Erro ao verificar tabelas: {e}')
        
        # 4. Verificar usuários
        self.stdout.write('\n👥 USUÁRIOS NO BANCO:')
        try:
            users = User.objects.all()
            if users:
                self.stdout.write(f'   Total: {users.count()} usuários')
                for user in users:
                    self.stdout.write(f'   - {user.username} (staff: {user.is_staff}, super: {user.is_superuser}, active: {user.is_active})')
            else:
                self.stdout.write('   ❌ Nenhum usuário encontrado!')
        except Exception as e:
            self.stdout.write(f'   ❌ Erro ao verificar usuários: {e}')
        
        # 5. Criar usuário admin se não existir
        self.stdout.write('\n👤 CRIANDO USUÁRIO ADMIN...')
        try:
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser(
                    username='admin',
                    email='admin@admin.com',
                    password='admin123'
                )
                self.stdout.write('   ✅ Usuário admin criado!')
            else:
                self.stdout.write('   ✅ Usuário admin já existe!')
            
            # Verificar se foi criado
            user = User.objects.get(username='admin')
            self.stdout.write(f'   ID: {user.id}')
            self.stdout.write(f'   is_staff: {user.is_staff}')
            self.stdout.write(f'   is_superuser: {user.is_superuser}')
            self.stdout.write(f'   is_active: {user.is_active}')
            
        except Exception as e:
            self.stdout.write(f'   ❌ Erro ao criar usuário: {e}')
        
        # 6. Testar autenticação
        self.stdout.write('\n🔐 TESTE DE AUTENTICAÇÃO:')
        try:
            from django.contrib.auth import authenticate
            auth_user = authenticate(username='admin', password='admin123')
            if auth_user:
                self.stdout.write('   ✅ Autenticação funcionando!')
            else:
                self.stdout.write('   ❌ Autenticação falhou!')
        except Exception as e:
            self.stdout.write(f'   ❌ Erro na autenticação: {e}')
        
        # 7. Verificar variáveis de ambiente
        self.stdout.write('\n🌍 VARIÁVEIS DE AMBIENTE:')
        env_vars = ['SECRET_KEY', 'DEBUG', 'ALLOWED_HOSTS']
        for var in env_vars:
            value = os.environ.get(var, 'NÃO DEFINIDA')
            if var == 'SECRET_KEY' and value != 'NÃO DEFINIDA':
                value = f'{value[:10]}...'
            self.stdout.write(f'   {var}: {value}')
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('🏁 VERIFICAÇÃO COMPLETA!')
        self.stdout.write('Teste com:')
        self.stdout.write('   Username: admin')
        self.stdout.write('   Password: admin123')
