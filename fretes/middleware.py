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
            # Verificar se já existe dados no banco antes de executar
            if self.banco_ja_configurado():
                self.setup_done = True
                return
            self.setup_database()
            self.setup_done = True
    
    def banco_ja_configurado(self):
        """Verifica se o banco já foi configurado"""
        try:
            from django.contrib.auth.models import User
            from fretes.models import Loja, Transportadora
            
            # Se já existe usuário admin e lojas, não precisa configurar novamente
            return (User.objects.filter(username='admin').exists() and 
                    Loja.objects.exists() and 
                    Transportadora.objects.exists())
        except:
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
            import traceback
            print(f"Detalhes: {traceback.format_exc()}")
