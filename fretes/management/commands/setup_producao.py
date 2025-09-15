from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from fretes.models import UserProfile, Transportadora, Loja
import os

class Command(BaseCommand):
    help = 'Configura dados iniciais para produção'

    def handle(self, *args, **options):
        self.stdout.write('Configurando dados iniciais para produção...')
        
        # Criar usuário master se não existir
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_user(
                username='admin',
                email='admin@portalfretes.com',
                password='admin123',
                first_name='Administrador',
                last_name='Sistema',
                is_staff=True,
                is_superuser=True
            )
            
            # Criar perfil master
            UserProfile.objects.create(
                user=admin_user,
                tipo_usuario='master',
                is_master=True,
                tipo_acesso='completo'
            )
            
            self.stdout.write(
                self.style.SUCCESS('Usuário admin criado com sucesso!')
            )
            self.stdout.write('Username: admin')
            self.stdout.write('Password: admin123')
        else:
            self.stdout.write('Usuário admin já existe.')
        
        # Criar transportadoras básicas se não existirem
        transportadoras_data = [
            {'nome': 'Transportadora ABC', 'email': 'contato@abc.com'},
            {'nome': 'Logística XYZ', 'email': 'contato@xyz.com'},
            {'nome': 'Frete Express', 'email': 'contato@express.com'},
        ]
        
        for data in transportadoras_data:
            transportadora, created = Transportadora.objects.get_or_create(
                nome=data['nome'],
                defaults={'email': data['email']}
            )
            if created:
                self.stdout.write(f'Transportadora {data["nome"]} criada.')
        
        # Verificar se há lojas
        if not Loja.objects.exists():
            self.stdout.write(
                self.style.WARNING('Nenhuma loja encontrada. Execute o comando import_lojas.py para importar as lojas.')
            )
        
        self.stdout.write(
            self.style.SUCCESS('Configuração inicial concluída!')
        )
