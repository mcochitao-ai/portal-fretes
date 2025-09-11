import os
import django
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal_fretes.settings')
django.setup()

from fretes.models import Loja

# Ajuste o caminho se necessário
file_path = 'Lojas Portal.xlsx'

df = pd.read_excel(file_path)


for _, row in df.iterrows():
    Loja.objects.get_or_create(
        nome=row['Loja'],
        endereco=row['Endereço'],
        numero=str(row['Número']),
        municipio=row['Municipio'],
        estado=row['UF'],
        cep=str(row['CEP']) if not pd.isna(row['CEP']) else '',
        regional=row['Regional'] if not pd.isna(row['Regional']) else '',
        latitude=row['Latitude'] if not pd.isna(row['Latitude']) else None,
        longitude=row['Longitude'] if not pd.isna(row['Longitude']) else None
    )

print('Importação concluída!')
