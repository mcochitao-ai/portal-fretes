from django.core.management.base import BaseCommand
from fretes.models import Loja
import os
import pandas as pd

class Command(BaseCommand):
    help = 'Importa lojas do arquivo Excel automaticamente'

    def handle(self, *args, **options):
        self.stdout.write('🔄 IMPORTANDO LOJAS DO EXCEL...')
        
        # Verificar se o arquivo existe
        file_path = 'Lojas Portal.xlsx'
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'❌ Arquivo {file_path} não encontrado!'))
            return
        
        try:
            # Ler o arquivo Excel
            df = pd.read_excel(file_path)
            self.stdout.write(f'📊 Arquivo Excel carregado: {len(df)} lojas encontradas')
            
            # Contar lojas importadas
            importadas = 0
            existentes = 0
            
            for _, row in df.iterrows():
                loja, created = Loja.objects.get_or_create(
                    nome=str(row['Loja']),
                    defaults={
                        'endereco': str(row['Endereço']),
                        'numero': str(row['Número']) if not pd.isna(row['Número']) else '',
                        'municipio': str(row['Municipio']),
                        'estado': str(row['UF']),
                        'cep': str(row['CEP']) if not pd.isna(row['CEP']) else '',
                        'regional': str(row['Regional']) if not pd.isna(row['Regional']) else '',
                        'latitude': float(row['Latitude']) if not pd.isna(row['Latitude']) else None,
                        'longitude': float(row['Longitude']) if not pd.isna(row['Longitude']) else None
                    }
                )
                
                if created:
                    importadas += 1
                    self.stdout.write(f'✅ Loja {loja.nome} importada')
                else:
                    existentes += 1
            
            self.stdout.write(f'\n📈 RESUMO DA IMPORTAÇÃO:')
            self.stdout.write(f'   - Lojas importadas: {importadas}')
            self.stdout.write(f'   - Lojas já existentes: {existentes}')
            self.stdout.write(f'   - Total no banco: {Loja.objects.count()}')
            
            if importadas > 0:
                self.stdout.write(self.style.SUCCESS('🎉 Importação concluída com sucesso!'))
            else:
                self.stdout.write(self.style.WARNING('⚠️ Nenhuma loja nova foi importada (todas já existiam)'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro na importação: {e}'))
            import traceback
            self.stdout.write(traceback.format_exc())
