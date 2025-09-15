from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from fretes.models import UserProfile, Transportadora

class Command(BaseCommand):
    help = 'Cria usuário admin com senha admin123'

    def handle(self, *args, **options):
        self.stdout.write('=== CRIANDO USUÁRIO ADMIN ===')
        
        # Verifica se já existe
        if User.objects.filter(username='admin').exists():
            self.stdout.write(self.style.WARNING('Usuário admin já existe!'))
            admin_user = User.objects.get(username='admin')
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write('Senha do admin foi resetada para: admin123')
        else:
            # Cria usuário admin
            admin_user = User.objects.create_user(
                username='admin',
                email='admin@portal.com',
                password='admin123',
                is_staff=True,
                is_superuser=True,
                is_active=True
            )
            self.stdout.write(self.style.SUCCESS('✅ Usuário admin criado!'))
            self.stdout.write('   Username: admin')
            self.stdout.write('   Senha: admin123')
        
        # Cria ou atualiza profile
        profile, created = UserProfile.objects.get_or_create(
            user=admin_user,
            defaults={
                'tipo_usuario': 'gerente',
                'is_master': True
            }
        )
        
        if created:
            self.stdout.write('✅ Profile do admin criado!')
        else:
            self.stdout.write('✅ Profile do admin já existia!')
        
        self.stdout.write('\n🎉 LOGIN DISPONÍVEL:')
        self.stdout.write('   URL: https://portal-fretes.onrender.com/login/')
        self.stdout.write('   Username: admin')
        self.stdout.write('   Senha: admin123')
