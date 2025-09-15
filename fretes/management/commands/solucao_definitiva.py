from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import connection
import os

class Command(BaseCommand):
    help = 'Solução definitiva para o problema de login'

    def handle(self, *args, **options):
        self.stdout.write('🎯 SOLUÇÃO DEFINITIVA - PROBLEMA DE LOGIN')
        self.stdout.write('=' * 80)
        
        try:
            # 1. LIMPAR TUDO
            self.stdout.write('\n🧹 LIMPANDO USUÁRIOS EXISTENTES:')
            User.objects.all().delete()
            self.stdout.write('   ✅ Todos os usuários removidos')
            
            # 2. CRIAR USUÁRIO ADMIN SIMPLES
            self.stdout.write('\n👑 CRIANDO USUÁRIO ADMIN:')
            admin = User.objects.create_user(
                username='admin',
                email='admin@portal.com',
                password='admin123',
                is_staff=True,
                is_superuser=True,
                is_active=True
            )
            self.stdout.write('   ✅ Admin criado: admin / admin123')
            
            # 3. CRIAR USUÁRIO COCHIT0
            self.stdout.write('\n👤 CRIANDO USUÁRIO COCHIT0:')
            cochit0 = User.objects.create_user(
                username='cochit0',
                email='cochit0@portal.com',
                password='123456',
                is_staff=True,
                is_superuser=True,
                is_active=True
            )
            self.stdout.write('   ✅ Cochit0 criado: cochit0 / 123456')
            
            # 4. TESTAR LOGIN
            self.stdout.write('\n🔐 TESTANDO LOGIN:')
            from django.contrib.auth import authenticate
            
            # Testar admin
            user1 = authenticate(username='admin', password='admin123')
            if user1:
                self.stdout.write('   ✅ admin / admin123: SUCESSO')
            else:
                self.stdout.write('   ❌ admin / admin123: FALHOU')
            
            # Testar cochit0
            user2 = authenticate(username='cochit0', password='123456')
            if user2:
                self.stdout.write('   ✅ cochit0 / 123456: SUCESSO')
            else:
                self.stdout.write('   ❌ cochit0 / 123456: FALHOU')
            
            # 5. VERIFICAR BANCO
            self.stdout.write('\n🗄️ VERIFICANDO BANCO:')
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM auth_user;")
                count = cursor.fetchone()[0]
                self.stdout.write(f'   👥 Total de usuários no banco: {count}')
            
            # 6. MOSTRAR TODOS OS USUÁRIOS
            self.stdout.write('\n📋 USUÁRIOS CRIADOS:')
            for user in User.objects.all():
                self.stdout.write(f'   👤 {user.username} (staff: {user.is_staff}, superuser: {user.is_superuser}, ativo: {user.is_active})')
                
        except Exception as e:
            self.stdout.write(f'❌ ERRO: {e}')
            import traceback
            self.stdout.write(f'   Traceback: {traceback.format_exc()}')
        
        self.stdout.write('\n' + '=' * 80)
        self.stdout.write('🏁 SOLUÇÃO DEFINITIVA APLICADA!')
        self.stdout.write('🔑 CREDENCIAIS:')
        self.stdout.write('   admin / admin123')
        self.stdout.write('   cochit0 / 123456')
