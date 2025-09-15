from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection
import os

class Command(BaseCommand):
    help = 'Verifica qual banco de dados está sendo usado'

    def handle(self, *args, **options):
        self.stdout.write('🔍 Verificando configuração do banco de dados...')
        self.stdout.write('=' * 60)
        
        # Verificar configuração do Django
        db_config = settings.DATABASES['default']
        self.stdout.write(f'📊 Engine: {db_config["ENGINE"]}')
        self.stdout.write(f'📊 Name: {db_config["NAME"]}')
        self.stdout.write(f'📊 Host: {db_config.get("HOST", "N/A")}')
        self.stdout.write(f'📊 Port: {db_config.get("PORT", "N/A")}')
        self.stdout.write(f'📊 User: {db_config.get("USER", "N/A")}')
        
        # Verificar variáveis de ambiente
        self.stdout.write('\n🌍 Variáveis de ambiente:')
        database_url = os.environ.get('DATABASE_URL')
        if database_url:
            self.stdout.write(f'✅ DATABASE_URL: {database_url[:50]}...')
        else:
            self.stdout.write('❌ DATABASE_URL: Não definida')
        
        # Verificar conexão
        self.stdout.write('\n🔌 Testando conexão:')
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                if result:
                    self.stdout.write('✅ Conexão com banco: OK')
                else:
                    self.stdout.write('❌ Conexão com banco: FALHOU')
        except Exception as e:
            self.stdout.write(f'❌ Erro na conexão: {e}')
        
        # Verificar se é SQLite ou PostgreSQL
        if 'sqlite' in db_config['ENGINE']:
            self.stdout.write('\n⚠️ ATENÇÃO: Usando SQLite (dados serão perdidos!)')
            self.stdout.write('💡 Para usar PostgreSQL, verifique a variável DATABASE_URL')
        elif 'postgresql' in db_config['ENGINE']:
            self.stdout.write('\n✅ Usando PostgreSQL (dados persistentes)')
        else:
            self.stdout.write(f'\n❓ Banco desconhecido: {db_config["ENGINE"]}')
        
        self.stdout.write('=' * 60)
