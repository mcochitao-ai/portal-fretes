from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from fretes.models import UserProfile


class Command(BaseCommand):
    help = 'Configura permissões de usuários (limitado ou completo)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--usuario',
            type=str,
            help='Nome do usuário para configurar permissões'
        )
        parser.add_argument(
            '--tipo',
            type=str,
            choices=['limitado', 'completo', 'master'],
            help='Tipo de acesso: limitado, completo ou master'
        )
        parser.add_argument(
            '--master',
            action='store_true',
            help='Tornar usuário master (pode ver todos os fretes)'
        )
        parser.add_argument(
            '--listar',
            action='store_true',
            help='Lista todos os usuários e seus tipos de acesso'
        )

    def handle(self, *args, **options):
        if options['listar']:
            self.listar_usuarios()
            return

        if not options['usuario'] or not options['tipo']:
            self.stdout.write(
                self.style.ERROR('❌ É necessário fornecer --usuario e --tipo ou usar --listar')
            )
            return

        username = options['usuario']
        tipo_acesso = options['tipo']
        is_master = options['master']

        try:
            user = User.objects.get(username=username)
            
            # Criar ou atualizar o perfil
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={'tipo_acesso': tipo_acesso, 'is_master': is_master}
            )
            
            if not created:
                profile.tipo_acesso = tipo_acesso
                profile.is_master = is_master
                profile.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Permissões configuradas para {username}: {tipo_acesso}'
                )
            )
            
            # Mostrar o que o usuário pode fazer
            if is_master:
                self.stdout.write(
                    self.style.SUCCESS(
                        '   🏆 Usuário Master: Pode ver todos os fretes de todos os usuários'
                    )
                )
            elif tipo_acesso == 'limitado':
                self.stdout.write(
                    self.style.WARNING(
                        '   📋 Acesso Limitado: Pode apenas solicitar fretes e ver lista'
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        '   🔧 Acesso Completo: Pode solicitar, editar e ver detalhes dos fretes'
                    )
                )
                
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'❌ Usuário "{username}" não encontrado!')
            )

    def listar_usuarios(self):
        self.stdout.write(self.style.SUCCESS('📋 Lista de Usuários e Permissões:'))
        self.stdout.write('=' * 50)
        
        users = User.objects.all().order_by('username')
        
        for user in users:
            try:
                profile = user.userprofile
                tipo = profile.get_tipo_acesso_display()
                if profile.is_master:
                    icon = '🏆'
                    style = self.style.SUCCESS
                    tipo += ' (Master)'
                elif profile.tipo_acesso == 'completo':
                    icon = '🔧'
                    style = self.style.SUCCESS
                else:
                    icon = '📋'
                    style = self.style.WARNING
            except UserProfile.DoesNotExist:
                tipo = 'Não configurado'
                icon = '❓'
                style = self.style.ERROR
            
            self.stdout.write(
                style(f'{icon} {user.username:<20} - {tipo}')
            )
        
        self.stdout.write('=' * 50)
        self.stdout.write(
            self.style.SUCCESS(
                '\n💡 Use: python manage.py configurar_permissoes --usuario NOME --tipo TIPO'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                '   TIPOS: limitado (apenas solicitar/ver lista) ou completo (editar/ver detalhes)'
            )
        )
