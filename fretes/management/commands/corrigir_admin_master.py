from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from fretes.models import UserProfile

class Command(BaseCommand):
    help = 'Corrige o usuário admin para ser MASTER com acesso completo'

    def handle(self, *args, **options):
        self.stdout.write('👑 CORRIGINDO USUÁRIO ADMIN PARA MASTER...')
        self.stdout.write('=' * 50)
        
        try:
            # Buscar ou criar usuário admin
            admin_user, created = User.objects.get_or_create(
                username='admin',
                defaults={
                    'email': 'admin@portal.com',
                    'is_staff': True,
                    'is_superuser': True,
                    'is_active': True
                }
            )
            
            # Sempre garantir permissões corretas
            admin_user.set_password('admin123')
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.is_active = True
            admin_user.save()
            
            if created:
                self.stdout.write('✅ Usuário admin criado')
            else:
                self.stdout.write('✅ Usuário admin encontrado e atualizado')
            
            # Criar ou atualizar profile como MASTER
            profile, created = UserProfile.objects.get_or_create(
                user=admin_user,
                defaults={
                    'tipo_usuario': 'master',
                    'is_master': True,
                    'tipo_acesso': 'completo'
                }
            )
            
            # Sempre garantir que seja master
            profile.tipo_usuario = 'master'
            profile.is_master = True
            profile.tipo_acesso = 'completo'
            profile.save()
            
            if created:
                self.stdout.write('✅ Profile do admin criado como MASTER')
            else:
                self.stdout.write('✅ Profile do admin atualizado para MASTER')
            
            # Verificar permissões
            self.stdout.write(f'\n📋 VERIFICAÇÃO:')
            self.stdout.write(f'   - Username: {admin_user.username}')
            self.stdout.write(f'   - Email: {admin_user.email}')
            self.stdout.write(f'   - Is Staff: {admin_user.is_staff}')
            self.stdout.write(f'   - Is Superuser: {admin_user.is_superuser}')
            self.stdout.write(f'   - Is Active: {admin_user.is_active}')
            self.stdout.write(f'   - Tipo Usuário: {profile.tipo_usuario}')
            self.stdout.write(f'   - Is Master: {profile.is_master}')
            self.stdout.write(f'   - Tipo Acesso: {profile.tipo_acesso}')
            
            self.stdout.write(self.style.SUCCESS('\n🎉 USUÁRIO ADMIN CONFIGURADO COMO MASTER!'))
            self.stdout.write('🔑 Login: admin / admin123')
            self.stdout.write('👑 Acesso: MASTER (acesso completo a tudo)')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro: {e}'))
            import traceback
            self.stdout.write(traceback.format_exc())
        
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write('🏁 CORREÇÃO COMPLETA!')
