#!/usr/bin/env python3
"""
Script para verificar o status do deploy e testar a funcionalidade
"""
import requests
import time
import sys

def check_site_status():
    """Verifica se o site está acessível"""
    try:
        response = requests.get('https://portal-fretes.onrender.com/', timeout=10)
        if response.status_code == 200:
            print("✅ Site está acessível")
            return True
        else:
            print(f"⚠️ Site retornou status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao acessar o site: {e}")
        return False

def check_login_page():
    """Verifica se a página de login está funcionando"""
    try:
        response = requests.get('https://portal-fretes.onrender.com/login/', timeout=10)
        if response.status_code == 200 and 'login' in response.text.lower():
            print("✅ Página de login está funcionando")
            return True
        else:
            print("⚠️ Página de login pode ter problemas")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao acessar página de login: {e}")
        return False

def main():
    print("🔍 Verificando status do deploy...")
    print("=" * 50)
    
    # Verificar site principal
    site_ok = check_site_status()
    
    # Verificar página de login
    login_ok = check_login_page()
    
    print("=" * 50)
    
    if site_ok and login_ok:
        print("🎉 Deploy parece estar funcionando!")
        print("\n📋 Próximos passos:")
        print("1. Acesse: https://portal-fretes.onrender.com/login/")
        print("2. Login com: admin / admin123")
        print("3. Teste criar um frete")
        print("4. Verifique se dados persistem após refresh")
    else:
        print("⚠️ Deploy pode ainda estar em andamento ou com problemas")
        print("\n💡 Dicas:")
        print("- Aguarde mais alguns minutos")
        print("- Verifique os logs no dashboard do Render")
        print("- Tente novamente em 5-10 minutos")

if __name__ == "__main__":
    main()
