from django.core.management.base import BaseCommand
from fretes.models import CotacaoFrete, User, FreteRequest

class Command(BaseCommand):
    help = 'Cria uma cotação de teste para a transportadora'

    def handle(self, *args, **options):
        try:
            transportadora = User.objects.get(username='transportadora_teste')
            frete = FreteRequest.objects.filter(status='cotacao_enviada').first()
            
            if frete:
                cotacao = CotacaoFrete.objects.create(
                    frete=frete,
                    transportadora=transportadora,
                    status='pendente'
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Cotação criada: {cotacao.id} para frete {frete.id}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING('Nenhum frete disponível para cotação')
                )
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Usuário transportadora_teste não encontrado')
            )

