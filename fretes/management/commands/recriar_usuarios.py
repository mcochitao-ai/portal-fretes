from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from fretes.models import UserProfile, Transportadora
from django.db import transaction

class Command(BaseCommand):
    help = 'Recria usuários e transportadoras que existiam antes'

    def handle(self, *args, **options):
        self.stdout.write('🔄 Recriando usuários e transportadoras...')
        self.stdout.write('=' * 60)
        
        with transaction.atomic():
            # Criar usuário cochit0 (master)
            if not User.objects.filter(username='cochit0').exists():
                cochit0_user = User.objects.create_user(
                    username='cochit0',
                    email='mcochitao@gmail.com',
                    password='1357',
                    first_name='Marcos',
                    last_name='Cochitao',
                    is_staff=True,
                    is_superuser=True,
                    is_active=True
                )
                
                UserProfile.objects.create(
                    user=cochit0_user,
                    tipo_usuario='master',
                    is_master=True,
                    tipo_acesso='completo'
                )
                self.stdout.write('✅ Usuário cochit0 criado (master)')
            else:
                self.stdout.write('✅ Usuário cochit0 já existe')
            
            # Criar usuário teste_solicitador
            if not User.objects.filter(username='teste_solicitador').exists():
                teste_user = User.objects.create_user(
                    username='teste_solicitador',
                    email='teste@portalfretes.com',
                    password='1357',
                    first_name='Teste',
                    last_name='Solicitador',
                    is_active=True
                )
                
                UserProfile.objects.create(
                    user=teste_user,
                    tipo_usuario='solicitador',
                    is_master=False,
                    tipo_acesso='limitado'
                )
                self.stdout.write('✅ Usuário teste_solicitador criado')
            else:
                self.stdout.write('✅ Usuário teste_solicitador já existe')
            
            # Criar transportadoras
            transportadoras_data = [
                {
                    'nome': 'Transportadora ABC',
                    'email': 'contato@abc.com'
                },
                {
                    'nome': 'Logística XYZ',
                    'email': 'contato@xyz.com'
                },
                {
                    'nome': 'Frete Express',
                    'email': 'contato@express.com'
                },
                {
                    'nome': 'Transportadora Rápida',
                    'email': 'contato@rapida.com'
                }
            ]
            
            for data in transportadoras_data:
                transportadora, created = Transportadora.objects.get_or_create(
                    nome=data['nome'],
                    defaults={
                        'email': data['email']
                    }
                )
                if created:
                    self.stdout.write(f'✅ Transportadora {data["nome"]} criada')
                else:
                    self.stdout.write(f'✅ Transportadora {data["nome"]} já existe')
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('🎉 Usuários e transportadoras recriados com sucesso!')
        self.stdout.write('\n📋 Usuários disponíveis:')
        self.stdout.write('   - cochit0 (master) - senha: 1357')
        self.stdout.write('   - teste_solicitador - senha: 1357')
        self.stdout.write('   - admin (admin) - senha: admin123')
        self.stdout.write('\n🚛 Transportadoras criadas:')
        for transportadora in Transportadora.objects.all():
            self.stdout.write(f'   - {transportadora.nome}')
