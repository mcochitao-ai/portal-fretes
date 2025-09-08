# Imports organizados
import json
import openpyxl
from datetime import timedelta
from openpyxl.utils import get_column_letter

from django import forms
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django import forms
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

from .models import Loja, FreteRequest, Destino, Transportadora

# Formulário customizado para signup
class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        help_text="Obrigatório. 30 caracteres ou menos. Letras, números e @/./+/-/_ apenas.",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        help_text="Obrigatório. Digite um email válido.",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

# Views principais
def signup(request):
    """View para registro de novos usuários"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'fretes/signup.html', {'form': form})


@login_required(login_url='/login/')
def home(request):
    """Página inicial com lista de fretes e estatísticas"""
    fretes = FreteRequest.objects.select_related(
        'usuario', 'transportadora_selecionada'
    ).all().order_by('-data_criacao')
    mensagem = request.GET.get('mensagem')
    
    # Estatísticas para o resumo rápido
    estatisticas = None
    if request.user.is_authenticated:
        try:
            # Total de fretes do usuário
            total_fretes = FreteRequest.objects.filter(usuario=request.user).count()
            
            # Fretes pendentes do usuário
            fretes_pendentes = FreteRequest.objects.filter(
                usuario=request.user, 
                status='pendente'
            ).count()
            
            # Fretes finalizados do usuário
            fretes_finalizados = FreteRequest.objects.filter(
                usuario=request.user, 
                status='finalizado'
            ).count()
            
            # Fretes deste mês do usuário
            hoje = timezone.now()
            inicio_mes = hoje.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            fretes_mes = FreteRequest.objects.filter(
                usuario=request.user,
                data_criacao__gte=inicio_mes
            ).count()
            
            estatisticas = {
                'total_fretes': total_fretes,
                'fretes_pendentes': fretes_pendentes,
                'fretes_finalizados': fretes_finalizados,
                'fretes_mes': fretes_mes,
            }
            
            # Debug: imprimir no console para verificar
            print(f"DEBUG - Estatísticas para {request.user.username}:")
            print(f"  Total: {total_fretes}")
            print(f"  Pendentes: {fretes_pendentes}")
            print(f"  Finalizados: {fretes_finalizados}")
            print(f"  Este mês: {fretes_mes}")
            
        except Exception as e:
            print(f"ERRO ao calcular estatísticas: {e}")
            estatisticas = {
                'total_fretes': 0,
                'fretes_pendentes': 0,
                'fretes_finalizados': 0,
                'fretes_mes': 0,
            }
    
    return render(request, 'fretes/home.html', {
        'fretes': fretes, 
        'mensagem': mensagem,
        'estatisticas': estatisticas
    })


@login_required(login_url='/login/')
def dashboard(request):
    """Dashboard com gráficos e estatísticas"""
    hoje = timezone.now()
    meses = []
    labels = []
    
    # Preparar dados para os últimos 12 meses
    for i in range(11, -1, -1):
        mes_data = hoje - timedelta(days=30*i)
        mes = mes_data.strftime('%Y-%m')
        meses.append(mes)
        labels.append(mes_data.strftime('%m/%Y'))
    
    # Fretes por mês
    fretes_por_mes = {m: 0 for m in meses}
    for frete in FreteRequest.objects.all():
        mes = frete.data_criacao.strftime('%Y-%m')
        if mes in fretes_por_mes:
            fretes_por_mes[mes] += 1
    
    data = [fretes_por_mes[m] for m in meses]
    fretes_por_mes_json = json.dumps({'labels': labels, 'data': data})

    # Volumes por destino (top 6)
    destinos = Destino.objects.values('loja').annotate(
        total=Sum('volume')
    ).order_by('-total')[:6]
    volumes_labels = [d['loja'] for d in destinos]
    volumes_data = [d['total'] for d in destinos]
    volumes_por_destino_json = json.dumps({
        'labels': volumes_labels, 
        'data': volumes_data
    })

    # Fretes por origem (top 6)
    origens = FreteRequest.objects.values('origem__nome').annotate(
        total=Count('id')
    ).order_by('-total')[:6]
    origens_labels = [o['origem__nome'] or '-' for o in origens]
    origens_data = [o['total'] for o in origens]
    fretes_por_origem_json = json.dumps({
        'labels': origens_labels, 
        'data': origens_data
    })

    # Estatísticas para o resumo geral
    estatisticas = None
    if request.user.is_authenticated:
        try:
            # Total de fretes do usuário
            total_fretes = FreteRequest.objects.filter(usuario=request.user).count()
            
            # Fretes pendentes do usuário
            fretes_pendentes = FreteRequest.objects.filter(
                usuario=request.user, 
                status='pendente'
            ).count()
            
            # Fretes finalizados do usuário
            fretes_finalizados = FreteRequest.objects.filter(
                usuario=request.user, 
                status='finalizado'
            ).count()
            
            # Fretes deste mês do usuário
            inicio_mes = hoje.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            fretes_mes = FreteRequest.objects.filter(
                usuario=request.user,
                data_criacao__gte=inicio_mes
            ).count()
            
            estatisticas = {
                'total_fretes': total_fretes,
                'fretes_pendentes': fretes_pendentes,
                'fretes_finalizados': fretes_finalizados,
                'fretes_mes': fretes_mes,
            }
            
            # Debug: imprimir no console para verificar
            print(f"DEBUG Dashboard - Estatísticas para {request.user.username}:")
            print(f"  Total: {total_fretes}")
            print(f"  Pendentes: {fretes_pendentes}")
            print(f"  Finalizados: {fretes_finalizados}")
            print(f"  Este mês: {fretes_mes}")
            
        except Exception as e:
            print(f"ERRO ao calcular estatísticas do dashboard: {e}")
            estatisticas = {
                'total_fretes': 0,
                'fretes_pendentes': 0,
                'fretes_finalizados': 0,
                'fretes_mes': 0,
            }

    return render(request, 'fretes/dashboard.html', {
        'fretes_por_mes': fretes_por_mes_json,
        'volumes_por_destino': volumes_por_destino_json,
        'fretes_por_origem': fretes_por_origem_json,
        'estatisticas': estatisticas,
    })


# Views para criação de fretes
@login_required(login_url='/login/')
def selecionar_origem(request):
    """Tela 1: Seleção de origem"""
    lojas_qs = Loja.objects.all()
    
    def loja_numero(loja):
        try:
            return int(loja.nome)
        except (ValueError, TypeError):
            return 0
    
    lojas_list = sorted(lojas_qs, key=loja_numero)
    lojas_choices = [
        (str(loja.id), loja.nome, loja.latitude, loja.longitude) 
        for loja in lojas_list
    ]
    
    if request.method == 'POST':
        loja_id = request.POST.get('origem')
        horario_coleta = request.POST.get('horario_coleta')
        observacoes_origem = request.POST.get('observacoes_origem', '')
        if loja_id and horario_coleta:
            # Codificar as observações para URL
            import urllib.parse
            observacoes_encoded = urllib.parse.quote(observacoes_origem)
            return redirect(f"{reverse('selecionar_destino')}?origem_id={loja_id}&horario_coleta={horario_coleta}&observacoes_origem={observacoes_encoded}")
    
    return render(request, 'fretes/selecionar_origem.html', {
        'lojas_choices': lojas_choices
    })


@login_required(login_url='/login/')
def selecionar_destino(request):
    """Tela 2: Seleção de destino estruturada"""
    origem_id = request.GET.get('origem_id') or request.POST.get('origem_id')
    horario_coleta = request.GET.get('horario_coleta') or request.POST.get('horario_coleta')
    observacoes_origem = request.GET.get('observacoes_origem') or request.POST.get('observacoes_origem', '')
    
    # Decodificar as observações se vieram da URL
    if observacoes_origem and request.GET.get('observacoes_origem'):
        import urllib.parse
        observacoes_origem = urllib.parse.unquote(observacoes_origem)
    
    if not origem_id:
        return redirect('selecionar_origem')
    
    lojas_qs = Loja.objects.all()
    
    def loja_numero(loja):
        try:
            return int(loja.nome)
        except (ValueError, TypeError):
            return 0
    
    lojas_list = sorted(lojas_qs, key=loja_numero)
    lojas_choices = [
        (str(loja.id), loja.nome) 
        for loja in lojas_list 
        if str(loja.id) != str(origem_id)
    ]
    
    erro = None
    
    if request.method == 'POST':
        # Garantir que horario_coleta está disponível
        if not horario_coleta:
            horario_coleta = request.POST.get('horario_coleta') or request.GET.get('horario_coleta')
        
        destino_ids = request.POST.getlist('destino')
        descricao = request.POST.get('descricao', '')
        origem_loja = Loja.objects.filter(id=origem_id).first()
        
        if not origem_loja:
            erro = 'Origem inválida.'
        elif not destino_ids:
            erro = 'Selecione pelo menos um destino.'
        else:
            # Criar o frete
            frete = FreteRequest.objects.create(
                usuario=request.user,
                origem=origem_loja,
                descricao=descricao,
                horario_coleta=horario_coleta,
                observacoes_origem=observacoes_origem
            )
            
            # Criar os destinos
            for loja_id in destino_ids:
                loja = Loja.objects.filter(id=loja_id).first()
                if loja:
                    volume = request.POST.get(f'volume_{loja_id}', 1)
                    try:
                        volume = int(volume)
                        if volume < 1:
                            raise ValueError
                    except (ValueError, TypeError):
                        volume = 1
                    
                    observacao = request.POST.get(f'observacao_{loja_id}', '')
                    
                    Destino.objects.create(
                        frete=frete,
                        loja=loja.nome,
                        endereco=loja.endereco,
                        numero=loja.numero,
                        cidade=loja.municipio,
                        estado=loja.estado,
                        cep=loja.cep,
                        volume=volume,
                        observacao=observacao,
                    )
            
            return redirect(f"{reverse('home')}?mensagem=Frete+enviado+com+sucesso")
    
    return render(request, 'fretes/selecionar_destino.html', {
        'lojas_choices': lojas_choices,
        'origem_id': origem_id,
        'horario_coleta': horario_coleta,
        'observacoes_origem': observacoes_origem,
        'erro': erro
    })


# Views para gerenciar fretes
@login_required(login_url='/login/')
def meus_fretes(request):
    """Lista de fretes do usuário logado"""
    status = request.GET.get('status')
    search = request.GET.get('search', '').strip()
    qs = FreteRequest.objects.filter(usuario=request.user)
    
    # Filtro por status
    if status in ['pendente', 'cotacao_enviada', 'finalizado']:
        qs = qs.filter(status=status)
    
    # Filtro por pesquisa
    if search:
        from django.db.models import Q
        qs = qs.filter(
            Q(id__icontains=search) |
            Q(origem__nome__icontains=search) |
            Q(origem__municipio__icontains=search) |
            Q(descricao__icontains=search) |
            Q(destinos__loja__icontains=search) |
            Q(destinos__cidade__icontains=search)
        ).distinct()
    
    fretes = qs.order_by('-data_criacao')
    return render(request, 'fretes/meus_fretes.html', {
        'fretes': fretes, 
        'status_selected': status,
        'search_query': search
    })


@login_required(login_url='/login/')
def frete_detalhe(request, frete_id):
    """Detalhes de um frete específico"""
    frete = get_object_or_404(FreteRequest, id=frete_id)
    destinos = frete.destinos.all()
    transportadoras = Transportadora.objects.all()
    
    if request.method == 'POST':
        transportadora_id = request.POST.get('transportadora_id')
        if transportadora_id:
            transportadora = Transportadora.objects.filter(id=transportadora_id).first()
            if transportadora:
                frete.transportadora_selecionada = transportadora
                frete.save()
    
    return render(request, 'fretes/frete_detalhe.html', {
        'frete': frete,
        'destinos': destinos,
        'transportadoras': transportadoras
    })


@login_required(login_url='/login/')
@require_POST
def atualizar_status_frete(request, frete_id):
    """Atualizar status de um frete via AJAX"""
    frete = get_object_or_404(FreteRequest, id=frete_id)
    status = request.POST.get('status')
    
    if status in ['pendente', 'cotacao_enviada', 'finalizado']:
        frete.status = status
        frete.save()
        return JsonResponse({'success': True, 'status': status})
    
    return JsonResponse({
        'success': False, 
        'error': 'Status inválido'
    }, status=400)


# Views de API/AJAX
@login_required(login_url='/login/')
def loja_info(request, loja_id):
    """API para obter informações de uma loja"""
    loja = Loja.objects.filter(id=loja_id).first()
    
    if loja:
        # Formatar CEP removendo .0 se existir
        cep_formatted = str(loja.cep) if loja.cep else ''
        if cep_formatted.endswith('.0'):
            cep_formatted = cep_formatted[:-2]
        
        data = {
            'nome': loja.nome,
            'endereco': loja.endereco,
            'numero': loja.numero,
            'municipio': loja.municipio,
            'estado': loja.estado,
            'cep': cep_formatted,
            'latitude': str(loja.latitude) if loja.latitude else '',
            'longitude': str(loja.longitude) if loja.longitude else '',
        }
        return JsonResponse(data)
    
    return JsonResponse({'error': 'Loja não encontrada'}, status=404)


# Views para relatórios
@login_required(login_url='/login/')
def meus_fretes_relatorio_excel(request):
    """Gerar relatório Excel dos fretes do usuário"""
    status = request.GET.get('status')
    qs = FreteRequest.objects.select_related(
        'usuario', 'origem'
    ).prefetch_related('destinos').filter(usuario=request.user)
    
    if status in ['pendente', 'cotacao_enviada', 'finalizado']:
        qs = qs.filter(status=status)
    
    # Criar workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Fretes'
    
    # Cabeçalho
    headers = [
        'Solicitante', 'Data Solicitação da Coleta', 'Origem Loja', 
        'Origem Endereço', 'Origem Cidade', 'Origem Estado', 'Origem CEP',
        'Destino Loja', 'Destino Endereço', 'Destino Cidade', 
        'Destino Estado', 'Destino CEP', 'Volume', 'Status'
    ]
    ws.append(headers)
    
    # Dados
    for frete in qs:
        for destino in frete.destinos.all():
            ws.append([
                frete.usuario.username,
                frete.data_criacao.strftime('%d/%m/%Y %H:%M'),
                frete.origem.nome if frete.origem else '',
                frete.origem.endereco if frete.origem else '',
                frete.origem.municipio if frete.origem else '',
                frete.origem.estado if frete.origem else '',
                frete.origem.cep if frete.origem else '',
                destino.loja or '',
                destino.endereco or '',
                destino.cidade or '',
                destino.estado or '',
                destino.cep or '',
                destino.volume,
                frete.status
            ])
    
    # Ajustar largura das colunas
    for col in range(1, len(headers) + 1):
        ws.column_dimensions[get_column_letter(col)].width = 18
    
    # Preparar response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=fretes_relatorio.xlsx'
    wb.save(response)
    return response


def health_check(request):
    """Endpoint para verificação de saúde do sistema"""
    return JsonResponse({
        'status': 'ok',
        'message': 'Portal de Fretes está funcionando',
        'timestamp': timezone.now().isoformat()
    })


# Form classes
class FreteForm(forms.ModelForm):
    """Form para criação de fretes"""
    origem = forms.ChoiceField(choices=[], label='Origem')
    destino = forms.MultipleChoiceField(choices=[], label='Destino')
    horario_coleta = forms.DateTimeField(
        label='Horário de Coleta',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )

    class Meta:
        model = FreteRequest
        fields = ['descricao']


# Views para reset de senha
def forgot_password(request):
    """View para solicitar reset de senha"""
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                # Gerar token e enviar email
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                # URL para reset de senha
                reset_url = request.build_absolute_uri(
                    reverse('reset_password', kwargs={'uidb64': uid, 'token': token})
                )
                
                # Tentar enviar email, mas não falhar se não estiver configurado
                try:
                    # Enviar email
                    subject = 'Reset de Senha - Portal de Fretes'
                    message = f"""
                    Olá {user.username},
                    
                    Você solicitou um reset de senha para sua conta no Portal de Fretes.
                    
                    Clique no link abaixo para redefinir sua senha:
                    {reset_url}
                    
                    Este link é válido por 24 horas.
                    
                    Se você não solicitou este reset, ignore este email.
                    
                    Atenciosamente,
                    Equipe Portal de Fretes
                    """
                    
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        fail_silently=True,  # Não falhar se email não estiver configurado
                    )
                    
                    messages.success(request, '✅ Email de reset enviado com sucesso! Verifique sua caixa de entrada e spam.')
                    
                except Exception as e:
                    # Se falhar o envio de email, mostrar o link diretamente
                    messages.success(request, f'✅ Link de reset gerado! Como o email não está configurado, copie o link abaixo: {reset_url}')
                
                return redirect('login')
                
            except User.DoesNotExist:
                messages.error(request, '❌ Email não encontrado em nosso sistema. Verifique se digitou corretamente.')
    else:
        form = PasswordResetForm()
    
    return render(request, 'fretes/forgot_password.html', {'form': form})


def reset_password(request, uidb64, token):
    """View para resetar senha com token"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, '✅ Senha redefinida com sucesso! Faça login com sua nova senha.')
                return redirect('login')
        else:
            form = SetPasswordForm(user)
        
        return render(request, 'fretes/reset_password.html', {'form': form})
    else:
        messages.error(request, '❌ Link inválido ou expirado. Solicite um novo reset de senha.')
        return redirect('forgot_password')