from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from fretes.models import Loja, Transportadora, UserProfile

class Command(BaseCommand):
    help = 'Verifica se o banco está configurado corretamente'

    def handle(self, *args, **options):
        try:
            # Verificar se existe usuário admin
            admin_exists = User.objects.filter(username='admin').exists()
            self.stdout.write(f'👤 Usuário admin: {"✅ Existe" if admin_exists else "❌ Não existe"}')
            
            # Verificar se existem lojas
            lojas_count = Loja.objects.count()
            self.stdout.write(f'🏪 Lojas: {"✅" if lojas_count > 0 else "❌"} {lojas_count} encontradas')
            
            # Verificar se existem transportadoras
            transportadoras_count = Transportadora.objects.count()
            self.stdout.write(f'🚛 Transportadoras: {"✅" if transportadoras_count > 0 else "❌"} {transportadoras_count} encontradas')
            
            # Verificar se admin tem profile
            if admin_exists:
                admin = User.objects.get(username='admin')
                profile_exists = UserProfile.objects.filter(user=admin).exists()
                self.stdout.write(f'👤 Profile do admin: {"✅ Existe" if profile_exists else "❌ Não existe"}')
            
            # Resumo
            if admin_exists and lojas_count > 0 and transportadoras_count > 0:
                self.stdout.write(self.style.SUCCESS('🎉 Banco configurado corretamente!'))
                return True
            else:
                self.stdout.write(self.style.WARNING('⚠️ Banco precisa ser configurado'))
                return False
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro ao verificar banco: {e}'))
            return False