from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Garante que o usuário cochit0 existe e tem senha'

    def handle(self, *args, **options):
        self.stdout.write('🔧 GARANTINDO USUÁRIO COCHIT0')
        self.stdout.write('=' * 60)
        
        try:
            # Buscar ou criar usuário cochit0
            user, created = User.objects.get_or_create(
                username='cochit0',
                defaults={
                    'email': 'cochit0@portal.com',
                    'is_staff': True,
                    'is_superuser': True,
                    'is_active': True,
                }
            )
            
            if created:
                self.stdout.write('✅ Usuário cochit0 CRIADO!')
            else:
                self.stdout.write('✅ Usuário cochit0 já existe!')
            
            # Garantir que tem senha
            user.set_password('123456')
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.save()
            
            self.stdout.write('🔑 Senha definida: 123456')
            self.stdout.write('👑 Staff: True')
            self.stdout.write('🔧 Superuser: True')
            self.stdout.write('✅ Ativo: True')
            
            # Testar login
            from django.contrib.auth import authenticate
            test_user = authenticate(username='cochit0', password='123456')
            if test_user:
                self.stdout.write('✅ Login testado com SUCESSO!')
            else:
                self.stdout.write('❌ Login FALHOU!')
                
        except Exception as e:
            self.stdout.write(f'❌ Erro: {e}')
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('🏁 USUÁRIO COCHIT0 CONFIGURADO!')
