from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import connection
from django.contrib.auth import authenticate
import os

class Command(BaseCommand):
    help = 'Debug completo do sistema'

    def handle(self, *args, **options):
        self.stdout.write('🔍 DEBUG COMPLETO DO SISTEMA')
        self.stdout.write('=' * 60)
        
        # 1. Verificar configuração do banco
        self.stdout.write('\n📊 CONFIGURAÇÃO DO BANCO:')
        db_config = connection.settings_dict
        self.stdout.write(f'   Engine: {db_config["ENGINE"]}')
        self.stdout.write(f'   Host: {db_config["HOST"]}')
        self.stdout.write(f'   Database: {db_config["NAME"]}')
        self.stdout.write(f'   User: {db_config["USER"]}')
        
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
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    ORDER BY table_name;
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
        
        # 5. Testar autenticação
        self.stdout.write('\n🔐 TESTE DE AUTENTICAÇÃO:')
        test_users = ['teste', 'cochit0', 'admin']
        for username in test_users:
            try:
                user = authenticate(username=username, password='123456')
                if user:
                    self.stdout.write(f'   ✅ {username} / 123456: OK')
                else:
                    self.stdout.write(f'   ❌ {username} / 123456: FALHOU')
            except Exception as e:
                self.stdout.write(f'   ❌ {username}: ERRO - {e}')
        
        # 6. Verificar variáveis de ambiente
        self.stdout.write('\n🌍 VARIÁVEIS DE AMBIENTE:')
        env_vars = ['DATABASE_URL', 'SECRET_KEY', 'DEBUG', 'ALLOWED_HOSTS']
        for var in env_vars:
            value = os.environ.get(var, 'NÃO DEFINIDA')
            if var == 'SECRET_KEY' and value != 'NÃO DEFINIDA':
                value = f'{value[:10]}...'  # Mostrar apenas os primeiros 10 caracteres
            self.stdout.write(f'   {var}: {value}')
        
        # 7. Verificar se é PostgreSQL
        self.stdout.write('\n🐘 VERIFICAÇÃO POSTGRESQL:')
        if 'postgresql' in db_config['ENGINE']:
            self.stdout.write('   ✅ Usando PostgreSQL')
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT version();")
                    version = cursor.fetchone()[0]
                    self.stdout.write(f'   Versão: {version[:50]}...')
            except Exception as e:
                self.stdout.write(f'   ❌ Erro ao verificar versão: {e}')
        else:
            self.stdout.write('   ❌ NÃO está usando PostgreSQL!')
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('🏁 DEBUG COMPLETO FINALIZADO!')
