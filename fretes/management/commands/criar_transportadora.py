from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from fretes.models import UserProfile

class Command(BaseCommand):
    help = 'Cria um usuário transportadora para testes'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Nome de usuário da transportadora')
        parser.add_argument('email', type=str, help='Email da transportadora')
        parser.add_argument('password', type=str, help='Senha da transportadora')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']
        
        # Criar usuário
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': username,
                'is_active': True
            }
        )
        
        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'Usuário {username} criado com sucesso!')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Usuário {username} já existe!')
            )
        
        # Criar ou atualizar perfil
        profile, profile_created = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'tipo_usuario': 'transportadora',
                'tipo_acesso': 'completo',
                'is_master': False
            }
        )
        
        if not profile_created:
            profile.tipo_usuario = 'transportadora'
            profile.save()
            self.stdout.write(
                self.style.SUCCESS(f'Perfil de {username} atualizado para transportadora!')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Perfil de transportadora criado para {username}!')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Transportadora {username} configurada com sucesso!')
        )


