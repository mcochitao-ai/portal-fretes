from django.core.management.base import BaseCommand
from django.db import transaction
from fretes.models import FreteRequest, Destino, CotacaoFrete
from django.contrib.auth.models import User
from django.utils import timezone


class Command(BaseCommand):
    help = 'Limpa todos os fretes, destinos e cotações do banco de dados'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirma a operação de limpeza',
        )
        parser.add_argument(
            '--manter-usuarios',
            action='store_true',
            help='Mantém os usuários, remove apenas fretes e cotações',
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(
                self.style.WARNING(
                    '⚠️  ATENÇÃO: Esta operação irá remover TODOS os dados de fretes!\n'
                    'Use --confirm para executar a limpeza.\n'
                    'Use --manter-usuarios para manter apenas os usuários.'
                )
            )
            return

        with transaction.atomic():
            # Contar registros antes da limpeza
            total_fretes = FreteRequest.objects.count()
            total_destinos = Destino.objects.count()
            total_cotacoes = CotacaoFrete.objects.count()
            total_usuarios = User.objects.count()

            self.stdout.write(f'📊 Dados atuais:')
            self.stdout.write(f'   - Fretes: {total_fretes}')
            self.stdout.write(f'   - Destinos: {total_destinos}')
            self.stdout.write(f'   - Cotações: {total_cotacoes}')
            self.stdout.write(f'   - Usuários: {total_usuarios}')

            # Limpar cotações primeiro (devido às foreign keys)
            self.stdout.write('\n🗑️  Removendo cotações...')
            cotacoes_removidas = CotacaoFrete.objects.count()
            CotacaoFrete.objects.all().delete()
            self.stdout.write(f'   ✅ {cotacoes_removidas} cotações removidas')

            # Limpar destinos
            self.stdout.write('🗑️  Removendo destinos...')
            destinos_removidos = Destino.objects.count()
            Destino.objects.all().delete()
            self.stdout.write(f'   ✅ {destinos_removidos} destinos removidos')

            # Limpar fretes
            self.stdout.write('🗑️  Removendo fretes...')
            fretes_removidos = FreteRequest.objects.count()
            FreteRequest.objects.all().delete()
            self.stdout.write(f'   ✅ {fretes_removidos} fretes removidos')

            # Opcional: remover usuários (exceto superuser)
            if not options['manter_usuarios']:
                self.stdout.write('🗑️  Removendo usuários (exceto superuser)...')
                usuarios_removidos = User.objects.exclude(is_superuser=True).count()
                User.objects.exclude(is_superuser=True).delete()
                self.stdout.write(f'   ✅ {usuarios_removidos} usuários removidos')
            else:
                self.stdout.write('👥 Usuários mantidos conforme solicitado')

            # Resetar sequências do banco (para PostgreSQL)
            from django.db import connection
            with connection.cursor() as cursor:
                try:
                    cursor.execute("SELECT setval(pg_get_serial_sequence('fretes_freterequest', 'id'), 1, false);")
                    cursor.execute("SELECT setval(pg_get_serial_sequence('fretes_destino', 'id'), 1, false);")
                    cursor.execute("SELECT setval(pg_get_serial_sequence('fretes_cotacaofrete', 'id'), 1, false);")
                    self.stdout.write('   ✅ Sequências do banco resetadas')
                except Exception as e:
                    # Para SQLite, não é necessário resetar sequências
                    self.stdout.write('   ℹ️  Sequências não resetadas (SQLite)')

        # Verificar limpeza
        fretes_restantes = FreteRequest.objects.count()
        destinos_restantes = Destino.objects.count()
        cotacoes_restantes = CotacaoFrete.objects.count()
        usuarios_restantes = User.objects.count()

        self.stdout.write(f'\n✅ Limpeza concluída!')
        self.stdout.write(f'📊 Dados restantes:')
        self.stdout.write(f'   - Fretes: {fretes_restantes}')
        self.stdout.write(f'   - Destinos: {destinos_restantes}')
        self.stdout.write(f'   - Cotações: {cotacoes_restantes}')
        self.stdout.write(f'   - Usuários: {usuarios_restantes}')

        if fretes_restantes == 0 and destinos_restantes == 0 and cotacoes_restantes == 0:
            self.stdout.write(
                self.style.SUCCESS(
                    '\n🎉 Banco de dados limpo com sucesso! '
                    'Agora você pode começar com dados frescos.'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    '\n⚠️  Ainda existem dados no banco. '
                    'Verifique se há algum problema.'
                )
            )
