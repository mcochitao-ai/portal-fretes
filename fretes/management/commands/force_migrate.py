from django.core.management.base import BaseCommand
from django.db import connection
import os


class Command(BaseCommand):
    help = 'Força a execução das migrações no Render'

    def handle(self, *args, **options):
        self.stdout.write('🔧 Executando migrações forçadas...')
        
        try:
            # Verificar se as tabelas existem
            with connection.cursor() as cursor:
                # Verificar se a tabela AgendamentoFrete existe
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'fretes_agendamentofrete'
                    );
                """)
                agendamento_exists = cursor.fetchone()[0]
                
                # Verificar se a tabela TrackingFrete existe
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'fretes_trackingfrete'
                    );
                """)
                tracking_exists = cursor.fetchone()[0]
                
                self.stdout.write(f'AgendamentoFrete existe: {agendamento_exists}')
                self.stdout.write(f'TrackingFrete existe: {tracking_exists}')
                
                if not agendamento_exists or not tracking_exists:
                    self.stdout.write('⚠️ Tabelas não existem. Executando migrações...')
                    
                    # Executar migrações específicas
                    from django.core.management import call_command
                    call_command('migrate', 'fretes', '0027', verbosity=2)
                    
                    self.stdout.write('✅ Migrações executadas com sucesso!')
                else:
                    self.stdout.write('✅ Todas as tabelas já existem!')
                    
        except Exception as e:
            self.stdout.write(f'❌ Erro ao executar migrações: {str(e)}')
            raise
