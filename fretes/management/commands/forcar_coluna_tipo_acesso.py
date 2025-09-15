from django.core.management.base import BaseCommand
from django.db import connection
import os

class Command(BaseCommand):
    help = 'Força a criação da coluna tipo_acesso na tabela fretes_userprofile'

    def handle(self, *args, **options):
        print('🔧 FORÇANDO CRIAÇÃO DA COLUNA TIPO_ACESSO')
        print('=' * 50)
        
        # Verificar se está usando PostgreSQL
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            print('❌ Não está usando PostgreSQL')
            return
        
        print('✅ Usando PostgreSQL - criando coluna tipo_acesso')
        
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
                
                if not table_exists:
                    print('❌ Tabela fretes_userprofile não existe!')
                    print('💡 Execute: python manage.py migrate')
                    return
                
                print('✅ Tabela fretes_userprofile existe')
                
                # 2. Verificar se a coluna tipo_acesso existe
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.columns 
                        WHERE table_name = 'fretes_userprofile' 
                        AND column_name = 'tipo_acesso'
                    );
                """)
                column_exists = cursor.fetchone()[0]
                
                if column_exists:
                    print('✅ Coluna tipo_acesso já existe')
                else:
                    print('❌ Coluna tipo_acesso não existe - criando...')
                    
                    # 3. Criar a coluna tipo_acesso
                    cursor.execute("""
                        ALTER TABLE fretes_userprofile 
                        ADD COLUMN tipo_acesso VARCHAR(20) DEFAULT 'limitado';
                    """)
                    print('✅ Coluna tipo_acesso criada')
                
                # 4. Verificar se a coluna is_master existe
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.columns 
                        WHERE table_name = 'fretes_userprofile' 
                        AND column_name = 'is_master'
                    );
                """)
                is_master_exists = cursor.fetchone()[0]
                
                if not is_master_exists:
                    print('❌ Coluna is_master não existe - criando...')
                    cursor.execute("""
                        ALTER TABLE fretes_userprofile 
                        ADD COLUMN is_master BOOLEAN DEFAULT FALSE;
                    """)
                    print('✅ Coluna is_master criada')
                else:
                    print('✅ Coluna is_master já existe')
                
                # 5. Verificar se a coluna tipo_usuario existe
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.columns 
                        WHERE table_name = 'fretes_userprofile' 
                        AND column_name = 'tipo_usuario'
                    );
                """)
                tipo_usuario_exists = cursor.fetchone()[0]
                
                if not tipo_usuario_exists:
                    print('❌ Coluna tipo_usuario não existe - criando...')
                    cursor.execute("""
                        ALTER TABLE fretes_userprofile 
                        ADD COLUMN tipo_usuario VARCHAR(20) DEFAULT 'solicitante';
                    """)
                    print('✅ Coluna tipo_usuario criada')
                else:
                    print('✅ Coluna tipo_usuario já existe')
                
                # 6. Verificar se a coluna transportadora_id existe
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.columns 
                        WHERE table_name = 'fretes_userprofile' 
                        AND column_name = 'transportadora_id'
                    );
                """)
                transportadora_exists = cursor.fetchone()[0]
                
                if not transportadora_exists:
                    print('❌ Coluna transportadora_id não existe - criando...')
                    cursor.execute("""
                        ALTER TABLE fretes_userprofile 
                        ADD COLUMN transportadora_id INTEGER;
                    """)
                    print('✅ Coluna transportadora_id criada')
                else:
                    print('✅ Coluna transportadora_id já existe')
                
                # 7. Listar todas as colunas da tabela
                print('\n📋 COLUNAS DA TABELA FRETES_USERPROFILE:')
                cursor.execute("""
                    SELECT column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns 
                    WHERE table_name = 'fretes_userprofile' 
                    ORDER BY column_name;
                """)
                columns = cursor.fetchall()
                
                for column in columns:
                    print(f'   - {column[0]} ({column[1]}) - Null: {column[2]} - Default: {column[3]}')
                
                print('\n✅ TODAS AS COLUNAS CRIADAS COM SUCESSO!')
                
        except Exception as e:
            print(f'❌ ERRO: {e}')
            import traceback
            print(f'Detalhes: {traceback.format_exc()}')
        
        print('\n' + '=' * 50)
        print('🏁 CRIAÇÃO DE COLUNAS FINALIZADA!')
