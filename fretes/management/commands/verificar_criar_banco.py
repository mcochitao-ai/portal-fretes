from django.core.management.base import BaseCommand
from django.db import connection
import os

class Command(BaseCommand):
    help = 'Verifica e cria banco PostgreSQL se necessário'

    def handle(self, *args, **options):
        self.stdout.write('🔍 VERIFICANDO E CRIANDO BANCO POSTGRESQL...')
        self.stdout.write('=' * 60)
        
        # 1. Verificar configuração atual
        self.stdout.write('\n📊 CONFIGURAÇÃO ATUAL:')
        db_config = connection.settings_dict
        self.stdout.write(f'   Engine: {db_config["ENGINE"]}')
        self.stdout.write(f'   Host: {db_config["HOST"]}')
        self.stdout.write(f'   Database: {db_config["NAME"]}')
        self.stdout.write(f'   User: {db_config["USER"]}')
        
        # 2. Verificar DATABASE_URL
        self.stdout.write('\n🌍 DATABASE_URL:')
        database_url = os.environ.get('DATABASE_URL')
        if database_url:
            self.stdout.write(f'   ✅ DATABASE_URL definida: {database_url[:50]}...')
        else:
            self.stdout.write('   ❌ DATABASE_URL NÃO definida!')
            self.stdout.write('   🔧 Isso pode ser o problema!')
        
        # 3. Testar conexão
        self.stdout.write('\n🔌 TESTE DE CONEXÃO:')
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                self.stdout.write('   ✅ Conexão com banco: OK')
        except Exception as e:
            self.stdout.write(f'   ❌ Erro na conexão: {e}')
            self.stdout.write('   🔧 Problema na conexão com o banco!')
            return
        
        # 4. Verificar se é PostgreSQL
        if 'postgresql' not in db_config['ENGINE']:
            self.stdout.write('\n❌ PROBLEMA IDENTIFICADO:')
            self.stdout.write('   Não está usando PostgreSQL!')
            self.stdout.write('   Engine atual: ' + db_config['ENGINE'])
            self.stdout.write('   🔧 Verifique a configuração do DATABASE_URL')
            return
        
        # 5. Verificar tabelas
        self.stdout.write('\n📋 VERIFICANDO TABELAS:')
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
                    self.stdout.write(f'   ✅ {len(tables)} tabelas encontradas')
                    for table in tables:
                        self.stdout.write(f'   - {table[0]}')
                else:
                    self.stdout.write('   ❌ Nenhuma tabela encontrada!')
                    self.stdout.write('   🔧 As migrações não foram executadas')
        except Exception as e:
            self.stdout.write(f'   ❌ Erro ao verificar tabelas: {e}')
        
        # 6. Verificar se auth_user existe
        self.stdout.write('\n👤 VERIFICANDO TABELA auth_user:')
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'auth_user'
                    );
                """)
                auth_user_exists = cursor.fetchone()[0]
                
                if auth_user_exists:
                    self.stdout.write('   ✅ Tabela auth_user existe')
                else:
                    self.stdout.write('   ❌ Tabela auth_user NÃO existe!')
                    self.stdout.write('   🔧 Execute: python manage.py migrate')
        except Exception as e:
            self.stdout.write(f'   ❌ Erro ao verificar auth_user: {e}')
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('🏁 VERIFICAÇÃO COMPLETA!')
        
        # 7. Recomendações
        self.stdout.write('\n💡 RECOMENDAÇÕES:')
        if not database_url:
            self.stdout.write('   1. Verifique se o banco PostgreSQL foi criado no Render')
            self.stdout.write('   2. Verifique se a variável DATABASE_URL está configurada')
        elif not tables:
            self.stdout.write('   1. Execute: python manage.py makemigrations')
            self.stdout.write('   2. Execute: python manage.py migrate')
        else:
            self.stdout.write('   ✅ Banco PostgreSQL configurado corretamente!')
