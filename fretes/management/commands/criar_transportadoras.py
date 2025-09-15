from django.core.management.base import BaseCommand
from fretes.models import Transportadora


class Command(BaseCommand):
    help = 'Cria transportadoras no sistema'

    def add_arguments(self, parser):
        parser.add_argument('--nome', type=str, help='Nome da transportadora')
        parser.add_argument('--email', type=str, help='Email da transportadora')
        parser.add_argument('--lista', action='store_true', help='Lista todas as transportadoras')

    def handle(self, *args, **options):
        if options['lista']:
            self.listar_transportadoras()
        elif options['nome'] and options['email']:
            self.criar_transportadora(options['nome'], options['email'])
        else:
            self.criar_transportadoras_padrao()

    def listar_transportadoras(self):
        """Lista todas as transportadoras cadastradas"""
        transportadoras = Transportadora.objects.all().order_by('nome')
        
        if not transportadoras:
            self.stdout.write(self.style.WARNING('Nenhuma transportadora cadastrada'))
            return
        
        self.stdout.write(f'Transportadoras cadastradas ({transportadoras.count()}):')
        for t in transportadoras:
            self.stdout.write(f'  - {t.nome} ({t.email})')

    def criar_transportadora(self, nome, email):
        """Cria uma transportadora específica"""
        if Transportadora.objects.filter(nome=nome).exists():
            self.stdout.write(
                self.style.WARNING(f'❌ Transportadora {nome} já existe!')
            )
            return
        
        transportadora = Transportadora.objects.create(
            nome=nome,
            email=email
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Transportadora criada: {nome} ({email})')
        )

    def criar_transportadoras_padrao(self):
        """Cria as transportadoras padrão do sistema"""
        transportadoras = [
            'Log20',
            'Leão Log',
            'Soluciona',
            'Nika',
            'Rodo Flip'
        ]
        
        self.stdout.write('Criando transportadoras padrão...')
        
        for nome in transportadoras:
            if Transportadora.objects.filter(nome=nome).exists():
                self.stdout.write(f'✅ {nome} - já existe')
            else:
                email = f'{nome.lower().replace(" ", "").replace("ã", "a")}@transportadora.com'
                Transportadora.objects.create(nome=nome, email=email)
                self.stdout.write(f'✅ {nome} - criada')
        
        total = Transportadora.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f'🎯 Total de transportadoras: {total}')
        )

