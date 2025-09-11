from django import template
import datetime

register = template.Library()

@register.filter
def format_horario_coleta(value):
    """
    Converte string 'YYYY-MM-DDTHH:MM' para 'DD/MM/YYYY HH:MM'.
    Se não for possível converter, retorna o valor original.
    """
    if not value:
        return ''
    try:
        # Aceita tanto 'YYYY-MM-DDTHH:MM' quanto 'YYYY-MM-DD HH:MM'
        if 'T' in value:
            dt = datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M')
        else:
            dt = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M')
        return dt.strftime('%d/%m/%Y %H:%M')
    except Exception:
        return value

@register.filter
def format_cep(value):
    """
    Remove o .0 do final do CEP e formata como string limpa.
    """
    if not value:
        return ''
    
    # Converte para string e remove .0 se existir
    cep_str = str(value)
    if cep_str.endswith('.0'):
        cep_str = cep_str[:-2]
    
    # Remove espaços e caracteres especiais
    cep_clean = ''.join(filter(str.isdigit, cep_str))
    
    # Formata como CEP brasileiro (12345-678)
    if len(cep_clean) == 8:
        return f"{cep_clean[:5]}-{cep_clean[5:]}"
    
    return cep_clean

@register.filter
def split(value, delimiter):
    """
    Divide uma string usando um delimitador.
    """
    if not value:
        return []
    return value.split(delimiter)