# Correções para Problemas no Render

## Problemas Identificados

### 1. WORKER TIMEOUT
- **Causa**: Middleware executando comando pesado em cada requisição
- **Solução**: Implementado thread lock para executar setup apenas uma vez por instância

### 2. Conexão com Banco Fechada
- **Causa**: Comando tentando recriar tabelas desnecessariamente
- **Solução**: Verificação de existência de tabelas antes de criar

### 3. Performance Lenta
- **Causa**: Setup executando no middleware
- **Solução**: Otimizado para executar apenas quando necessário

### 4. Comando Inexistente
- **Causa**: `render.yaml` tentando executar `python manage.py resolver_tudo`
- **Solução**: Removido comando inexistente

## Correções Implementadas

### 1. Middleware Otimizado (`fretes/middleware.py`)
- Thread lock para evitar execução múltipla
- Verificação de banco configurado antes de executar setup
- Tratamento de erros melhorado

### 2. Comando Setup Otimizado (`fretes/management/commands/setup_completo.py`)
- Uso de migrações Django em vez de SQL manual
- Verificação de existência de tabelas
- Bulk create para importação de lojas
- Fallback para lojas básicas se Excel não existir

### 3. Configuração Gunicorn (`gunicorn.conf.py`)
- Timeout aumentado para 120 segundos
- Configurações de performance otimizadas
- Logging configurado

### 4. Render.yaml Atualizado
- Removido comando inexistente
- Adicionado comando de inicialização
- Configurações de gunicorn otimizadas

### 5. Comando de Inicialização (`fretes/management/commands/init_deploy.py`)
- Executa apenas o necessário no deploy
- Não falha o deploy por erros de setup
- Verifica se banco já está configurado

### 6. Comando de Verificação (`fretes/management/commands/verificar_banco.py`)
- Verifica status do banco de forma simples
- Útil para debug

## Configurações de Performance

### Gunicorn
- Workers: 2
- Timeout: 120 segundos
- Max requests: 1000
- Preload app: True

### Django
- Connection max age: 600 segundos
- Connection health checks: True
- Sessões em cache

## Como Testar

1. Fazer deploy no Render
2. Verificar logs para confirmar que não há mais timeouts
3. Acessar a aplicação para confirmar funcionamento
4. Executar `python manage.py verificar_banco` para verificar status

## Monitoramento

- Logs do Render devem mostrar setup executado apenas uma vez
- Não deve haver mais erros de "connection is closed"
- Aplicação deve responder rapidamente
- Workers não devem ser mortos por timeout
