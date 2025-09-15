from django.core.management.base import BaseCommand
from django.db import connection
import os

class Command(BaseCommand):
    help = 'Recria completamente a tabela fretes_userprofile com todas as colunas'

    def handle(self, *args, **options):
        print('🔧 RECRIANDO TABELA FRETES_USERPROFILE')
        print('=' * 50)
        
        # Verificar se está usando PostgreSQL
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            print('❌ Não está usando PostgreSQL')
            return
        
        print('✅ Usando PostgreSQL - recriando tabela fretes_userprofile')
        
        try:
            with connection.cursor() as cursor:
                # 1. Verificar se a tabela existe
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'fretes_userprofile'
                    );
                """)
                table_exists = cursor.fetchone()[0]
                
                if table_exists:
                    print('⚠️ Tabela fretes_userprofile existe - removendo...')
                    cursor.execute("DROP TABLE fretes_userprofile CASCADE;")
                    print('✅ Tabela removida')
                
                # 2. Criar a tabela fretes_userprofile completa
                print('🔨 Criando nova tabela fretes_userprofile...')
                cursor.execute("""
                    CREATE TABLE fretes_userprofile (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
                        tipo_acesso VARCHAR(20) DEFAULT 'limitado',
                        is_master BOOLEAN DEFAULT FALSE,
                        tipo_usuario VARCHAR(20) DEFAULT 'solicitante',
                        transportadora_id INTEGER REFERENCES fretes_transportadora(id) ON DELETE SET NULL
                    );
                """)
                print('✅ Tabela fretes_userprofile criada com sucesso')
                
                # 3. Criar índice único para user_id
                cursor.execute("""
                    CREATE UNIQUE INDEX fretes_userprofile_user_id_key 
                    ON fretes_userprofile (user_id);
                """)
                print('✅ Índice único criado')
                
                # 4. Verificar se a tabela foi criada corretamente
                print('\n📋 VERIFICANDO TABELA CRIADA:')
                cursor.execute("""
                    SELECT column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns 
                    WHERE table_name = 'fretes_userprofile' 
                    ORDER BY column_name;
                """)
                columns = cursor.fetchall()
                
                print(f'   📋 Total de colunas: {len(columns)}')
                for column in columns:
                    print(f'      - {column[0]} ({column[1]}) - Null: {column[2]} - Default: {column[3]}')
                
                # 5. Verificar se todas as colunas necessárias existem
                column_names = [col[0] for col in columns]
                required_columns = ['id', 'user_id', 'tipo_acesso', 'is_master', 'tipo_usuario', 'transportadora_id']
                
                missing_columns = [col for col in required_columns if col not in column_names]
                if missing_columns:
                    print(f'❌ Colunas faltando: {missing_columns}')
                else:
                    print('✅ Todas as colunas necessárias estão presentes')
                
                print('\n✅ TABELA FRETES_USERPROFILE RECRIADA COM SUCESSO!')
                
        except Exception as e:
            print(f'❌ ERRO: {e}')
            import traceback
            print(f'Detalhes: {traceback.format_exc()}')
        
        print('\n' + '=' * 50)
        print('🏁 RECRIAÇÃO DE TABELA FINALIZADA!')
