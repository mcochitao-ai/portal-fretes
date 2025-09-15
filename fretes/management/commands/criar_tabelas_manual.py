from django.core.management.base import BaseCommand
from django.db import connection
import os

class Command(BaseCommand):
    help = 'Cria tabelas manualmente via SQL'

    def handle(self, *args, **options):
        self.stdout.write('🔧 CRIANDO TABELAS MANUALMENTE VIA SQL')
        self.stdout.write('=' * 80)
        
        try:
            with connection.cursor() as cursor:
                # 1. Criar tabela auth_user
                self.stdout.write('\n👤 CRIANDO TABELA AUTH_USER:')
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS auth_user (
                        id SERIAL PRIMARY KEY,
                        password VARCHAR(128) NOT NULL,
                        last_login TIMESTAMP WITH TIME ZONE,
                        is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
                        username VARCHAR(150) NOT NULL UNIQUE,
                        first_name VARCHAR(150) NOT NULL DEFAULT '',
                        last_name VARCHAR(150) NOT NULL DEFAULT '',
                        email VARCHAR(254) NOT NULL DEFAULT '',
                        is_staff BOOLEAN NOT NULL DEFAULT FALSE,
                        is_active BOOLEAN NOT NULL DEFAULT TRUE,
                        date_joined TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
                    );
                """)
                self.stdout.write('   ✅ Tabela auth_user criada')
                
                # 2. Criar tabela django_session
                self.stdout.write('\n🔐 CRIANDO TABELA DJANGO_SESSION:')
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS django_session (
                        session_key VARCHAR(40) NOT NULL PRIMARY KEY,
                        session_data TEXT NOT NULL,
                        expire_date TIMESTAMP WITH TIME ZONE NOT NULL
                    );
                """)
                self.stdout.write('   ✅ Tabela django_session criada')
                
                # 3. Criar tabela django_migrations
                self.stdout.write('\n📝 CRIANDO TABELA DJANGO_MIGRATIONS:')
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS django_migrations (
                        id SERIAL PRIMARY KEY,
                        app VARCHAR(255) NOT NULL,
                        name VARCHAR(255) NOT NULL,
                        applied TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
                    );
                """)
                self.stdout.write('   ✅ Tabela django_migrations criada')
                
                # 4. Criar tabela fretes_transportadora
                self.stdout.write('\n🚛 CRIANDO TABELA FRETES_TRANSPORTADORA:')
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS fretes_transportadora (
                        id SERIAL PRIMARY KEY,
                        nome VARCHAR(255) NOT NULL,
                        email VARCHAR(254) NOT NULL
                    );
                """)
                self.stdout.write('   ✅ Tabela fretes_transportadora criada')
                
                # 5. Criar tabela fretes_userprofile
                self.stdout.write('\n👥 CRIANDO TABELA FRETES_USERPROFILE:')
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS fretes_userprofile (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
                        tipo_usuario VARCHAR(50) NOT NULL DEFAULT 'solicitador',
                        transportadora_id INTEGER REFERENCES fretes_transportadora(id) ON DELETE SET NULL
                    );
                """)
                self.stdout.write('   ✅ Tabela fretes_userprofile criada')
                
                # 6. Criar tabela fretes_loja
                self.stdout.write('\n🏪 CRIANDO TABELA FRETES_LOJA:')
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS fretes_loja (
                        id SERIAL PRIMARY KEY,
                        nome VARCHAR(255) NOT NULL,
                        endereco TEXT NOT NULL,
                        cep VARCHAR(10) NOT NULL,
                        regional VARCHAR(100) NOT NULL
                    );
                """)
                self.stdout.write('   ✅ Tabela fretes_loja criada')
                
                # 7. Criar tabela fretes_freterequest
                self.stdout.write('\n📦 CRIANDO TABELA FRETES_FRETEREQUEST:')
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS fretes_freterequest (
                        id SERIAL PRIMARY KEY,
                        solicitador_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
                        origem_id INTEGER NOT NULL REFERENCES fretes_loja(id) ON DELETE CASCADE,
                        data_solicitacao TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                        status VARCHAR(50) NOT NULL DEFAULT 'pendente',
                        observacoes TEXT DEFAULT '',
                        anexo_origem VARCHAR(100) DEFAULT '',
                        anexo_nota_fiscal VARCHAR(100) DEFAULT '',
                        tipo_veiculo VARCHAR(50) DEFAULT '',
                        precisa_ajudante BOOLEAN DEFAULT FALSE,
                        horario_coleta TIMESTAMP WITH TIME ZONE,
                        data_cotacao TIMESTAMP WITH TIME ZONE,
                        data_aprovacao TIMESTAMP WITH TIME ZONE,
                        data_cancelamento TIMESTAMP WITH TIME ZONE,
                        aprovador_id INTEGER REFERENCES auth_user(id) ON DELETE SET NULL,
                        centro_custo VARCHAR(100) DEFAULT '',
                        observacoes_origem TEXT DEFAULT ''
                    );
                """)
                self.stdout.write('   ✅ Tabela fretes_freterequest criada')
                
                # 8. Criar tabela fretes_destino
                self.stdout.write('\n🎯 CRIANDO TABELA FRETES_DESTINO:')
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS fretes_destino (
                        id SERIAL PRIMARY KEY,
                        frete_id INTEGER NOT NULL REFERENCES fretes_freterequest(id) ON DELETE CASCADE,
                        loja_id INTEGER NOT NULL REFERENCES fretes_loja(id) ON DELETE CASCADE,
                        endereco TEXT NOT NULL,
                        numero VARCHAR(20) DEFAULT '',
                        cep VARCHAR(10) NOT NULL,
                        observacao TEXT DEFAULT '',
                        anexo VARCHAR(100) DEFAULT '',
                        data_entrega TIMESTAMP WITH TIME ZONE,
                        volume VARCHAR(100) DEFAULT ''
                    );
                """)
                self.stdout.write('   ✅ Tabela fretes_destino criada')
                
                # 9. Criar tabela fretes_cotacaofrete
                self.stdout.write('\n💰 CRIANDO TABELA FRETES_COTACAOFRETE:')
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS fretes_cotacaofrete (
                        id SERIAL PRIMARY KEY,
                        frete_id INTEGER NOT NULL REFERENCES fretes_freterequest(id) ON DELETE CASCADE,
                        transportadora_id INTEGER NOT NULL REFERENCES fretes_transportadora(id) ON DELETE CASCADE,
                        valor DECIMAL(10,2) NOT NULL,
                        observacoes TEXT DEFAULT '',
                        data_cotacao TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                        status VARCHAR(50) NOT NULL DEFAULT 'pendente'
                    );
                """)
                self.stdout.write('   ✅ Tabela fretes_cotacaofrete criada')
                
                # 10. Verificar tabelas criadas
                self.stdout.write('\n📊 VERIFICANDO TABELAS CRIADAS:')
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    ORDER BY table_name;
                """)
                tables = cursor.fetchall()
                self.stdout.write(f'   📋 Total de tabelas: {len(tables)}')
                for table in tables:
                    self.stdout.write(f'      - {table[0]}')
                
                self.stdout.write('\n✅ TODAS AS TABELAS CRIADAS COM SUCESSO!')
                
        except Exception as e:
            self.stdout.write(f'❌ ERRO: {e}')
            import traceback
            self.stdout.write(f'   Traceback: {traceback.format_exc()}')
        
        self.stdout.write('\n' + '=' * 80)
        self.stdout.write('🏁 CRIAÇÃO MANUAL DE TABELAS COMPLETA!')