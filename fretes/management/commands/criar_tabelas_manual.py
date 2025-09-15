from django.core.management.base import BaseCommand
from django.db import connection
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Cria tabelas manualmente se as migrações falharem'

    def handle(self, *args, **options):
        self.stdout.write('🔧 Criando tabelas manualmente...')
        self.stdout.write('=' * 60)
        
        # Verificar conexão
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                self.stdout.write('✅ Conexão com banco: OK')
        except Exception as e:
            self.stdout.write(f'❌ Erro na conexão: {e}')
            return
        
        # Verificar se é PostgreSQL
        db_config = connection.settings_dict
        if 'postgresql' not in db_config['ENGINE']:
            self.stdout.write('❌ Não é PostgreSQL, abortando...')
            return
        
        self.stdout.write('✅ Usando PostgreSQL')
        
        # Tentar migrações normais primeiro
        self.stdout.write('\n🔄 Tentando migrações normais...')
        try:
            call_command('makemigrations', verbosity=0)
            call_command('migrate', verbosity=0)
            self.stdout.write('✅ Migrações normais executadas')
        except Exception as e:
            self.stdout.write(f'⚠️ Migrações normais falharam: {e}')
            self.stdout.write('🔧 Tentando criação manual...')
            
            # Criar tabelas manualmente
            self.criar_tabelas_manualmente()
        
        # Verificar resultado
        self.verificar_tabelas()
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('🎯 Processo concluído!')
    
    def criar_tabelas_manualmente(self):
        """Cria as tabelas essenciais manualmente"""
        try:
            with connection.cursor() as cursor:
                # Criar tabela auth_user
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS auth_user (
                        id SERIAL PRIMARY KEY,
                        password VARCHAR(128) NOT NULL,
                        last_login TIMESTAMP WITH TIME ZONE,
                        is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
                        username VARCHAR(150) UNIQUE NOT NULL,
                        first_name VARCHAR(150) NOT NULL DEFAULT '',
                        last_name VARCHAR(150) NOT NULL DEFAULT '',
                        email VARCHAR(254) NOT NULL DEFAULT '',
                        is_staff BOOLEAN NOT NULL DEFAULT FALSE,
                        is_active BOOLEAN NOT NULL DEFAULT TRUE,
                        date_joined TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
                    );
                """)
                self.stdout.write('✅ Tabela auth_user criada')
                
                # Criar tabela auth_group
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS auth_group (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(150) UNIQUE NOT NULL
                    );
                """)
                self.stdout.write('✅ Tabela auth_group criada')
                
                # Criar tabela auth_permission
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS auth_permission (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        content_type_id INTEGER NOT NULL,
                        codename VARCHAR(100) NOT NULL,
                        UNIQUE(content_type_id, codename)
                    );
                """)
                self.stdout.write('✅ Tabela auth_permission criada')
                
                # Criar tabela django_content_type
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS django_content_type (
                        id SERIAL PRIMARY KEY,
                        app_label VARCHAR(100) NOT NULL,
                        model VARCHAR(100) NOT NULL,
                        UNIQUE(app_label, model)
                    );
                """)
                self.stdout.write('✅ Tabela django_content_type criada')
                
                # Criar tabela django_migrations
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS django_migrations (
                        id SERIAL PRIMARY KEY,
                        app VARCHAR(255) NOT NULL,
                        name VARCHAR(255) NOT NULL,
                        applied TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
                    );
                """)
                self.stdout.write('✅ Tabela django_migrations criada')
                
                # Criar tabela django_session
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS django_session (
                        session_key VARCHAR(40) PRIMARY KEY,
                        session_data TEXT NOT NULL,
                        expire_date TIMESTAMP WITH TIME ZONE NOT NULL
                    );
                """)
                self.stdout.write('✅ Tabela django_session criada')
                
                # Criar tabela fretes_userprofile
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS fretes_userprofile (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER UNIQUE NOT NULL,
                        tipo_usuario VARCHAR(20) NOT NULL DEFAULT 'solicitador',
                        is_master BOOLEAN NOT NULL DEFAULT FALSE,
                        transportadora_id INTEGER,
                        FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE
                    );
                """)
                self.stdout.write('✅ Tabela fretes_userprofile criada')
                
                # Criar tabela fretes_transportadora
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS fretes_transportadora (
                        id SERIAL PRIMARY KEY,
                        nome VARCHAR(200) NOT NULL,
                        cnpj VARCHAR(18) UNIQUE NOT NULL,
                        telefone VARCHAR(20),
                        email VARCHAR(254),
                        endereco TEXT,
                        ativa BOOLEAN NOT NULL DEFAULT TRUE,
                        data_criacao TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
                    );
                """)
                self.stdout.write('✅ Tabela fretes_transportadora criada')
                
                # Criar tabela fretes_loja
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS fretes_loja (
                        id SERIAL PRIMARY KEY,
                        nome VARCHAR(200) NOT NULL,
                        cep VARCHAR(10),
                        endereco TEXT,
                        cidade VARCHAR(100),
                        estado VARCHAR(2),
                        regional VARCHAR(100),
                        ativa BOOLEAN NOT NULL DEFAULT TRUE
                    );
                """)
                self.stdout.write('✅ Tabela fretes_loja criada')
                
                # Criar tabela fretes_freterequest
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS fretes_freterequest (
                        id SERIAL PRIMARY KEY,
                        solicitador_id INTEGER NOT NULL,
                        origem_id INTEGER NOT NULL,
                        destino_id INTEGER NOT NULL,
                        volume DECIMAL(10,2),
                        tipo_veiculo VARCHAR(50),
                        horario_coleta TIMESTAMP WITH TIME ZONE,
                        data_entrega DATE,
                        observacoes_origem TEXT,
                        observacoes_destino TEXT,
                        status VARCHAR(20) NOT NULL DEFAULT 'pendente',
                        aprovador_id INTEGER,
                        centro_custo VARCHAR(100),
                        data_cotacao TIMESTAMP WITH TIME ZONE,
                        data_aprovacao TIMESTAMP WITH TIME ZONE,
                        data_cancelamento TIMESTAMP WITH TIME ZONE,
                        precisa_ajudante BOOLEAN NOT NULL DEFAULT FALSE,
                        anexo_origem VARCHAR(100),
                        anexo_destino VARCHAR(100),
                        anexo_nota_fiscal VARCHAR(100),
                        data_criacao TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                        FOREIGN KEY (solicitador_id) REFERENCES auth_user(id) ON DELETE CASCADE,
                        FOREIGN KEY (origem_id) REFERENCES fretes_loja(id) ON DELETE CASCADE,
                        FOREIGN KEY (destino_id) REFERENCES fretes_loja(id) ON DELETE CASCADE,
                        FOREIGN KEY (aprovador_id) REFERENCES auth_user(id) ON DELETE SET NULL
                    );
                """)
                self.stdout.write('✅ Tabela fretes_freterequest criada')
                
                # Criar tabela fretes_destino
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS fretes_destino (
                        id SERIAL PRIMARY KEY,
                        frete_id INTEGER NOT NULL,
                        loja_id INTEGER NOT NULL,
                        volume DECIMAL(10,2),
                        numero VARCHAR(20),
                        observacao TEXT,
                        anexo VARCHAR(100),
                        data_entrega DATE,
                        FOREIGN KEY (frete_id) REFERENCES fretes_freterequest(id) ON DELETE CASCADE,
                        FOREIGN KEY (loja_id) REFERENCES fretes_loja(id) ON DELETE CASCADE
                    );
                """)
                self.stdout.write('✅ Tabela fretes_destino criada')
                
                # Criar tabela fretes_cotacaofrete
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS fretes_cotacaofrete (
                        id SERIAL PRIMARY KEY,
                        frete_id INTEGER NOT NULL,
                        transportadora_id INTEGER NOT NULL,
                        valor DECIMAL(10,2) NOT NULL,
                        observacoes TEXT,
                        data_cotacao TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                        FOREIGN KEY (frete_id) REFERENCES fretes_freterequest(id) ON DELETE CASCADE,
                        FOREIGN KEY (transportadora_id) REFERENCES fretes_transportadora(id) ON DELETE CASCADE
                    );
                """)
                self.stdout.write('✅ Tabela fretes_cotacaofrete criada')
                
        except Exception as e:
            self.stdout.write(f'❌ Erro ao criar tabelas: {e}')
    
    def verificar_tabelas(self):
        """Verifica se as tabelas foram criadas"""
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    ORDER BY table_name;
                """)
                tables = cursor.fetchall()
                
                self.stdout.write(f'\n📊 Total de tabelas: {len(tables)}')
                for table in tables:
                    self.stdout.write(f'   - {table[0]}')
                
                # Verificar tabelas essenciais
                essential_tables = ['auth_user', 'fretes_freterequest', 'fretes_userprofile']
                for table in essential_tables:
                    if any(t[0] == table for t in tables):
                        self.stdout.write(f'✅ {table}: OK')
                    else:
                        self.stdout.write(f'❌ {table}: FALTANDO')
                        
        except Exception as e:
            self.stdout.write(f'❌ Erro ao verificar tabelas: {e}')
