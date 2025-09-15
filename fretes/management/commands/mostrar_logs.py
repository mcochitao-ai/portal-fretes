from django.core.management.base import BaseCommand
import os
import sys

class Command(BaseCommand):
    help = 'Mostra logs do sistema'

    def handle(self, *args, **options):
        self.stdout.write('📋 LOGS DO SISTEMA')
        self.stdout.write('=' * 60)
        
        # 1. Verificar se estamos no Render
        self.stdout.write('\n🌍 AMBIENTE:')
        if os.environ.get('RENDER'):
            self.stdout.write('   ✅ Executando no Render')
        else:
            self.stdout.write('   ❌ NÃO está no Render')
        
        # 2. Verificar variáveis de ambiente
        self.stdout.write('\n🔧 VARIÁVEIS DE AMBIENTE:')
        env_vars = ['RENDER', 'PORT', 'PYTHON_VERSION', 'SECRET_KEY', 'DEBUG', 'ALLOWED_HOSTS']
        for var in env_vars:
            value = os.environ.get(var, 'NÃO DEFINIDA')
            if var == 'SECRET_KEY' and value != 'NÃO DEFINIDA':
                value = f'{value[:10]}...'
            self.stdout.write(f'   {var}: {value}')
        
        # 3. Verificar diretório atual
        self.stdout.write('\n📁 DIRETÓRIO ATUAL:')
        self.stdout.write(f'   {os.getcwd()}')
        
        # 4. Verificar arquivos importantes
        self.stdout.write('\n📄 ARQUIVOS IMPORTANTES:')
        important_files = ['manage.py', 'requirements.txt', 'render.yaml']
        for file in important_files:
            if os.path.exists(file):
                self.stdout.write(f'   ✅ {file}')
            else:
                self.stdout.write(f'   ❌ {file} não encontrado')
        
        # 5. Verificar se Django está funcionando
        self.stdout.write('\n🐍 DJANGO:')
        try:
            import django
            self.stdout.write(f'   Versão: {django.get_version()}')
            self.stdout.write('   ✅ Django importado com sucesso')
        except Exception as e:
            self.stdout.write(f'   ❌ Erro ao importar Django: {e}')
        
        # 6. Verificar configurações
        self.stdout.write('\n⚙️ CONFIGURAÇÕES:')
        try:
            from django.conf import settings
            self.stdout.write(f'   DEBUG: {settings.DEBUG}')
            self.stdout.write(f'   ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}')
            self.stdout.write(f'   DATABASE: {settings.DATABASES["default"]["ENGINE"]}')
        except Exception as e:
            self.stdout.write(f'   ❌ Erro ao verificar configurações: {e}')
        
        # 7. Verificar se o servidor está rodando
        self.stdout.write('\n🚀 SERVIDOR:')
        try:
            from django.core.management import execute_from_command_line
            self.stdout.write('   ✅ Django management funcionando')
        except Exception as e:
            self.stdout.write(f'   ❌ Erro no Django management: {e}')
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('🏁 LOGS COMPLETOS!')
