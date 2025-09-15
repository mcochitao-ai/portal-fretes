from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from fretes.models import Loja, Transportadora, UserProfile
from django.db import connection

class Command(BaseCommand):
    help = 'Verifica o status do banco de dados em produção'

    def handle(self, *args, **options):
        self.stdout.write('🔍 VERIFICAÇÃO DO BANCO DE DADOS EM PRODUÇÃO')
        self.stdout.write('=' * 60)
        
        try:
            # Verificar conexão com banco
            with connection.cursor() as cursor:
                cursor.execute("SELECT version();")
                version = cursor.fetchone()
                self.stdout.write(f'✅ Conexão com banco: {version[0][:50]}...')
            
            # Verificar usuários
            users_count = User.objects.count()
            self.stdout.write(f'👤 Total de usuários: {users_count}')
            
            admin_exists = User.objects.filter(username='admin').exists()
            self.stdout.write(f'👤 Usuário admin: {"✅ Existe" if admin_exists else "❌ Não existe"}')
            
            if admin_exists:
                admin = User.objects.get(username='admin')
                self.stdout.write(f'   - Ativo: {admin.is_active}')
                self.stdout.write(f'   - Staff: {admin.is_staff}')
                self.stdout.write(f'   - Superuser: {admin.is_superuser}')
                
                try:
                    profile = admin.userprofile
                    self.stdout.write(f'   - Profile tipo: {profile.tipo_usuario}')
                    self.stdout.write(f'   - Profile master: {profile.is_master}')
                except UserProfile.DoesNotExist:
                    self.stdout.write('   - ❌ Profile não encontrado')
            
            # Verificar transportadoras
            transportadoras_count = Transportadora.objects.count()
            self.stdout.write(f'🚛 Total de transportadoras: {transportadoras_count}')
            
            if transportadoras_count > 0:
                self.stdout.write('   Transportadoras:')
                for t in Transportadora.objects.all()[:5]:  # Mostrar apenas as primeiras 5
                    self.stdout.write(f'   - {t.nome} ({t.email})')
                if transportadoras_count > 5:
                    self.stdout.write(f'   ... e mais {transportadoras_count - 5} transportadoras')
            
            # Verificar lojas
            lojas_count = Loja.objects.count()
            self.stdout.write(f'🏪 Total de lojas: {lojas_count}')
            
            # Verificar tabela de sessões
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT table_name FROM information_schema.tables 
                    WHERE table_schema = 'public' AND table_name = 'django_session'
                """)
                session_table_exists = cursor.fetchone() is not None
                self.stdout.write(f'📊 Tabela de sessões: {"✅ Existe" if session_table_exists else "❌ Não existe"}')
                
                if session_table_exists:
                    cursor.execute("SELECT COUNT(*) FROM django_session")
                    session_count = cursor.fetchone()[0]
                    self.stdout.write(f'   - Sessões ativas: {session_count}')
            
            # Verificar se há fretes pendentes
            from fretes.models import FreteRequest
            fretes_pendentes = FreteRequest.objects.filter(status='pendente').count()
            self.stdout.write(f'📦 Fretes pendentes: {fretes_pendentes}')
            
            self.stdout.write(self.style.SUCCESS('🎉 Verificação concluída!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro na verificação: {e}'))
            import traceback
            self.stdout.write(traceback.format_exc())
