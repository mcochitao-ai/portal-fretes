from django.utils.deprecation import MiddlewareMixin
import os
import threading

class DatabaseSetupMiddleware(MiddlewareMixin):
    """
    Middleware que verifica se o banco está configurado
    Executa setup apenas uma vez por instância da aplicação
    """
    
    _setup_lock = threading.Lock()
    _setup_done = False
    _setup_attempted = False
    
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)
    
    def process_request(self, request):
        # Só executa uma vez por instância da aplicação
        if not DatabaseSetupMiddleware._setup_attempted and os.environ.get('DATABASE_URL'):
            with DatabaseSetupMiddleware._setup_lock:
                if not DatabaseSetupMiddleware._setup_attempted:
                    DatabaseSetupMiddleware._setup_attempted = True
                    
                    # Verificar se já existe dados no banco antes de executar
                    if self.banco_ja_configurado():
                        DatabaseSetupMiddleware._setup_done = True
                        return
                    
                    # Executar setup apenas se necessário
                    self.setup_database()
                    DatabaseSetupMiddleware._setup_done = True
    
    def banco_ja_configurado(self):
        """Verifica se o banco já foi configurado"""
        try:
            from django.contrib.auth.models import User
            from fretes.models import Loja, Transportadora
            
            # Se já existe usuário admin e lojas, não precisa configurar novamente
            return (User.objects.filter(username='admin').exists() and 
                    Loja.objects.exists() and 
                    Transportadora.objects.exists())
        except Exception as e:
            print(f"⚠️ [MIDDLEWARE] Erro ao verificar banco: {e}")
            return False
    
    def setup_database(self):
        """Executa o setup completo do sistema"""
        from django.core.management import call_command
        
        try:
            print("🔧 [MIDDLEWARE] Executando setup completo...")
            call_command('setup_completo', verbosity=0)
            print("✅ [MIDDLEWARE] Setup completo executado com sucesso!")
                        
        except Exception as e:
            print(f"❌ [MIDDLEWARE] Erro ao configurar banco: {e}")
            # Não imprimir traceback completo para evitar spam no log
            print("⚠️ [MIDDLEWARE] Setup falhou, mas aplicação continuará funcionando")
