from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from fretes.models import UserProfile, Transportadora, FreteRequest, Loja

class Command(BaseCommand):
    help = 'Mostra todos os dados do banco PostgreSQL'

    def handle(self, *args, **options):
        self.stdout.write('📊 DADOS DO BANCO POSTGRESQL')
        self.stdout.write('=' * 60)
        
        # Usuários
        self.stdout.write('\n👥 USUÁRIOS:')
        users = User.objects.all()
        for user in users:
            try:
                profile = user.userprofile
                self.stdout.write(f'   - {user.username} ({profile.tipo_usuario}) - {"Master" if profile.is_master else "Normal"}')
            except:
                self.stdout.write(f'   - {user.username} (sem perfil)')
        
        # Transportadoras
        self.stdout.write('\n🚛 TRANSPORTADORAS:')
        transportadoras = Transportadora.objects.all()
        for transportadora in transportadoras:
            self.stdout.write(f'   - {transportadora.nome} ({transportadora.email})')
        
        # Lojas
        self.stdout.write('\n🏪 LOJAS:')
        lojas = Loja.objects.all()
        self.stdout.write(f'   Total: {lojas.count()} lojas')
        for loja in lojas[:5]:  # Mostra apenas as primeiras 5
            self.stdout.write(f'   - {loja.nome} ({loja.municipio}/{loja.estado})')
        if lojas.count() > 5:
            self.stdout.write(f'   ... e mais {lojas.count() - 5} lojas')
        
        # Fretes
        self.stdout.write('\n📦 FRETES:')
        fretes = FreteRequest.objects.all()
        self.stdout.write(f'   Total: {fretes.count()} fretes')
        for frete in fretes[:3]:  # Mostra apenas os primeiros 3
            self.stdout.write(f'   - Frete #{frete.id} - {frete.usuario.username} - {frete.status}')
        if fretes.count() > 3:
            self.stdout.write(f'   ... e mais {fretes.count() - 3} fretes')
        
        # Estatísticas
        self.stdout.write('\n📈 ESTATÍSTICAS:')
        self.stdout.write(f'   - Usuários: {User.objects.count()}')
        self.stdout.write(f'   - Transportadoras: {Transportadora.objects.count()}')
        self.stdout.write(f'   - Lojas: {Loja.objects.count()}')
        self.stdout.write(f'   - Fretes: {FreteRequest.objects.count()}')
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('✅ Banco PostgreSQL funcionando perfeitamente!')
