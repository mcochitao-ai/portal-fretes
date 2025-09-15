from django.core.management.base import BaseCommand
from django.contrib.auth import authenticate

class Command(BaseCommand):
    help = 'Testa login de usuários'

    def handle(self, *args, **options):
        self.stdout.write('🔐 TESTANDO LOGIN DE USUÁRIOS')
        self.stdout.write('=' * 60)
        
        # Lista de usuários para testar
        usuarios_teste = [
            ('cochit0', '123456'),
            ('admin', 'admin123'),
            ('teste', '123456'),
            ('gerente_teste', '123456'),
        ]
        
        for username, password in usuarios_teste:
            self.stdout.write(f'\n👤 Testando: {username}')
            user = authenticate(username=username, password=password)
            
            if user:
                self.stdout.write(f'   ✅ Login SUCESSO!')
                self.stdout.write(f'   📧 Email: {user.email}')
                self.stdout.write(f'   👑 Staff: {user.is_staff}')
                self.stdout.write(f'   🔧 Superuser: {user.is_superuser}')
                self.stdout.write(f'   ✅ Ativo: {user.is_active}')
            else:
                self.stdout.write(f'   ❌ Login FALHOU!')
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('🏁 TESTE DE LOGIN COMPLETO!')
