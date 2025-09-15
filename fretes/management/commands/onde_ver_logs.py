from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):
    help = 'Mostra onde encontrar os logs no Render'

    def handle(self, *args, **options):
        self.stdout.write('📋 COMO VER OS LOGS NO RENDER')
        self.stdout.write('=' * 80)
        
        self.stdout.write('\n🌐 PASSOS PARA VER OS LOGS:')
        self.stdout.write('1. Acesse: https://dashboard.render.com')
        self.stdout.write('2. Faça login na sua conta')
        self.stdout.write('3. Clique no serviço "portal-fretes"')
        self.stdout.write('4. Clique na aba "Logs" (ao lado de "Settings")')
        self.stdout.write('5. Procure pelos logs do comando "solucao_definitiva"')
        
        self.stdout.write('\n🔍 O QUE PROCURAR NOS LOGS:')
        self.stdout.write('- "SOLUÇÃO DEFINITIVA - PROBLEMA DE LOGIN"')
        self.stdout.write('- "Admin criado: admin / admin123"')
        self.stdout.write('- "Cochit0 criado: cochit0 / 123456"')
        self.stdout.write('- "admin / admin123: SUCESSO"')
        self.stdout.write('- "cochit0 / 123456: SUCESSO"')
        
        self.stdout.write('\n📱 ALTERNATIVA - LOGS VIA TERMINAL:')
        self.stdout.write('Se não conseguir ver no dashboard, me envie:')
        self.stdout.write('- Screenshot da tela de logs')
        self.stdout.write('- Ou copie e cole os logs aqui')
        
        self.stdout.write('\n🎯 CREDENCIAIS PARA TESTAR:')
        self.stdout.write('admin / admin123')
        self.stdout.write('cochit0 / 123456')
        
        self.stdout.write('\n' + '=' * 80)
        self.stdout.write('🏁 INSTRUÇÕES COMPLETAS!')
