from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connections
import os
import json

class Command(BaseCommand):
    help = 'Migra dados do SQLite local para PostgreSQL do Render'

    def handle(self, *args, **options):
        self.stdout.write('🔄 MIGRAÇÃO SQLITE → POSTGRESQL')
        self.stdout.write('=' * 50)
        
        # Verificar se estamos no Render (PostgreSQL)
        if 'DATABASE_URL' in os.environ:
            self.stdout.write('✅ Detectado PostgreSQL (Render)')
            self.migrate_data_to_postgres()
        else:
            self.stdout.write('⚠️ SQLite detectado - nada para migrar')
    
    def migrate_data_to_postgres(self):
        """Migra dados do SQLite para PostgreSQL"""
        try:
            # 1. Fazer backup dos dados do SQLite
            self.stdout.write('📦 Fazendo backup dos dados...')
            call_command('dumpdata', 
                        'auth.User', 
                        'fretes.Loja', 
                        'fretes.Transportadora', 
                        'fretes.UserProfile',
                        'fretes.FreteRequest',
                        'fretes.AgendamentoFrete',
                        'fretes.TrackingFrete',
                        'fretes.Destino',
                        'fretes.CotacaoFrete',
                        output='backup_data.json',
                        indent=2)
            
            self.stdout.write('✅ Backup criado: backup_data.json')
            
            # 2. Carregar dados no PostgreSQL
            self.stdout.write('📥 Carregando dados no PostgreSQL...')
            call_command('loaddata', 'backup_data.json', verbosity=0)
            
            self.stdout.write('✅ Dados migrados com sucesso!')
            
            # 3. Verificar migração
            self.verificar_migracao()
            
        except Exception as e:
            self.stdout.write(f'❌ Erro na migração: {str(e)}')
            raise
    
    def verificar_migracao(self):
        """Verifica se a migração foi bem-sucedida"""
        try:
            from django.contrib.auth.models import User
            from fretes.models import Loja, Transportadora, FreteRequest, TrackingFrete
            
            self.stdout.write('\n📊 VERIFICAÇÃO DA MIGRAÇÃO:')
            self.stdout.write(f'👥 Usuários: {User.objects.count()}')
            self.stdout.write(f'🏪 Lojas: {Loja.objects.count()}')
            self.stdout.write(f'🚚 Transportadoras: {Transportadora.objects.count()}')
            self.stdout.write(f'📦 Fretes: {FreteRequest.objects.count()}')
            self.stdout.write(f'📍 Tracking: {TrackingFrete.objects.count()}')
            
            self.stdout.write('\n✅ Migração concluída com sucesso!')
            
        except Exception as e:
            self.stdout.write(f'❌ Erro na verificação: {str(e)}')
