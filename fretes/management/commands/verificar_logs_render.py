from django.core.management.base import BaseCommand
import os
import requests
import json

class Command(BaseCommand):
    help = 'Verifica logs do Render via API'

    def handle(self, *args, **options):
        self.stdout.write('📋 VERIFICANDO LOGS DO RENDER')
        self.stdout.write('=' * 60)
        
        # Verificar se temos API key do Render
        api_key = os.environ.get('RENDER_API_KEY')
        if not api_key:
            self.stdout.write('❌ RENDER_API_KEY não encontrada')
            self.stdout.write('   Para ver logs, acesse: https://dashboard.render.com')
            return
        
        try:
            # Headers para API do Render
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Accept': 'application/json'
            }
            
            # Tentar buscar logs do serviço
            service_id = os.environ.get('RENDER_SERVICE_ID', 'portal-fretes')
            url = f'https://api.render.com/v1/services/{service_id}/logs'
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                logs = response.json()
                self.stdout.write('✅ Logs obtidos com sucesso!')
                self.stdout.write(f'   Total de logs: {len(logs)}')
                
                # Mostrar últimos 10 logs
                for log in logs[-10:]:
                    self.stdout.write(f'   {log}')
            else:
                self.stdout.write(f'❌ Erro ao buscar logs: {response.status_code}')
                self.stdout.write(f'   Resposta: {response.text}')
                
        except Exception as e:
            self.stdout.write(f'❌ Erro ao conectar com API: {e}')
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('💡 Para ver logs completos, acesse:')
        self.stdout.write('   https://dashboard.render.com')
        self.stdout.write('   → Seu serviço → Aba "Logs"')
