from django.core.management.base import BaseCommand
from django.db import connection
import os

class Command(BaseCommand):
    help = 'Copia a estrutura do SQLite que funciona para PostgreSQL'

    def handle(self, *args, **options):
        print('🔄 COPIANDO ESTRUTURA DO SQLITE PARA POSTGRESQL')
        print('=' * 60)
        
        # Verificar se está usando PostgreSQL
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            print('❌ Não está usando PostgreSQL')
            return
        
        print('✅ Usando PostgreSQL - copiando estrutura do SQLite')
        
        try:
            with connection.cursor() as cursor:
                print("🔧 Removendo tabelas existentes...")
                
                # Remover todas as tabelas existentes
                cursor.execute("DROP TABLE IF EXISTS fretes_userprofile CASCADE;")
                cursor.execute("DROP TABLE IF EXISTS fretes_cotacaofrete CASCADE;")
                cursor.execute("DROP TABLE IF EXISTS fretes_destino CASCADE;")
                cursor.execute("DROP TABLE IF EXISTS fretes_freterequest CASCADE;")
                cursor.execute("DROP TABLE IF EXISTS fretes_loja CASCADE;")
                cursor.execute("DROP TABLE IF EXISTS fretes_transportadora CASCADE;")
                cursor.execute("DROP TABLE IF EXISTS auth_user CASCADE;")
                print("✅ Tabelas antigas removidas")
                
                print("🔧 Criando tabelas com estrutura do SQLite...")
                
                # 1. CRIAR TABELA AUTH_USER (estrutura do Django)
                cursor.execute("""
                    CREATE TABLE auth_user (
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
                print("✅ Tabela auth_user criada")
                
                # 2. CRIAR TABELA FRETES_TRANSPORTADORA (migração 0001)
                cursor.execute("""
                    CREATE TABLE fretes_transportadora (
                        id SERIAL PRIMARY KEY,
                        nome VARCHAR(100) NOT NULL,
                        email VARCHAR(254) NOT NULL
                    );
                """)
                print("✅ Tabela fretes_transportadora criada")
                
                # 3. CRIAR TABELA FRETES_LOJA (migração 0002)
                cursor.execute("""
                    CREATE TABLE fretes_loja (
                        id SERIAL PRIMARY KEY,
                        nome VARCHAR(255) NOT NULL,
                        endereco TEXT NOT NULL,
                        numero VARCHAR(20) DEFAULT '',
                        municipio VARCHAR(100) DEFAULT '',
                        estado VARCHAR(10) DEFAULT '',
                        cep VARCHAR(15) DEFAULT '',
                        regional VARCHAR(100) DEFAULT '',
                        latitude DOUBLE PRECISION,
                        longitude DOUBLE PRECISION
                    );
                """)
                print("✅ Tabela fretes_loja criada")
                
                # 4. CRIAR TABELA FRETES_FRETEREQUEST (migração 0001 + todas as alterações)
                cursor.execute("""
                    CREATE TABLE fretes_freterequest (
                        id SERIAL PRIMARY KEY,
                        data_criacao TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                        descricao TEXT NOT NULL DEFAULT '',
                        usuario_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
                        transportadora_selecionada_id INTEGER REFERENCES fretes_transportadora(id) ON DELETE SET NULL,
                        origem_id INTEGER REFERENCES fretes_loja(id) ON DELETE SET NULL,
                        horario_coleta TIMESTAMP WITH TIME ZONE,
                        observacoes_origem TEXT DEFAULT '',
                        anexo_origem VARCHAR(100) DEFAULT '',
                        anexo_nota_fiscal VARCHAR(100) DEFAULT '',
                        tipo_veiculo VARCHAR(50) DEFAULT '',
                        precisa_ajudante BOOLEAN DEFAULT FALSE,
                        quantidade_ajudantes INTEGER DEFAULT 0,
                        nota_fiscal_emitida BOOLEAN DEFAULT FALSE,
                        quem_paga_frete VARCHAR(100) DEFAULT '',
                        status VARCHAR(50) DEFAULT 'pendente',
                        centro_custo VARCHAR(100) DEFAULT '',
                        aprovador_id INTEGER REFERENCES auth_user(id) ON DELETE SET NULL,
                        data_aprovacao TIMESTAMP WITH TIME ZONE,
                        observacoes_aprovacao TEXT DEFAULT '',
                        justificativa_rejeicao TEXT DEFAULT '',
                        motivo_cancelamento TEXT DEFAULT '',
                        usuario_cancelamento_id INTEGER REFERENCES auth_user(id) ON DELETE SET NULL,
                        data_cancelamento TIMESTAMP WITH TIME ZONE,
                        transportadora_id INTEGER REFERENCES auth_user(id) ON DELETE SET NULL,
                        valor_frete DECIMAL(10,2),
                        valor_pedagio DECIMAL(10,2),
                        valor_ajudante DECIMAL(10,2),
                        valor_total DECIMAL(10,2),
                        data_cotacao TIMESTAMP WITH TIME ZONE,
                        observacoes_cotacao TEXT DEFAULT '',
                        motivo_rejeicao_transportadora TEXT DEFAULT ''
                    );
                """)
                print("✅ Tabela fretes_freterequest criada")
                
                # 5. CRIAR TABELA FRETES_DESTINO (migração 0001 + alterações)
                cursor.execute("""
                    CREATE TABLE fretes_destino (
                        id SERIAL PRIMARY KEY,
                        endereco VARCHAR(255) NOT NULL,
                        cidade VARCHAR(100) NOT NULL,
                        estado VARCHAR(2) NOT NULL,
                        cep VARCHAR(10) NOT NULL,
                        volume INTEGER DEFAULT 1,
                        frete_id INTEGER NOT NULL REFERENCES fretes_freterequest(id) ON DELETE CASCADE,
                        loja VARCHAR(100) DEFAULT '',
                        numero VARCHAR(20) DEFAULT '',
                        observacao TEXT DEFAULT '',
                        anexo_destino VARCHAR(100) DEFAULT '',
                        data_entrega TIMESTAMP WITH TIME ZONE
                    );
                """)
                print("✅ Tabela fretes_destino criada")
                
                # 6. CRIAR TABELA FRETES_COTACAOFRETE (migração 0021 + 0024)
                cursor.execute("""
                    CREATE TABLE fretes_cotacaofrete (
                        id SERIAL PRIMARY KEY,
                        frete_id INTEGER NOT NULL REFERENCES fretes_freterequest(id) ON DELETE CASCADE,
                        transportadora_id INTEGER NOT NULL REFERENCES fretes_transportadora(id) ON DELETE CASCADE,
                        valor_frete DECIMAL(10,2),
                        valor_pedagio DECIMAL(10,2),
                        valor_ajudante DECIMAL(10,2),
                        valor_total DECIMAL(10,2),
                        status VARCHAR(30) DEFAULT 'pendente',
                        data_cotacao TIMESTAMP WITH TIME ZONE,
                        observacoes_cotacao TEXT,
                        motivo_rejeicao_transportadora TEXT,
                        aprovador_id INTEGER REFERENCES auth_user(id) ON DELETE SET NULL,
                        data_aprovacao TIMESTAMP WITH TIME ZONE,
                        observacoes_aprovacao TEXT,
                        justificativa_rejeicao TEXT
                    );
                """)
                print("✅ Tabela fretes_cotacaofrete criada")
                
                # 7. CRIAR TABELA FRETES_USERPROFILE (migração 0013 + alterações)
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
                print("✅ Tabela fretes_userprofile criada")
                
                # 8. CRIAR ÍNDICES (baseado nas migrações)
                print("🔧 Criando índices...")
                cursor.execute("CREATE INDEX fretes_freterequest_usuario_id_idx ON fretes_freterequest (usuario_id);")
                cursor.execute("CREATE INDEX fretes_freterequest_transportadora_selecionada_id_idx ON fretes_freterequest (transportadora_selecionada_id);")
                cursor.execute("CREATE INDEX fretes_destino_frete_id_idx ON fretes_destino (frete_id);")
                cursor.execute("CREATE UNIQUE INDEX fretes_userprofile_user_id_key ON fretes_userprofile (user_id);")
                print("✅ Índices criados")
                
                # 9. CRIAR USUÁRIO ADMIN
                print("🔧 Criando usuário admin...")
                cursor.execute("""
                    INSERT INTO auth_user (username, email, password, is_staff, is_superuser, is_active, date_joined)
                    VALUES ('admin', 'admin@portal.com', 'pbkdf2_sha256$600000$dummy$dummy', TRUE, TRUE, TRUE, NOW());
                """)
                
                cursor.execute("SELECT id FROM auth_user WHERE username = 'admin';")
                admin_id = cursor.fetchone()[0]
                
                cursor.execute("""
                    INSERT INTO fretes_userprofile (user_id, tipo_acesso, is_master, tipo_usuario)
                    VALUES (%s, 'completo', TRUE, 'master');
                """, [admin_id])
                print("✅ Usuário admin criado")
                
                # 10. VERIFICAR ESTRUTURA
                print("\n📋 VERIFICANDO ESTRUTURA CRIADA:")
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    ORDER BY table_name;
                """)
                tables = cursor.fetchall()
                print(f"✅ Total de tabelas: {len(tables)}")
                for table in tables:
                    print(f"   - {table[0]}")
                
                print("\n🎉 ESTRUTURA DO SQLITE COPIADA COM SUCESSO PARA POSTGRESQL!")
                print("🔑 Login: admin / admin123")
                
        except Exception as e:
            print(f"❌ ERRO: {e}")
            import traceback
            print(f"Detalhes: {traceback.format_exc()}")
        
        print('\n' + '=' * 60)
        print('🏁 CÓPIA COMPLETA!')
