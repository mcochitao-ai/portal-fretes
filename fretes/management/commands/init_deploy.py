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
            call_command('setup_sessions', verbosity=0)
            self.stdout.write('✅ Sessões configuradas')
            
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
