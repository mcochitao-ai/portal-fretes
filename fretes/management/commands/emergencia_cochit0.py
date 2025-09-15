from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from fretes.models import UserProfile

class Command(BaseCommand):
    help = 'EMERGÊNCIA: Força criação do usuário cochit0'

    def handle(self, *args, **options):
        self.stdout.write('🚨 MODO EMERGÊNCIA - Criando cochit0...')
        
        try:
            # Deletar usuário cochit0 se existir
            if User.objects.filter(username='cochit0').exists():
                User.objects.filter(username='cochit0').delete()
                self.stdout.write('🗑️ Usuário cochit0 antigo removido')
            
            # Criar usuário cochit0 do zero
            user = User.objects.create_user(
                username='cochit0',
                email='mcochitao@gmail.com',
                password='1357',
                first_name='Marcos',
                last_name='Cochitao',
                is_staff=True,
                is_superuser=True,
                is_active=True
            )
            
            # Criar perfil master
            UserProfile.objects.create(
                user=user,
                tipo_usuario='master',
                is_master=True,
                tipo_acesso='completo'
            )
            
            self.stdout.write('✅ Usuário cochit0 criado com sucesso!')
            self.stdout.write('   Username: cochit0')
            self.stdout.write('   Password: 1357')
            self.stdout.write('   Admin: SIM')
            self.stdout.write('   Master: SIM')
            
            # Verificar se foi criado corretamente
            user_check = User.objects.get(username='cochit0')
            self.stdout.write(f'   is_staff: {user_check.is_staff}')
            self.stdout.write(f'   is_superuser: {user_check.is_superuser}')
            self.stdout.write(f'   is_active: {user_check.is_active}')
            
        except Exception as e:
            self.stdout.write(f'❌ ERRO: {e}')
        
        self.stdout.write('\n🎯 Comando de emergência finalizado!')
