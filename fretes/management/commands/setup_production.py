from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import connection
from fretes.models import Transportadora, Loja, UserProfile
import os

class Command(BaseCommand):
    help = 'Setup production database with proper migrations and initial data'

    def handle(self, *args, **options):
        self.stdout.write('🚀 SETUP PRODUÇÃO - CONFIGURANDO BANCO')
        self.stdout.write('=' * 80)
        
        # Verificar se está no PostgreSQL
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            self.stdout.write('❌ DATABASE_URL não encontrada - usando SQLite')
            return
        
        self.stdout.write('✅ Usando PostgreSQL - configurando banco de produção')
        
        try:
            # 1. VERIFICAR SE TABELAS EXISTEM
            self.stdout.write('\n🔍 VERIFICANDO TABELAS:')
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
                
                # Verificar se auth_user existe
                if 'auth_user' not in table_names:
                    self.stdout.write('   ❌ Tabela auth_user não encontrada!')
                    self.stdout.write('   💡 Execute: python manage.py migrate')
                    return
                else:
                    self.stdout.write('   ✅ Tabela auth_user encontrada')
            
            # 2. CRIAR USUÁRIO ADMIN SE NÃO EXISTIR
            self.stdout.write('\n👑 VERIFICANDO USUÁRIO ADMIN:')
            if not User.objects.filter(username='admin').exists():
                admin = User.objects.create_user(
                    username='admin',
                    email='admin@portal.com',
                    password='admin123',
                    is_staff=True,
                    is_superuser=True,
                    is_active=True
                )
                self.stdout.write('   ✅ Admin criado: admin / admin123')
            else:
                self.stdout.write('   ⚠️ Admin já existe')
            
            # 3. CRIAR TRANSPORTADORAS BÁSICAS
            self.stdout.write('\n🚛 VERIFICANDO TRANSPORTADORAS:')
            transportadoras_basicas = [
                {'nome': 'Translero', 'email': 'mcochitao@gmail.com'},
                {'nome': 'Log20', 'email': 'log20@transportadora.com'},
            ]
            
            for trans_data in transportadoras_basicas:
                if not Transportadora.objects.filter(nome=trans_data['nome']).exists():
                    transportadora = Transportadora.objects.create(
                        nome=trans_data['nome'],
                        email=trans_data['email']
                    )
                    self.stdout.write(f'   ✅ {transportadora.nome} criada')
                else:
                    self.stdout.write(f'   ⚠️ {trans_data["nome"]} já existe')
            
            # 4. VERIFICAR LOGIN
            self.stdout.write('\n🔐 TESTANDO LOGIN:')
            from django.contrib.auth import authenticate
            
            user = authenticate(username='admin', password='admin123')
            if user:
                self.stdout.write('   ✅ Login admin funcionando!')
            else:
                self.stdout.write('   ❌ Login admin falhou!')
            
            # 5. VERIFICAR CONTAGENS
            self.stdout.write('\n📊 VERIFICANDO DADOS:')
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM auth_user;")
                user_count = cursor.fetchone()[0]
                self.stdout.write(f'   👥 Total de usuários: {user_count}')
                
                cursor.execute("SELECT COUNT(*) FROM fretes_transportadora;")
                trans_count = cursor.fetchone()[0]
                self.stdout.write(f'   🚛 Total de transportadoras: {trans_count}')
            
            self.stdout.write('\n✅ SETUP PRODUÇÃO CONCLUÍDO COM SUCESSO!')
            self.stdout.write('🔑 CREDENCIAIS:')
            self.stdout.write('   admin / admin123 (Admin)')
            
        except Exception as e:
            self.stdout.write(f'❌ ERRO: {e}')
            import traceback
            self.stdout.write(f'   Traceback: {traceback.format_exc()}')
        
        self.stdout.write('\n' + '=' * 80)
        self.stdout.write('🏁 SETUP PRODUÇÃO COMPLETO!')
