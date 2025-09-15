from django.core.management.base import BaseCommand
from django.core.management import call_command
import os

class Command(BaseCommand):
    help = 'Comando de inicialização para deploy - executa apenas o necessário'

    def handle(self, *args, **options):
        self.stdout.write('🚀 INICIALIZAÇÃO DO DEPLOY')
        self.stdout.write('=' * 50)
        
        try:
            # 1. Executar migrações
            self.stdout.write('📊 Executando migrações...')
            call_command('migrate', verbosity=0, interactive=False)
            self.stdout.write('✅ Migrações executadas')
            
            # 2. Configurar sessões
            self.stdout.write('🔧 Configurando sessões...')
            try:
                call_command('setup_sessions', verbosity=0)
                self.stdout.write('✅ Sessões configuradas')
            except Exception as e:
                self.stdout.write(f'⚠️ Erro ao configurar sessões: {e}')
                # Tentar criar tabela de sessões manualmente
                from django.db import connection
                with connection.cursor() as cursor:
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS django_session (
                            session_key VARCHAR(40) NOT NULL PRIMARY KEY,
                            session_data TEXT NOT NULL,
                            expire_date TIMESTAMP WITH TIME ZONE NOT NULL
                        );
                    """)
                    cursor.execute("CREATE INDEX IF NOT EXISTS django_session_expire_date_idx ON django_session (expire_date);")
                self.stdout.write('✅ Tabela de sessões criada manualmente')
            
            # 3. Verificar se precisa de setup
            from django.contrib.auth.models import User
            from fretes.models import Loja, Transportadora
            
            if not (User.objects.filter(username='admin').exists() and 
                    Loja.objects.exists() and 
                    Transportadora.objects.exists()):
                
                self.stdout.write('🔧 Executando setup inicial...')
                call_command('setup_completo', verbosity=0)
                self.stdout.write('✅ Setup inicial executado')
            else:
                self.stdout.write('✅ Banco já configurado')
            
            # 4. Coletar arquivos estáticos (se não foi feito no build)
            if not os.path.exists('staticfiles'):
                self.stdout.write('📁 Coletando arquivos estáticos...')
                call_command('collectstatic', verbosity=0, interactive=False)
                self.stdout.write('✅ Arquivos estáticos coletados')
            
            self.stdout.write(self.style.SUCCESS('🎉 Inicialização concluída com sucesso!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro na inicialização: {e}'))
            # Não falhar o deploy por causa de erros de setup
            self.stdout.write('⚠️ Continuando com deploy mesmo com erros...')
