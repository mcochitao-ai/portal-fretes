# Generated manually for performance optimization

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fretes', '0025_userprofile_transportadora'),
    ]

    operations = [
        # Índices para FreteRequest
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS idx_freterequest_status ON fretes_freterequest(status);",
            reverse_sql="DROP INDEX IF EXISTS idx_freterequest_status;"
        ),
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS idx_freterequest_data_criacao ON fretes_freterequest(data_criacao DESC);",
            reverse_sql="DROP INDEX IF EXISTS idx_freterequest_data_criacao;"
        ),
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS idx_freterequest_usuario ON fretes_freterequest(usuario_id);",
            reverse_sql="DROP INDEX IF EXISTS idx_freterequest_usuario;"
        ),
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS idx_freterequest_origem ON fretes_freterequest(origem_id);",
            reverse_sql="DROP INDEX IF EXISTS idx_freterequest_origem;"
        ),
        
        # Índices para CotacaoFrete
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS idx_cotacaofrete_status ON fretes_cotacaofrete(status);",
            reverse_sql="DROP INDEX IF EXISTS idx_cotacaofrete_status;"
        ),
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS idx_cotacaofrete_transportadora ON fretes_cotacaofrete(transportadora_id);",
            reverse_sql="DROP INDEX IF EXISTS idx_cotacaofrete_transportadora;"
        ),
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS idx_cotacaofrete_frete ON fretes_cotacaofrete(frete_id);",
            reverse_sql="DROP INDEX IF EXISTS idx_cotacaofrete_frete;"
        ),
        
        # Índices para Destino
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS idx_destino_frete ON fretes_destino(frete_id);",
            reverse_sql="DROP INDEX IF EXISTS idx_destino_frete;"
        ),
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS idx_destino_cidade ON fretes_destino(cidade);",
            reverse_sql="DROP INDEX IF EXISTS idx_destino_cidade;"
        ),
        
        # Índices para Loja
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS idx_loja_nome ON fretes_loja(nome);",
            reverse_sql="DROP INDEX IF EXISTS idx_loja_nome;"
        ),
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS idx_loja_municipio ON fretes_loja(municipio);",
            reverse_sql="DROP INDEX IF EXISTS idx_loja_municipio;"
        ),
        
        # Índices para UserProfile
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS idx_userprofile_tipo_usuario ON fretes_userprofile(tipo_usuario);",
            reverse_sql="DROP INDEX IF EXISTS idx_userprofile_tipo_usuario;"
        ),
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS idx_userprofile_transportadora ON fretes_userprofile(transportadora_id);",
            reverse_sql="DROP INDEX IF EXISTS idx_userprofile_transportadora;"
        ),
    ]
