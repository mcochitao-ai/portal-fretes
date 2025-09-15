from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Cria usuário admin simples'

    def handle(self, *args, **options):
        self.stdout.write('🔧 CRIANDO USUÁRIO ADMIN SIMPLES...')
        
        # Deletar se existir
        if User.objects.filter(username='admin').exists():
            User.objects.filter(username='admin').delete()
            self.stdout.write('Usuário admin antigo removido')
        
        # Criar usuário admin
        User.objects.create_superuser(
            username='admin',
            email='admin@admin.com',
            password='admin123'
        )
        
        self.stdout.write('✅ Usuário admin criado!')
        self.stdout.write('Username: admin')
        self.stdout.write('Password: admin123')
        
        # Verificar se foi criado
        user = User.objects.get(username='admin')
        self.stdout.write(f'ID: {user.id}')
        self.stdout.write(f'is_staff: {user.is_staff}')
        self.stdout.write(f'is_superuser: {user.is_superuser}')
        self.stdout.write(f'is_active: {user.is_active}')
        
        self.stdout.write('🎯 USUÁRIO ADMIN CRIADO COM SUCESSO!')
