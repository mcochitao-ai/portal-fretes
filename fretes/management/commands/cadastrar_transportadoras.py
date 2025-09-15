from django.core.management.base import BaseCommand
from fretes.models import Transportadora

class Command(BaseCommand):
    help = 'Cadastra transportadoras para teste'

    def handle(self, *args, **options):
        self.stdout.write('🚛 CADASTRANDO TRANSPORTADORAS...')
        self.stdout.write('=' * 50)
        
        # Lista de transportadoras para cadastrar
        transportadoras_data = [
            {'nome': 'Log20', 'email': 'log20@lojasrenner.com.br'},
            {'nome': 'Soluciona', 'email': 'soluciona@lojasrenner.com.br'},
            {'nome': 'Leão Log', 'email': 'leaolog@lojasrenner.com.br'},
        ]
        
        cadastradas = 0
        existentes = 0
        
        for data in transportadoras_data:
            transportadora, created = Transportadora.objects.get_or_create(
                nome=data['nome'],
                defaults={'email': data['email']}
            )
            
            if created:
                cadastradas += 1
                self.stdout.write(f'✅ Transportadora {transportadora.nome} cadastrada')
                self.stdout.write(f'   Email: {transportadora.email}')
            else:
                existentes += 1
                self.stdout.write(f'🔄 Transportadora {transportadora.nome} já existia')
                # Atualizar email se necessário
                if transportadora.email != data['email']:
                    transportadora.email = data['email']
                    transportadora.save()
                    self.stdout.write(f'   Email atualizado para: {transportadora.email}')
        
        self.stdout.write(f'\n📈 RESUMO:')
        self.stdout.write(f'   - Transportadoras cadastradas: {cadastradas}')
        self.stdout.write(f'   - Transportadoras já existentes: {existentes}')
        self.stdout.write(f'   - Total no banco: {Transportadora.objects.count()}')
        
        # Mostrar todas as transportadoras
        self.stdout.write(f'\n📋 TRANSPORTADORAS DISPONÍVEIS:')
        transportadoras = Transportadora.objects.all()
        for transportadora in transportadoras:
            self.stdout.write(f'   - {transportadora.nome} ({transportadora.email})')
        
        if cadastradas > 0:
            self.stdout.write(self.style.SUCCESS('🎉 Transportadoras cadastradas com sucesso!'))
        else:
            self.stdout.write(self.style.WARNING('⚠️ Todas as transportadoras já existiam'))
        
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write('🏁 CADASTRO COMPLETO!')
