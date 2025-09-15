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
        """Executa o comando que copia a estrutura do SQLite para PostgreSQL"""
        from django.core.management import call_command
        
        try:
            print("🔧 [MIDDLEWARE] Executando cópia da estrutura do SQLite...")
            call_command('copiar_sqlite_para_postgres', verbosity=0)
            print("✅ [MIDDLEWARE] Estrutura copiada com sucesso!")
                        
        except Exception as e:
            print(f"❌ [MIDDLEWARE] Erro ao copiar estrutura: {e}")
            import traceback
            print(f"Detalhes: {traceback.format_exc()}")
