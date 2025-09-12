from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from fretes.models import UserProfile


class Command(BaseCommand):
    help = 'Corrige permissões de usuários gerentes para garantir que vejam apenas Aprovar Cotações'

    def handle(self, *args, **options):
        # Buscar todos os usuários gerentes
        gerentes = User.objects.filter(userprofile__tipo_usuario='gerente')
        
        self.stdout.write(f'Encontrados {gerentes.count()} usuários gerentes')
        
        for user in gerentes:
            profile = user.userprofile
            
            # Verificar se precisa correção
            if profile.is_master:
                profile.is_master = False
                profile.save()
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Corrigido {user.username}: is_master alterado para False')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f'✅ OK {user.username}: permissões já estão corretas')
                )
        
        self.stdout.write(
            self.style.SUCCESS('🎯 Todos os usuários gerentes agora veem apenas "Aprovar Cotações"')
        )
