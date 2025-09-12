from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from fretes.models import Transportadora, UserProfile


class Command(BaseCommand):
    help = 'Cria usuários para as transportadoras existentes'

    def handle(self, *args, **options):
        transportadoras = Transportadora.objects.all()
        
        self.stdout.write(f'Criando usuários para {transportadoras.count()} transportadoras...')
        
        for transportadora in transportadoras:
            # Criar username baseado no nome da transportadora
            username = transportadora.nome.lower().replace(' ', '_').replace('ã', 'a')
            
            # Verificar se usuário já existe
            if User.objects.filter(username=username).exists():
                self.stdout.write(f'✅ {transportadora.nome} - usuário {username} já existe')
                continue
            
            # Criar usuário
            user = User.objects.create_user(
                username=username,
                email=transportadora.email,
                password='123456',  # Senha padrão
                first_name=transportadora.nome,
                last_name='Transportadora'
            )
            
            # Configurar perfil como transportadora
            profile = user.userprofile
            profile.tipo_usuario = 'transportadora'
            profile.tipo_acesso = 'limitado'
            profile.is_master = False
            profile.transportadora = transportadora  # Vincular à transportadora
            profile.save()
            
            self.stdout.write(f'✅ {transportadora.nome} - usuário {username} criado')
        
        self.stdout.write(
            self.style.SUCCESS(f'🎯 Usuários criados para todas as transportadoras!')
        )
        self.stdout.write(
            self.style.SUCCESS(f'🔑 Senha padrão: 123456')
        )
