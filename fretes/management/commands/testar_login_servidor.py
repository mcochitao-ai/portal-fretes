from django.core.management.base import BaseCommand
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Testa login no servidor'

    def handle(self, *args, **options):
        self.stdout.write('🔐 TESTANDO LOGIN NO SERVIDOR')
        self.stdout.write('=' * 60)
        
        # Mostrar ambiente
        self.stdout.write(f'🌍 Ambiente: {"RENDER" if os.environ.get("RENDER") else "LOCAL"}')
        
        # Listar todos os usuários
        self.stdout.write('\n👥 USUÁRIOS NO BANCO:')
        try:
            users = User.objects.all()
            self.stdout.write(f'   Total: {users.count()}')
            for user in users:
                status = '✅' if user.is_active else '❌'
                staff = '👑' if user.is_staff else '👤'
                self.stdout.write(f'   {status} {staff} {user.username}')
        except Exception as e:
            self.stdout.write(f'   ❌ Erro ao listar usuários: {e}')
        
        # Testar login do cochit0
        self.stdout.write('\n🔐 TESTE DE LOGIN COCHIT0:')
        try:
            # Verificar se usuário existe
            try:
                user = User.objects.get(username='cochit0')
                self.stdout.write(f'   ✅ Usuário encontrado: {user.username}')
                self.stdout.write(f'   📧 Email: {user.email}')
                self.stdout.write(f'   👑 Staff: {user.is_staff}')
                self.stdout.write(f'   🔧 Superuser: {user.is_superuser}')
                self.stdout.write(f'   ✅ Ativo: {user.is_active}')
                
                # Testar autenticação
                auth_user = authenticate(username='cochit0', password='123456')
                if auth_user:
                    self.stdout.write('   ✅ Autenticação: SUCESSO!')
                    self.stdout.write(f'   🆔 ID: {auth_user.id}')
                else:
                    self.stdout.write('   ❌ Autenticação: FALHOU!')
                    
                    # Verificar senha
                    if user.check_password('123456'):
                        self.stdout.write('   🔑 Senha está correta no banco')
                    else:
                        self.stdout.write('   ❌ Senha está INCORRETA no banco')
                        
            except User.DoesNotExist:
                self.stdout.write('   ❌ Usuário cochit0 NÃO ENCONTRADO!')
                
        except Exception as e:
            self.stdout.write(f'   ❌ Erro: {e}')
            import traceback
            self.stdout.write(f'   Traceback: {traceback.format_exc()}')
        
        # Testar outros usuários
        self.stdout.write('\n🔐 TESTE DE OUTROS USUÁRIOS:')
        usuarios_teste = [
            ('admin', 'admin123'),
            ('teste', '123456'),
            ('gerente_teste', '123456'),
        ]
        
        for username, password in usuarios_teste:
            try:
                user = User.objects.get(username=username)
                auth_user = authenticate(username=username, password=password)
                if auth_user:
                    self.stdout.write(f'   ✅ {username}: SUCESSO')
                else:
                    self.stdout.write(f'   ❌ {username}: FALHOU')
            except User.DoesNotExist:
                self.stdout.write(f'   ❌ {username}: NÃO EXISTE')
            except Exception as e:
                self.stdout.write(f'   ❌ {username}: ERRO - {e}')
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('🏁 TESTE DE LOGIN COMPLETO!')
