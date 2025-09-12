from django.core.management.base import BaseCommand
from django.db import transaction
from fretes.models import FreteRequest, Destino, CotacaoFrete
from django.contrib.auth.models import User
from django.conf import settings


class Command(BaseCommand):
    help = 'Limpa dados de produção no Render (apenas fretes, mantém usuários)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm-producao',
            action='store_true',
            help='Confirma a operação de limpeza em produção',
        )

    def handle(self, *args, **options):
        # Verificar se está em produção
        if not settings.DEBUG:
            self.stdout.write(
                self.style.WARNING(
                    '🌐 Executando em ambiente de PRODUÇÃO'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    '⚠️  ATENÇÃO: Este comando é para PRODUÇÃO!'
                )
            )

        if not options['confirm_producao']:
            self.stdout.write(
                self.style.ERROR(
                    '❌ ERRO: Use --confirm-producao para executar em produção!\n'
                    'Este comando irá remover TODOS os fretes do ambiente de produção.'
                )
            )
            return

        with transaction.atomic():
            # Contar registros antes da limpeza
            total_fretes = FreteRequest.objects.count()
            total_destinos = Destino.objects.count()
            total_cotacoes = CotacaoFrete.objects.count()
            total_usuarios = User.objects.count()

            self.stdout.write(f'📊 Dados atuais em produção:')
            self.stdout.write(f'   - Fretes: {total_fretes}')
            self.stdout.write(f'   - Destinos: {total_destinos}')
            self.stdout.write(f'   - Cotações: {total_cotacoes}')
            self.stdout.write(f'   - Usuários: {total_usuarios}')

            if total_fretes == 0:
                self.stdout.write(
                    self.style.SUCCESS(
                        '✅ Banco de produção já está limpo!'
                    )
                )
                return

            # Limpar cotações primeiro (devido às foreign keys)
            self.stdout.write('\n🗑️  Removendo cotações de produção...')
            cotacoes_removidas = CotacaoFrete.objects.count()
            CotacaoFrete.objects.all().delete()
            self.stdout.write(f'   ✅ {cotacoes_removidas} cotações removidas')

            # Limpar destinos
            self.stdout.write('🗑️  Removendo destinos de produção...')
            destinos_removidos = Destino.objects.count()
            Destino.objects.all().delete()
            self.stdout.write(f'   ✅ {destinos_removidos} destinos removidos')

            # Limpar fretes
            self.stdout.write('🗑️  Removendo fretes de produção...')
            fretes_removidos = FreteRequest.objects.count()
            FreteRequest.objects.all().delete()
            self.stdout.write(f'   ✅ {fretes_removidos} fretes removidos')

            # Manter usuários (nunca remover em produção)
            self.stdout.write('👥 Usuários mantidos em produção')

        # Verificar limpeza
        fretes_restantes = FreteRequest.objects.count()
        destinos_restantes = Destino.objects.count()
        cotacoes_restantes = CotacaoFrete.objects.count()
        usuarios_restantes = User.objects.count()

        self.stdout.write(f'\n✅ Limpeza de produção concluída!')
        self.stdout.write(f'📊 Dados restantes em produção:')
        self.stdout.write(f'   - Fretes: {fretes_restantes}')
        self.stdout.write(f'   - Destinos: {destinos_restantes}')
        self.stdout.write(f'   - Cotações: {cotacoes_restantes}')
        self.stdout.write(f'   - Usuários: {usuarios_restantes}')

        if fretes_restantes == 0 and destinos_restantes == 0 and cotacoes_restantes == 0:
            self.stdout.write(
                self.style.SUCCESS(
                    '\n🎉 Banco de produção limpo com sucesso! '
                    'Ambiente de produção pronto para demonstrações.'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    '\n⚠️  Ainda existem dados no banco de produção. '
                    'Verifique se há algum problema.'
                )
            )
