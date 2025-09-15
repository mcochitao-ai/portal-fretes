from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Cria usuário admin definitivo'

    def handle(self, *args, **options):
        self.stdout.write('👑 CRIANDO USUÁRIO ADMIN DEFINITIVO')
        self.stdout.write('=' * 60)
        
        # Mostrar ambiente
        self.stdout.write(f'🌍 Ambiente: {"RENDER" if os.environ.get("RENDER") else "LOCAL"}')
        
        try:
            # Deletar usuário admin se existir
            try:
                old_admin = User.objects.get(username='admin')
                old_admin.delete()
                self.stdout.write('🗑️ Usuário admin antigo removido')
            except User.DoesNotExist:
                self.stdout.write('ℹ️ Nenhum usuário admin antigo encontrado')
            
            # Criar novo usuário admin
            admin = User.objects.create_user(
                username='admin',
                email='admin@portal.com',
                password='admin123',
                is_staff=True,
                is_superuser=True,
                is_active=True
            )
            
            self.stdout.write('✅ Usuário admin CRIADO!')
            self.stdout.write('   👤 Username: admin')
            self.stdout.write('   🔑 Password: admin123')
            self.stdout.write('   👑 Staff: True')
            self.stdout.write('   🔧 Superuser: True')
            self.stdout.write('   ✅ Ativo: True')
            
            # Testar login
            from django.contrib.auth import authenticate
            test_user = authenticate(username='admin', password='admin123')
            if test_user:
                self.stdout.write('✅ Login testado com SUCESSO!')
            else:
                self.stdout.write('❌ Login FALHOU!')
                
        except Exception as e:
            self.stdout.write(f'❌ Erro: {e}')
            import traceback
            self.stdout.write(f'   Traceback: {traceback.format_exc()}')
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('🏁 USUÁRIO ADMIN CRIADO!')
