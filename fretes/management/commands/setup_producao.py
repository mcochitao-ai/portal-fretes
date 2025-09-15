from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User
from fretes.models import Transportadora, UserProfile

class Command(BaseCommand):
    help = 'Setup completo para ambiente de produção - executa no PostgreSQL'

    def handle(self, *args, **options):
        self.stdout.write('🚀 SETUP PRODUÇÃO - POSTGRESQL')
        self.stdout.write('=' * 60)
        
        try:
            # 1. Executar migrações
            self.stdout.write('📊 Executando migrações...')
            call_command('migrate', verbosity=0, interactive=False)
            self.stdout.write('✅ Migrações executadas')
            
            # 2. Verificar se precisa de setup
            from django.contrib.auth.models import User
            from fretes.models import Loja, Transportadora
            
            if not (User.objects.filter(username='admin').exists() and 
                    Loja.objects.exists() and 
                    Transportadora.objects.exists()):
                
                self.stdout.write('🔧 Executando setup inicial...')
                call_command('setup_completo', verbosity=0)
                self.stdout.write('✅ Setup inicial executado')
            else:
                self.stdout.write('✅ Banco já configurado')
            
            # 3. Associar usuários às transportadoras
            self.stdout.write('🔗 Associando usuários às transportadoras...')
            self.associar_usuarios_transportadoras()
            
            # 4. Verificar status final
            self.stdout.write('\n📊 STATUS FINAL:')
            self.verificar_status()
            
            self.stdout.write(self.style.SUCCESS('🎉 Setup de produção concluído com sucesso!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro no setup: {e}'))
            import traceback
            self.stdout.write(traceback.format_exc())
    
    def associar_usuarios_transportadoras(self):
        """Associa usuários às transportadoras correspondentes"""
        # Mapear usuários para transportadoras baseado no nome
        associacoes = [
            # Formato: (username, nome_transportadora)
            ('soluciona', 'Soluciona'),
            ('log20', 'Log20'),
            ('leao_log', 'Leão Log'),
            ('translero', 'Translero'),
            ('nika', 'Nika'),
            ('rodo_flip', 'Rodo Flip'),
        ]
        
        associados = 0
        
        for username, nome_transportadora in associacoes:
            try:
                # Buscar usuário
                user = User.objects.get(username=username)
                
                # Buscar transportadora
                transportadora = Transportadora.objects.get(nome=nome_transportadora)
                
                # Atualizar perfil do usuário
                profile, created = UserProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'tipo_usuario': 'transportadora',
                        'tipo_acesso': 'completo',
                        'transportadora': transportadora
                    }
                )
                
                # Sempre atualizar para garantir que está correto
                profile.tipo_usuario = 'transportadora'
                profile.tipo_acesso = 'completo'
                profile.transportadora = transportadora
                profile.save()
                
                self.stdout.write(f'✅ {username} → {nome_transportadora}')
                associados += 1
                
            except User.DoesNotExist:
                self.stdout.write(f'⚠️ Usuário {username} não encontrado')
            except Transportadora.DoesNotExist:
                self.stdout.write(f'⚠️ Transportadora {nome_transportadora} não encontrada')
            except Exception as e:
                self.stdout.write(f'❌ Erro ao associar {username}: {e}')
        
        self.stdout.write(f'🎉 {associados} usuários associados às transportadoras!')
    
    def verificar_status(self):
        """Verifica o status final do sistema"""
        try:
            # Verificar usuários
            users_count = User.objects.count()
            self.stdout.write(f'👤 Total de usuários: {users_count}')
            
            admin_exists = User.objects.filter(username='admin').exists()
            self.stdout.write(f'👤 Usuário admin: {"✅ Existe" if admin_exists else "❌ Não existe"}')
            
            # Verificar transportadoras
            transportadoras_count = Transportadora.objects.count()
            self.stdout.write(f'🚛 Total de transportadoras: {transportadoras_count}')
            
            # Verificar lojas
            lojas_count = Loja.objects.count()
            self.stdout.write(f'🏪 Total de lojas: {lojas_count}')
            
            # Verificar associações
            self.stdout.write('\n🔗 ASSOCIAÇÕES USUÁRIO-TRANSPORTADORA:')
            for transportadora in Transportadora.objects.all():
                usuarios_associados = UserProfile.objects.filter(
                    transportadora=transportadora,
                    tipo_usuario='transportadora'
                )
                self.stdout.write(f'🚛 {transportadora.nome}: {usuarios_associados.count()} usuário(s)')
                for profile in usuarios_associados:
                    self.stdout.write(f'   - {profile.user.username} ({profile.user.email})')
            
        except Exception as e:
            self.stdout.write(f'❌ Erro ao verificar status: {e}')