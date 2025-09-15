from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from fretes.models import UserProfile

class Command(BaseCommand):
    help = 'Verificar e corrigir usuário gerente'

    def handle(self, *args, **options):
        self.stdout.write('🔍 VERIFICANDO USUÁRIOS GERENTE...')
        self.stdout.write('=' * 60)
        
        # Buscar todos os usuários gerente
        gerentes = UserProfile.objects.filter(tipo_usuario='gerente')
        
        if not gerentes.exists():
            self.stdout.write('❌ Nenhum usuário gerente encontrado!')
            return
        
        for profile in gerentes:
            user = profile.user
            self.stdout.write(f'\n👤 Usuário: {user.username}')
            self.stdout.write(f'   Email: {user.email}')
            self.stdout.write(f'   Tipo: {profile.tipo_usuario}')
            self.stdout.write(f'   is_master: {profile.is_master}')
            self.stdout.write(f'   is_staff: {user.is_staff}')
            self.stdout.write(f'   is_superuser: {user.is_superuser}')
            
            # Verificar se está correto
            if profile.is_master:
                self.stdout.write('   ⚠️ PROBLEMA: Gerente tem is_master=True!')
                profile.is_master = False
                profile.save()
                self.stdout.write('   ✅ CORRIGIDO: is_master definido como False')
            
            if user.is_staff or user.is_superuser:
                self.stdout.write('   ⚠️ PROBLEMA: Gerente tem permissões de admin!')
                user.is_staff = False
                user.is_superuser = False
                user.save()
                self.stdout.write('   ✅ CORRIGIDO: Permissões de admin removidas')
            
            self.stdout.write('   ✅ Usuário gerente configurado corretamente!')
        
        self.stdout.write('\n🎉 Verificação concluída!')
