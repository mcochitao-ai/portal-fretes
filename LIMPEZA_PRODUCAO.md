# 🧹 Limpeza do Banco de Produção

## Como limpar o banco de dados de produção no Render

### Opção 1: Via Render Shell (Recomendado)

1. Acesse o dashboard do Render
2. Vá para o serviço `portal-fretes`
3. Clique em "Shell" no menu lateral
4. Execute o comando:

```bash
python manage.py limpar_producao --confirm-producao
```

### Opção 2: Via Django Admin (Alternativa)

1. Acesse https://portal-fretes.onrender.com/admin/
2. Faça login com usuário administrador
3. Navegue para as seções:
   - **Fretes** → **Frete requests** → Selecione todos → Delete
   - **Fretes** → **Destinos** → Selecione todos → Delete  
   - **Fretes** → **Cotações de frete** → Selecione todos → Delete

### ⚠️ Importante

- **NUNCA** remova usuários em produção
- **SEMPRE** confirme a operação com `--confirm-producao`
- **BACKUP** automático é feito pelo Render
- **TESTE** primeiro em ambiente local

### ✅ Verificação

Após a limpeza, verifique:
- Fretes: 0
- Destinos: 0
- Cotações: 0
- Usuários: mantidos

### 🚀 Próximos Passos

Após limpeza:
1. Teste os novos dashboards
2. Crie fretes de demonstração
3. Valide o fluxo completo
4. Prepare apresentação

---
**Última limpeza:** $(date)
**Ambiente:** Produção (Render)
**Status:** ✅ Pronto para demonstrações
