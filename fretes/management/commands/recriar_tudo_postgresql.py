from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import connection
from fretes.models import Transportadora, Loja, UserProfile
import os

class Command(BaseCommand):
    help = 'Recria todos os dados no PostgreSQL'

    def handle(self, *args, **options):
        self.stdout.write('🔄 RECRIANDO TUDO NO POSTGRESQL')
        self.stdout.write('=' * 80)
        
        # Verificar se está no PostgreSQL
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            self.stdout.write('❌ DATABASE_URL não encontrada - usando SQLite')
            return
        
        self.stdout.write('✅ Usando PostgreSQL - recriando todos os dados')
        
        try:
            # 1. LIMPAR TUDO
            self.stdout.write('\n🧹 LIMPANDO DADOS EXISTENTES:')
            User.objects.all().delete()
            Transportadora.objects.all().delete()
            Loja.objects.all().delete()
            self.stdout.write('   ✅ Todos os dados removidos')
            
            # 2. CRIAR USUÁRIOS ADMIN
            self.stdout.write('\n👑 CRIANDO USUÁRIOS ADMIN:')
            
            # Admin principal
            admin = User.objects.create_user(
                username='admin',
                email='admin@portal.com',
                password='admin123',
                is_staff=True,
                is_superuser=True,
                is_active=True
            )
            self.stdout.write('   ✅ Admin criado: admin / admin123')
            
            # Cochit0
            cochit0 = User.objects.create_user(
                username='cochit0',
                email='cochit0@portal.com',
                password='123456',
                is_staff=True,
                is_superuser=True,
                is_active=True
            )
            self.stdout.write('   ✅ Cochit0 criado: cochit0 / 123456')
            
            # 3. CRIAR TRANSPORTADORAS
            self.stdout.write('\n🚛 CRIANDO TRANSPORTADORAS:')
            
            transportadoras = [
                {'nome': 'Translero', 'email': 'mcochitao@gmail.com'},
                {'nome': 'Log20', 'email': 'log20@transportadora.com'},
                {'nome': 'Leão Log', 'email': 'leaolog@transportadora.com'},
                {'nome': 'Soluciona', 'email': 'soluciona@transportadora.com'},
                {'nome': 'Nika', 'email': 'nika@transportadora.com'},
                {'nome': 'Rodo Flip', 'email': 'rodoflip@transportadora.com'},
            ]
            
            for trans_data in transportadoras:
                transportadora = Transportadora.objects.create(
                    nome=trans_data['nome'],
                    email=trans_data['email']
                )
                self.stdout.write(f'   ✅ {transportadora.nome} criada')
            
            # 4. CRIAR USUÁRIOS TRANSPORTADORAS
            self.stdout.write('\n👥 CRIANDO USUÁRIOS TRANSPORTADORAS:')
            
            usuarios_transportadoras = [
                {'username': 'translero', 'email': 'mcochitao@gmail.com', 'transportadora': 'Translero'},
                {'username': 'log20', 'email': 'log20@transportadora.com', 'transportadora': 'Log20'},
                {'username': 'leao_log', 'email': 'leaolog@transportadora.com', 'transportadora': 'Leão Log'},
                {'username': 'soluciona', 'email': 'soluciona@transportadora.com', 'transportadora': 'Soluciona'},
                {'username': 'nika', 'email': 'nika@transportadora.com', 'transportadora': 'Nika'},
                {'username': 'rodo_flip', 'email': 'rodoflip@transportadora.com', 'transportadora': 'Rodo Flip'},
            ]
            
            for user_data in usuarios_transportadoras:
                transportadora = Transportadora.objects.get(nome=user_data['transportadora'])
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password='123456',
                    is_staff=False,
                    is_superuser=False,
                    is_active=True
                )
                
                # Criar UserProfile
                UserProfile.objects.create(
                    user=user,
                    tipo_usuario='transportadora',
                    transportadora=transportadora
                )
                
                self.stdout.write(f'   ✅ {user.username} criado (senha: 123456)')
            
            # 5. CRIAR USUÁRIOS SOLICITADORES
            self.stdout.write('\n👤 CRIANDO USUÁRIOS SOLICITADORES:')
            
            usuarios_solicitadores = [
                {'username': 'murilo_teste', 'email': 'murilo@teste.com'},
                {'username': 'transportadora_teste', 'email': 'transportadora@teste.com'},
                {'username': 'teste_solicitador', 'email': 'teste@teste2.com'},
            ]
            
            for user_data in usuarios_solicitadores:
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password='123456',
                    is_staff=False,
                    is_superuser=False,
                    is_active=True
                )
                
                # Criar UserProfile
                UserProfile.objects.create(
                    user=user,
                    tipo_usuario='solicitador'
                )
                
                self.stdout.write(f'   ✅ {user.username} criado (senha: 123456)')
            
            # 6. TESTAR LOGIN
            self.stdout.write('\n🔐 TESTANDO LOGIN:')
            from django.contrib.auth import authenticate
            
            usuarios_teste = [
                ('admin', 'admin123'),
                ('cochit0', '123456'),
                ('translero', '123456'),
                ('log20', '123456'),
            ]
            
            for username, password in usuarios_teste:
                user = authenticate(username=username, password=password)
                if user:
                    self.stdout.write(f'   ✅ {username}: SUCESSO')
                else:
                    self.stdout.write(f'   ❌ {username}: FALHOU')
            
            # 7. VERIFICAR BANCO
            self.stdout.write('\n🗄️ VERIFICANDO BANCO:')
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM auth_user;")
                user_count = cursor.fetchone()[0]
                self.stdout.write(f'   👥 Total de usuários: {user_count}')
                
                cursor.execute("SELECT COUNT(*) FROM fretes_transportadora;")
                trans_count = cursor.fetchone()[0]
                self.stdout.write(f'   🚛 Total de transportadoras: {trans_count}')
            
            self.stdout.write('\n✅ TODOS OS DADOS RECRIADOS COM SUCESSO!')
            
        except Exception as e:
            self.stdout.write(f'❌ ERRO: {e}')
            import traceback
            self.stdout.write(f'   Traceback: {traceback.format_exc()}')
        
        self.stdout.write('\n' + '=' * 80)
        self.stdout.write('🏁 RECRIAÇÃO COMPLETA!')
        self.stdout.write('🔑 CREDENCIAIS:')
        self.stdout.write('   admin / admin123 (Admin)')
        self.stdout.write('   cochit0 / 123456 (Admin)')
        self.stdout.write('   translero / 123456 (Transportadora)')
        self.stdout.write('   log20 / 123456 (Transportadora)')
        self.stdout.write('   murilo_teste / 123456 (Solicitador)')
