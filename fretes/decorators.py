"""
Decorators para otimização de performance
"""
from functools import wraps
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
import hashlib


def cache_view(timeout=300, cache_key_prefix='view_cache'):
    """
    Decorator para cache de views com chave personalizada
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Criar chave de cache baseada na URL e parâmetros
            cache_key = f"{cache_key_prefix}_{request.path}_{hashlib.md5(str(request.GET).encode()).hexdigest()}"
            
            # Tentar obter do cache
            cached_response = cache.get(cache_key)
            if cached_response is not None:
                return cached_response
            
            # Executar view e cachear resultado
            response = view_func(request, *args, **kwargs)
            cache.set(cache_key, response, timeout)
            return response
        return wrapper
    return decorator


def cache_static_data(timeout=1800):
    """
    Decorator para cache de dados estáticos (lojas, transportadoras, etc.)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"static_{func.__name__}_{hashlib.md5(str(args).encode()).hexdigest()}"
            
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            result = func(*args, **kwargs)
            cache.set(cache_key, result, timeout)
            return result
        return wrapper
    return decorator


# Decorators específicos para diferentes tipos de cache
cache_short = cache_view(timeout=300, cache_key_prefix='short')
cache_medium = cache_view(timeout=900, cache_key_prefix='medium')
cache_long = cache_view(timeout=1800, cache_key_prefix='long')
cache_static = cache_view(timeout=3600, cache_key_prefix='static')
