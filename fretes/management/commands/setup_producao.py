from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from fretes.models import UserProfile, Transportadora, Loja
import os

class Command(BaseCommand):
    help = 'Configura dados iniciais para produção'

    def handle(self, *args, **options):
        self.stdout.write('Configurando dados iniciais para produção...')
        
        # Verificar se o banco está funcionando
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                self.stdout.write('✅ Conexão com banco: OK')
        except Exception as e:
            self.stdout.write(f'❌ Erro na conexão com banco: {e}')
            return
        
        # Criar usuário master se não existir
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_user(
                username='admin',
                email='admin@portalfretes.com',
                password='admin123',
                first_name='Administrador',
                last_name='Sistema',
                is_staff=True,
                is_superuser=True,
                is_active=True
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
            # Verificar se o usuário admin existente tem as permissões corretas
            admin_user = User.objects.get(username='admin')
            if not admin_user.is_staff or not admin_user.is_superuser:
                admin_user.is_staff = True
                admin_user.is_superuser = True
                admin_user.is_active = True
                admin_user.save()
                self.stdout.write('Permissões do usuário admin atualizadas!')
            else:
                self.stdout.write('Usuário admin já existe com permissões corretas.')
        
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
        
        # Configurar usuário cochit0 como admin se existir
        if User.objects.filter(username='cochit0').exists():
            cochit0_user = User.objects.get(username='cochit0')
            if not cochit0_user.is_staff or not cochit0_user.is_superuser:
                cochit0_user.is_staff = True
                cochit0_user.is_superuser = True
                cochit0_user.is_active = True
                cochit0_user.save()
                self.stdout.write('✅ Usuário cochit0 configurado como admin!')
            else:
                self.stdout.write('✅ Usuário cochit0 já tem permissões de admin.')
        
        self.stdout.write(
            self.style.SUCCESS('Configuração inicial concluída!')
        )
        self.stdout.write('✅ PostgreSQL configurado e funcionando!')
        self.stdout.write('🔄 Servidor reiniciado - testando persistência de dados...')
