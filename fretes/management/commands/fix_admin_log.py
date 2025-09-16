from django.core.management.base import BaseCommand
from django.db import connection
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Cria a tabela django_admin_log usando migrações do Django'

    def handle(self, *args, **options):
        try:
            # Tentar executar as migrações do admin
            self.stdout.write(
                self.style.WARNING('Executando migrações do Django Admin...')
            )
            
            call_command('migrate', 'admin', verbosity=0)
            
            self.stdout.write(
                self.style.SUCCESS('Migrações do Django Admin executadas com sucesso!')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erro ao executar migrações: {str(e)}')
            )
            
            # Se falhar, tentar criar a tabela manualmente
            self.stdout.write(
                self.style.WARNING('Tentando criar tabela manualmente...')
            )
            
            try:
                with connection.cursor() as cursor:
                    # Verificar se é PostgreSQL
                    if 'postgresql' in connection.vendor:
                        cursor.execute("""
                            CREATE TABLE IF NOT EXISTS django_admin_log (
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
                        # SQLite
                        cursor.execute("""
                            CREATE TABLE IF NOT EXISTS django_admin_log (
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
                        self.style.SUCCESS('Tabela django_admin_log criada manualmente!')
                    )
                    
            except Exception as e2:
                self.stdout.write(
                    self.style.ERROR(f'Erro ao criar tabela manualmente: {str(e2)}')
                )
