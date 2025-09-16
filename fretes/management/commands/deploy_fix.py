from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection

class Command(BaseCommand):
    help = 'Comando para executar após deploy - corrige problemas de banco'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('=== INICIANDO CORREÇÕES PÓS-DEPLOY ===')
        )
        
        # 1. Executar migrações
        try:
            self.stdout.write('Executando migrações...')
            call_command('migrate', verbosity=0)
            self.stdout.write(
                self.style.SUCCESS('✓ Migrações executadas com sucesso!')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Erro nas migrações: {str(e)}')
            )
        
        # 2. Criar tabela django_admin_log se necessário
        try:
            self.stdout.write('Verificando tabela django_admin_log...')
            
            with connection.cursor() as cursor:
                # Verificar se a tabela existe
                if 'postgresql' in connection.vendor:
                    cursor.execute("""
                        SELECT EXISTS (
                            SELECT FROM information_schema.tables 
                            WHERE table_schema = 'public' 
                            AND table_name = 'django_admin_log'
                        );
                    """)
                else:
                    cursor.execute("""
                        SELECT name FROM sqlite_master 
                        WHERE type='table' AND name='django_admin_log';
                    """)
                
                table_exists = cursor.fetchone()
                
                if not table_exists or not table_exists[0]:
                    self.stdout.write('Criando tabela django_admin_log...')
                    
                    if 'postgresql' in connection.vendor:
                        cursor.execute("""
                            CREATE TABLE django_admin_log (
                                id SERIAL PRIMARY KEY,
                                action_time TIMESTAMP WITH TIME ZONE NOT NULL,
                                object_id TEXT,
                                object_repr VARCHAR(200) NOT NULL,
                                action_flag SMALLINT NOT NULL CHECK (action_flag >= 0),
                                change_message TEXT NOT NULL,
                                content_type_id INTEGER,
                                user_id INTEGER NOT NULL
                            );
                        """)
                    else:
                        cursor.execute("""
                            CREATE TABLE django_admin_log (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                action_time DATETIME NOT NULL,
                                object_id TEXT,
                                object_repr VARCHAR(200) NOT NULL,
                                action_flag SMALLINT NOT NULL CHECK (action_flag >= 0),
                                change_message TEXT NOT NULL,
                                content_type_id INTEGER,
                                user_id INTEGER NOT NULL
                            );
                        """)
                    
                    self.stdout.write(
                        self.style.SUCCESS('✓ Tabela django_admin_log criada!')
                    )
                else:
                    self.stdout.write(
                        self.style.SUCCESS('✓ Tabela django_admin_log já existe!')
                    )
                    
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Erro ao verificar/criar tabela: {str(e)}')
            )
        
        # 3. Coletar arquivos estáticos
        try:
            self.stdout.write('Coletando arquivos estáticos...')
            call_command('collectstatic', '--noinput', verbosity=0)
            self.stdout.write(
                self.style.SUCCESS('✓ Arquivos estáticos coletados!')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Erro ao coletar estáticos: {str(e)}')
            )
        
        self.stdout.write(
            self.style.SUCCESS('=== CORREÇÕES PÓS-DEPLOY CONCLUÍDAS ===')
        )

