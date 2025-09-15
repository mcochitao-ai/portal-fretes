from django.core.management.base import BaseCommand
import os
import requests

class Command(BaseCommand):
    help = 'Verifica status do deploy no Render'

    def handle(self, *args, **options):
        self.stdout.write('🚀 VERIFICANDO STATUS DO DEPLOY')
        self.stdout.write('=' * 60)
        
        # Verificar se estamos no Render
        if os.environ.get('RENDER'):
            self.stdout.write('✅ Executando no Render')
            self.stdout.write(f'   RENDER: {os.environ.get("RENDER")}')
            self.stdout.write(f'   PORT: {os.environ.get("PORT")}')
        else:
            self.stdout.write('❌ NÃO está no Render')
        
        # Verificar se o site está respondendo
        try:
            response = requests.get('https://portal-fretes.onrender.com', timeout=10)
            self.stdout.write(f'✅ Site respondendo: {response.status_code}')
        except Exception as e:
            self.stdout.write(f'❌ Site não responde: {e}')
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('🏁 VERIFICAÇÃO COMPLETA!')
