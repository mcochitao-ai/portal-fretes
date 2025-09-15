from django.utils.deprecation import MiddlewareMixin
import os

class DatabaseSetupMiddleware(MiddlewareMixin):
    """
    Middleware que verifica e cria todas as tabelas necessárias
    Executa automaticamente em todas as requisições
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.setup_done = False
        super().__init__(get_response)
    
    def process_request(self, request):
        # Só executa uma vez por sessão para não sobrecarregar
        if not self.setup_done and os.environ.get('DATABASE_URL'):
            self.setup_database()
            self.setup_done = True
    
    def setup_database(self):
        """Verifica e cria todas as tabelas necessárias"""
        from django.db import connection
        
        try:
            with connection.cursor() as cursor:
                print("🔧 [MIDDLEWARE] Verificando e criando todas as tabelas...")
                
                # 1. CRIAR TABELA AUTH_USER SE NÃO EXISTIR
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
                print("✅ [MIDDLEWARE] Tabela auth_user OK")
                
                # 2. CRIAR TABELA FRETES_TRANSPORTADORA SE NÃO EXISTIR
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS fretes_transportadora (
                        id SERIAL PRIMARY KEY,
                        nome VARCHAR(255) NOT NULL,
                        email VARCHAR(254) NOT NULL
                    );
                """)
                print("✅ [MIDDLEWARE] Tabela fretes_transportadora OK")
                
                # 3. CRIAR TABELA FRETES_LOJA SE NÃO EXISTIR
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS fretes_loja (
                        id SERIAL PRIMARY KEY,
                        nome VARCHAR(255) NOT NULL,
                        endereco TEXT NOT NULL,
                        numero VARCHAR(20) DEFAULT '',
                        municipio VARCHAR(100) DEFAULT '',
                        estado VARCHAR(2) DEFAULT '',
                        cep VARCHAR(15) DEFAULT '',
                        regional VARCHAR(100) DEFAULT '',
                        latitude DECIMAL(9,6),
                        longitude DECIMAL(9,6)
                    );
                """)
                print("✅ [MIDDLEWARE] Tabela fretes_loja OK")
                
                # 4. CRIAR TABELA FRETES_FRETEREQUEST SE NÃO EXISTIR
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS fretes_freterequest (
                        id SERIAL PRIMARY KEY,
                        usuario_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
                        data_criacao TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                        descricao TEXT DEFAULT '',
                        transportadora_selecionada_id INTEGER REFERENCES fretes_transportadora(id) ON DELETE SET NULL,
                        origem_id INTEGER REFERENCES fretes_loja(id) ON DELETE SET NULL,
                        horario_coleta VARCHAR(50) DEFAULT '',
                        observacoes_origem TEXT DEFAULT '',
                        anexo_origem VARCHAR(100) DEFAULT '',
                        tipo_veiculo VARCHAR(10) DEFAULT '',
                        precisa_ajudante BOOLEAN DEFAULT FALSE,
                        quantidade_ajudantes INTEGER DEFAULT 0,
                        nota_fiscal_emitida BOOLEAN DEFAULT FALSE,
                        anexo_nota_fiscal VARCHAR(100) DEFAULT '',
                        quem_paga_frete VARCHAR(100) DEFAULT '',
                        status VARCHAR(30) DEFAULT 'pendente',
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
                print("✅ [MIDDLEWARE] Tabela fretes_freterequest OK")
                
                # 5. CRIAR TABELA FRETES_DESTINO SE NÃO EXISTIR
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS fretes_destino (
                        id SERIAL PRIMARY KEY,
                        frete_id INTEGER NOT NULL REFERENCES fretes_freterequest(id) ON DELETE CASCADE,
                        endereco VARCHAR(255) NOT NULL,
                        cidade VARCHAR(100) NOT NULL,
                        estado VARCHAR(2) NOT NULL,
                        cep VARCHAR(10) NOT NULL,
                        volume INTEGER DEFAULT 1,
                        loja VARCHAR(100) DEFAULT '',
                        numero VARCHAR(20) DEFAULT '',
                        data_entrega TIMESTAMP WITH TIME ZONE,
                        observacao TEXT DEFAULT '',
                        anexo_destino VARCHAR(100) DEFAULT ''
                    );
                """)
                print("✅ [MIDDLEWARE] Tabela fretes_destino OK")
                
                # 6. CRIAR TABELA FRETES_COTACAOFRETE SE NÃO EXISTIR
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS fretes_cotacaofrete (
                        id SERIAL PRIMARY KEY,
                        frete_id INTEGER NOT NULL REFERENCES fretes_freterequest(id) ON DELETE CASCADE,
                        transportadora_id INTEGER NOT NULL REFERENCES fretes_transportadora(id) ON DELETE CASCADE,
                        valor_frete DECIMAL(10,2),
                        valor_pedagio DECIMAL(10,2),
                        valor_ajudante DECIMAL(10,2),
                        valor_total DECIMAL(10,2),
                        status VARCHAR(30) DEFAULT 'pendente',
                        data_cotacao TIMESTAMP WITH TIME ZONE,
                        observacoes_cotacao TEXT DEFAULT '',
                        motivo_rejeicao_transportadora TEXT DEFAULT '',
                        aprovador_id INTEGER REFERENCES auth_user(id) ON DELETE SET NULL,
                        data_aprovacao TIMESTAMP WITH TIME ZONE,
                        observacoes_aprovacao TEXT DEFAULT '',
                        justificativa_rejeicao TEXT DEFAULT ''
                    );
                """)
                print("✅ [MIDDLEWARE] Tabela fretes_cotacaofrete OK")
                
                # 7. CRIAR TABELA FRETES_USERPROFILE SE NÃO EXISTIR
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS fretes_userprofile (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
                        tipo_acesso VARCHAR(20) DEFAULT 'limitado',
                        is_master BOOLEAN DEFAULT FALSE,
                        tipo_usuario VARCHAR(20) DEFAULT 'solicitante',
                        transportadora_id INTEGER REFERENCES fretes_transportadora(id) ON DELETE SET NULL
                    );
                """)
                print("✅ [MIDDLEWARE] Tabela fretes_userprofile OK")
                
                # 8. CRIAR ÍNDICES ÚNICOS
                cursor.execute("""
                    CREATE UNIQUE INDEX IF NOT EXISTS fretes_userprofile_user_id_key 
                    ON fretes_userprofile (user_id);
                """)
                print("✅ [MIDDLEWARE] Índices únicos criados")
                
                # 9. CRIAR USUÁRIO ADMIN SE NÃO EXISTIR
                cursor.execute("SELECT id FROM auth_user WHERE username = 'admin';")
                admin_exists = cursor.fetchone()
                
                if not admin_exists:
                    cursor.execute("""
                        INSERT INTO auth_user (username, email, password, is_staff, is_superuser, is_active, date_joined)
                        VALUES ('admin', 'admin@portal.com', 'pbkdf2_sha256$600000$dummy$dummy', TRUE, TRUE, TRUE, NOW());
                    """)
                    print("✅ [MIDDLEWARE] Usuário admin criado")
                    
                    # Criar profile do admin
                    cursor.execute("SELECT id FROM auth_user WHERE username = 'admin';")
                    admin_id = cursor.fetchone()[0]
                    
                    cursor.execute("""
                        INSERT INTO fretes_userprofile (user_id, tipo_acesso, is_master, tipo_usuario)
                        VALUES (%s, 'completo', TRUE, 'master')
                        ON CONFLICT (user_id) DO UPDATE SET
                        tipo_acesso = 'completo',
                        is_master = TRUE,
                        tipo_usuario = 'master';
                    """, [admin_id])
                    print("✅ [MIDDLEWARE] Profile do admin criado")
                else:
                    print("✅ [MIDDLEWARE] Usuário admin já existe")
                
                print("🎉 [MIDDLEWARE] TODAS AS TABELAS VERIFICADAS E CRIADAS COM SUCESSO!")
                        
        except Exception as e:
            print(f"❌ [MIDDLEWARE] Erro ao criar tabelas: {e}")
            import traceback
            print(f"Detalhes: {traceback.format_exc()}")
