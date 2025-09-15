from django.core.management.base import BaseCommand
from fretes.models import Loja
from django.db import connection

class Command(BaseCommand):
    help = 'Verifica se as lojas foram importadas corretamente'

    def handle(self, *args, **options):
        self.stdout.write('🔍 VERIFICANDO LOJAS NO BANCO...')
        self.stdout.write('=' * 50)
        
        # Verificar se a tabela existe
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'fretes_loja'
                );
            """)
            tabela_existe = cursor.fetchone()[0]
            
            if tabela_existe:
                self.stdout.write('✅ Tabela fretes_loja existe')
                
                # Contar lojas
                cursor.execute("SELECT COUNT(*) FROM fretes_loja;")
                total_lojas = cursor.fetchone()[0]
                self.stdout.write(f'📊 Total de lojas: {total_lojas}')
                
                if total_lojas > 0:
                    # Mostrar algumas lojas
                    cursor.execute("SELECT id, nome, endereco, municipio, estado FROM fretes_loja LIMIT 5;")
                    lojas = cursor.fetchall()
                    
                    self.stdout.write('\n📋 Primeiras 5 lojas:')
                    for loja in lojas:
                        self.stdout.write(f'   - ID: {loja[0]} | Nome: {loja[1]} | {loja[2]}, {loja[3]}/{loja[4]}')
                else:
                    self.stdout.write('❌ Nenhuma loja encontrada na tabela!')
            else:
                self.stdout.write('❌ Tabela fretes_loja NÃO existe!')
        
        # Verificar via Django ORM
        self.stdout.write('\n🔍 VERIFICAÇÃO VIA DJANGO ORM:')
        try:
            lojas_count = Loja.objects.count()
            self.stdout.write(f'📊 Django ORM - Total de lojas: {lojas_count}')
            
            if lojas_count > 0:
                lojas = Loja.objects.all()[:5]
                self.stdout.write('\n📋 Primeiras 5 lojas (Django ORM):')
                for loja in lojas:
                    self.stdout.write(f'   - ID: {loja.id} | Nome: {loja.nome} | {loja.endereco}, {loja.municipio}/{loja.estado}')
            else:
                self.stdout.write('❌ Django ORM - Nenhuma loja encontrada!')
                
        except Exception as e:
            self.stdout.write(f'❌ Erro no Django ORM: {e}')
        
        # Verificar arquivo Excel
        import os
        excel_path = 'Lojas Portal.xlsx'
        if os.path.exists(excel_path):
            self.stdout.write(f'\n✅ Arquivo Excel encontrado: {excel_path}')
            file_size = os.path.getsize(excel_path)
            self.stdout.write(f'📁 Tamanho do arquivo: {file_size} bytes')
        else:
            self.stdout.write(f'\n❌ Arquivo Excel NÃO encontrado: {excel_path}')
        
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write('🏁 VERIFICAÇÃO COMPLETA!')
