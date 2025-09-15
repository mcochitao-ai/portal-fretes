from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from fretes.models import Transportadora, UserProfile

class Command(BaseCommand):
    help = 'Associa usuários às transportadoras correspondentes'

    def handle(self, *args, **options):
        self.stdout.write('🔗 ASSOCIANDO USUÁRIOS ÀS TRANSPORTADORAS')
        self.stdout.write('=' * 60)
        
        try:
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
            
            self.stdout.write(f'\n🎉 {associados} usuários associados às transportadoras!')
            
            # Mostrar resumo
            self.stdout.write('\n📊 RESUMO DAS ASSOCIAÇÕES:')
            for transportadora in Transportadora.objects.all():
                usuarios_associados = UserProfile.objects.filter(
                    transportadora=transportadora,
                    tipo_usuario='transportadora'
                )
                self.stdout.write(f'🚛 {transportadora.nome}: {usuarios_associados.count()} usuário(s)')
                for profile in usuarios_associados:
                    self.stdout.write(f'   - {profile.user.username} ({profile.user.email})')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro geral: {e}'))
            import traceback
            self.stdout.write(traceback.format_exc())
