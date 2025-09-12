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
def format_data_entrega(value):
    """
    Converte string 'YYYY-MM-DDTHH:MM' para 'DD/MM/YYYY HH:MM'.
    Específico para data de entrega.
    """
    if not value:
        return 'Não especificada'
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
def split(value, delimiter):
    """
    Divide uma string usando um delimitador.
    """
    if not value:
        return []
    return value.split(delimiter)

@register.filter
def split_first(value, delimiter):
    """
    Divide uma string usando um delimitador e retorna apenas a primeira parte.
    """
    if not value:
        return ''
    return value.split(delimiter, 1)[0]

@register.filter
def split_last(value, delimiter):
    """
    Divide uma string usando um delimitador e retorna apenas a última parte.
    """
    if not value:
        return ''
    return value.split(delimiter, 1)[-1]

@register.filter
def format_currency(value):
    """
    Formata um valor numérico como moeda brasileira (R$ 1.234.567,89).
    """
    if not value:
        return 'R$ 0,00'
    
    try:
        # Converte para float se for string
        if isinstance(value, str):
            value = float(value.replace(',', '.'))
        
        # Formata com separadores de milhares e decimais
        formatted = f"{value:,.2f}"
        
        # Substitui vírgulas por pontos para milhares e ponto por vírgula para decimais
        formatted = formatted.replace(',', 'X').replace('.', ',').replace('X', '.')
        
        return f"R$ {formatted}"
    except (ValueError, TypeError):
        return 'R$ 0,00'