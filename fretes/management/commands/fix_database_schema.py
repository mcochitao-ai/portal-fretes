from django.core.management.base import BaseCommand
from django.db import connection
from django.core.management import call_command
import os

class Command(BaseCommand):
    help = 'Fix database schema issues by ensuring all migrations are applied'

    def handle(self, *args, **options):
        self.stdout.write('🔧 FIXING DATABASE SCHEMA')
        self.stdout.write('=' * 80)
        
        # Verificar se está no PostgreSQL
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            self.stdout.write('❌ DATABASE_URL não encontrada - usando SQLite')
            return
        
        self.stdout.write('✅ Usando PostgreSQL - corrigindo schema do banco')
        
        try:
            # 1. VERIFICAR TABELAS EXISTENTES
            self.stdout.write('\n🔍 VERIFICANDO TABELAS EXISTENTES:')
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    ORDER BY table_name;
                """)
                tables = cursor.fetchall()
                table_names = [table[0] for table in tables]
                
                self.stdout.write(f'   📋 Tabelas encontradas: {len(table_names)}')
                for table in table_names:
                    self.stdout.write(f'      - {table}')
            
            # 2. VERIFICAR SE FRETES_USERPROFILE EXISTE
            if 'fretes_userprofile' not in table_names:
                self.stdout.write('\n❌ Tabela fretes_userprofile não encontrada!')
                self.stdout.write('   💡 Executando migrações...')
                
                # Executar migrações
                call_command('migrate', verbosity=0)
                self.stdout.write('   ✅ Migrações executadas')
            else:
                self.stdout.write('\n✅ Tabela fretes_userprofile encontrada')
                
                # 3. VERIFICAR COLUNAS DA TABELA FRETES_USERPROFILE
                self.stdout.write('\n🔍 VERIFICANDO COLUNAS DA TABELA FRETES_USERPROFILE:')
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT column_name, data_type 
                        FROM information_schema.columns 
                        WHERE table_name = 'fretes_userprofile' 
                        ORDER BY column_name;
                    """)
                    columns = cursor.fetchall()
                    
                    self.stdout.write(f'   📋 Colunas encontradas: {len(columns)}')
                    for column in columns:
                        self.stdout.write(f'      - {column[0]} ({column[1]})')
                    
                    # Verificar se tipo_acesso existe
                    column_names = [col[0] for col in columns]
                    if 'tipo_acesso' not in column_names:
                        self.stdout.write('\n❌ Coluna tipo_acesso não encontrada!')
                        self.stdout.write('   💡 Executando migrações para corrigir...')
                        
                        # Executar migrações
                        call_command('migrate', verbosity=0)
                        self.stdout.write('   ✅ Migrações executadas')
                    else:
                        self.stdout.write('\n✅ Coluna tipo_acesso encontrada')
            
            # 4. VERIFICAR MIGRAÇÕES APLICADAS
            self.stdout.write('\n📝 VERIFICANDO MIGRAÇÕES APLICADAS:')
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT app, name, applied 
                    FROM django_migrations 
                    WHERE app = 'fretes' 
                    ORDER BY applied;
                """)
                migrations = cursor.fetchall()
                
                self.stdout.write(f'   📋 Migrações aplicadas: {len(migrations)}')
                for migration in migrations:
                    self.stdout.write(f'      - {migration[0]}.{migration[1]} ({migration[2]})')
            
            # 5. TESTAR CRIAR UM USERPROFILE
            self.stdout.write('\n🧪 TESTANDO CRIAÇÃO DE USERPROFILE:')
            try:
                from django.contrib.auth.models import User
                from fretes.models import UserProfile
                
                # Verificar se existe pelo menos um usuário
                if User.objects.exists():
                    user = User.objects.first()
                    self.stdout.write(f'   👤 Testando com usuário: {user.username}')
                    
                    # Tentar acessar o profile
                    try:
                        profile = user.userprofile
                        self.stdout.write(f'   ✅ Profile encontrado: {profile.tipo_acesso}')
                    except UserProfile.DoesNotExist:
                        self.stdout.write('   ⚠️ Profile não existe, criando...')
                        profile = UserProfile.objects.create(user=user)
                        self.stdout.write(f'   ✅ Profile criado: {profile.tipo_acesso}')
                else:
                    self.stdout.write('   ⚠️ Nenhum usuário encontrado no banco')
                    
            except Exception as e:
                self.stdout.write(f'   ❌ Erro ao testar UserProfile: {e}')
            
            self.stdout.write('\n✅ VERIFICAÇÃO DE SCHEMA CONCLUÍDA!')
            
        except Exception as e:
            self.stdout.write(f'❌ ERRO: {e}')
            import traceback
            self.stdout.write(f'   Traceback: {traceback.format_exc()}')
        
        self.stdout.write('\n' + '=' * 80)
        self.stdout.write('🏁 CORREÇÃO DE SCHEMA COMPLETA!')
