from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Verifica senhas dos usuários'

    def handle(self, *args, **options):
        self.stdout.write('🔑 VERIFICANDO SENHAS DOS USUÁRIOS')
        self.stdout.write('=' * 60)
        
        senhas_teste = ['123456', 'admin123', 'password', 'teste123']
        
        for user in User.objects.all():
            self.stdout.write(f'\n👤 Usuário: {user.username}')
            self.stdout.write(f'   📧 Email: {user.email}')
            self.stdout.write(f'   👑 Staff: {user.is_staff}')
            self.stdout.write(f'   🔧 Superuser: {user.is_superuser}')
            self.stdout.write(f'   ✅ Ativo: {user.is_active}')
            
            # Testar senhas
            for senha in senhas_teste:
                if user.check_password(senha):
                    self.stdout.write(f'   🔑 Senha correta: {senha}')
                    break
            else:
                self.stdout.write(f'   ❌ Nenhuma senha de teste funcionou')
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('🏁 VERIFICAÇÃO DE SENHAS COMPLETA!')
