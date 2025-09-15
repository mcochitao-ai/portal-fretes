from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Configura tabelas de sessão no banco de dados'

    def handle(self, *args, **options):
        self.stdout.write('🔧 Configurando tabelas de sessão...')
        
        try:
            # Executar migrações para criar tabela django_session
            call_command('migrate', verbosity=0, interactive=False)
            self.stdout.write('✅ Tabelas de sessão configuradas')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro ao configurar sessões: {e}'))
