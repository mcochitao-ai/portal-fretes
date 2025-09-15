from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from fretes.models import UserProfile

class Command(BaseCommand):
    help = 'Configura o usuário cochit0 como admin do Django Admin'

    def handle(self, *args, **options):
        self.stdout.write('🔧 Configurando usuário cochit0 como admin...')
        
        try:
            # Buscar o usuário cochit0
            user = User.objects.get(username='cochit0')
            
            # Configurar permissões de admin
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.save()
            
            # Verificar se tem perfil
            try:
                profile = user.userprofile
                profile.tipo_usuario = 'master'
                profile.is_master = True
                profile.tipo_acesso = 'completo'
                profile.save()
            except UserProfile.DoesNotExist:
                # Criar perfil se não existir
                UserProfile.objects.create(
                    user=user,
                    tipo_usuario='master',
                    is_master=True,
                    tipo_acesso='completo'
                )
            
            self.stdout.write(
                self.style.SUCCESS('✅ Usuário cochit0 configurado como admin!')
            )
            self.stdout.write('🔑 Credenciais para Django Admin:')
            self.stdout.write(f'   Username: cochit0')
            self.stdout.write(f'   Password: (sua senha atual)')
            self.stdout.write('')
            self.stdout.write('🌐 Acesse: https://portal-fretes.onrender.com/admin/')
            
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('❌ Usuário cochit0 não encontrado!')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erro ao configurar usuário: {e}')
            )
