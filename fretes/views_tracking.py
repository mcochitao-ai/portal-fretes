# Views de Agendamento e Tracking
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import connection
from .models import FreteRequest, AgendamentoFrete, TrackingFrete, UserProfile


def ensure_tables_exist():
    """Garante que as tabelas de agendamento e tracking existam"""
    try:
        with connection.cursor() as cursor:
            # Verificar se a tabela AgendamentoFrete existe
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'fretes_agendamentofrete'
                );
            """)
            agendamento_exists = cursor.fetchone()[0]
            
            # Verificar se a tabela TrackingFrete existe
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'fretes_trackingfrete'
                );
            """)
            tracking_exists = cursor.fetchone()[0]
            
            if not agendamento_exists:
                # Criar tabela AgendamentoFrete
                cursor.execute("""
                    CREATE TABLE fretes_agendamentofrete (
                        id SERIAL PRIMARY KEY,
                        frete_id INTEGER UNIQUE NOT NULL,
                        transportadora_id INTEGER NOT NULL,
                        placa_veiculo VARCHAR(10) NOT NULL,
                        modelo_veiculo VARCHAR(100) NOT NULL,
                        cor_veiculo VARCHAR(50) NOT NULL,
                        motorista_nome VARCHAR(100) NOT NULL,
                        motorista_cpf VARCHAR(14) NOT NULL,
                        motorista_telefone VARCHAR(20) NOT NULL,
                        data_coleta TIMESTAMP WITH TIME ZONE NOT NULL,
                        data_entrega_prevista TIMESTAMP WITH TIME ZONE NOT NULL,
                        observacoes_agendamento TEXT,
                        data_agendamento TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                        usuario_agendamento_id INTEGER NOT NULL,
                        FOREIGN KEY (frete_id) REFERENCES fretes_freterequest(id) ON DELETE CASCADE,
                        FOREIGN KEY (transportadora_id) REFERENCES fretes_transportadora(id) ON DELETE CASCADE,
                        FOREIGN KEY (usuario_agendamento_id) REFERENCES auth_user(id) ON DELETE CASCADE
                    );
                """)
                
            if not tracking_exists:
                # Criar tabela TrackingFrete
                cursor.execute("""
                    CREATE TABLE fretes_trackingfrete (
                        id SERIAL PRIMARY KEY,
                        agendamento_id INTEGER NOT NULL,
                        status VARCHAR(20) NOT NULL,
                        data_atualizacao TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                        localizacao_atual VARCHAR(255),
                        observacoes TEXT,
                        usuario_atualizacao_id INTEGER NOT NULL,
                        tipo_problema VARCHAR(100),
                        descricao_problema TEXT,
                        FOREIGN KEY (agendamento_id) REFERENCES fretes_agendamentofrete(id) ON DELETE CASCADE,
                        FOREIGN KEY (usuario_atualizacao_id) REFERENCES auth_user(id) ON DELETE CASCADE
                    );
                """)
                
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
        pass


@login_required(login_url='/login/')
def fretes_para_agendamento(request):
    """Lista de fretes aprovados que precisam ser agendados"""
    ensure_tables_exist()  # Garantir que as tabelas existam
    try:
        user_profile = request.user.userprofile
        if not (user_profile.is_transportadora() or user_profile.is_usuario_master()):
            messages.error(request, 'Você não tem permissão para acessar esta área.')
            return redirect('home')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Perfil de usuário não encontrado.')
        return redirect('home')
    
    # Buscar fretes com status 'cotacao_aprovada' da transportadora do usuário
    if user_profile.is_usuario_master():
        # Master vê todos os fretes aprovados
        fretes_para_agendamento = FreteRequest.objects.filter(
            status='cotacao_aprovada'
        ).select_related(
            'usuario', 'origem', 'transportadora_selecionada'
        ).prefetch_related(
            'destinos', 'cotacoes__transportadora'
        ).order_by('-data_criacao')
    else:
        # Transportadora vê apenas seus fretes aprovados
        if user_profile.transportadora:
            fretes_para_agendamento = FreteRequest.objects.filter(
                status='cotacao_aprovada',
                transportadora_selecionada=user_profile.transportadora
            ).select_related(
                'usuario', 'origem', 'transportadora_selecionada'
            ).prefetch_related(
                'destinos', 'cotacoes__transportadora'
            ).order_by('-data_criacao')
        else:
            fretes_para_agendamento = FreteRequest.objects.none()
    
    # Estatísticas
    total_para_agendamento = fretes_para_agendamento.count()
    fretes_agendados = FreteRequest.objects.filter(
        status='agendado',
        transportadora_selecionada=user_profile.transportadora if user_profile.transportadora else None
    ).count() if not user_profile.is_usuario_master() else FreteRequest.objects.filter(status='agendado').count()
    
    return render(request, 'fretes/fretes_para_agendamento.html', {
        'fretes_para_agendamento': fretes_para_agendamento,
        'total_para_agendamento': total_para_agendamento,
        'fretes_agendados': fretes_agendados,
        'user_profile': user_profile
    })


@login_required(login_url='/login/')
def agendar_frete(request, frete_id):
    """Tela para o transportador agendar o frete"""
    ensure_tables_exist()  # Garantir que as tabelas existam
    try:
        user_profile = request.user.userprofile
        if not (user_profile.is_transportadora() or user_profile.is_usuario_master()):
            messages.error(request, 'Você não tem permissão para acessar esta área.')
            return redirect('home')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Perfil de usuário não encontrado.')
        return redirect('home')
    
    frete = get_object_or_404(FreteRequest, id=frete_id)
    
    # Verificar se o frete pode ser agendado
    if frete.status != 'cotacao_aprovada':
        messages.error(request, 'Este frete não está disponível para agendamento.')
        return redirect('fretes_para_agendamento')
    
    # Verificar se a transportadora pode agendar este frete
    if not user_profile.is_usuario_master() and frete.transportadora_selecionada != user_profile.transportadora:
        messages.error(request, 'Você não tem permissão para agendar este frete.')
        return redirect('fretes_para_agendamento')
    
    # Verificar se já existe agendamento
    if hasattr(frete, 'agendamento'):
        messages.info(request, 'Este frete já foi agendado.')
        return redirect('tracking_frete', frete_id=frete.id)
    
    destinos = frete.destinos.all()
    
    if request.method == 'POST':
        # Processar formulário de agendamento
        placa_veiculo = request.POST.get('placa_veiculo', '').strip().upper()
        modelo_veiculo = request.POST.get('modelo_veiculo', '').strip()
        cor_veiculo = request.POST.get('cor_veiculo', '').strip()
        motorista_nome = request.POST.get('motorista_nome', '').strip()
        motorista_cpf = request.POST.get('motorista_cpf', '').strip()
        motorista_telefone = request.POST.get('motorista_telefone', '').strip()
        data_coleta = request.POST.get('data_coleta')
        data_entrega_prevista = request.POST.get('data_entrega_prevista')
        observacoes_agendamento = request.POST.get('observacoes_agendamento', '').strip()
        
        # Validações
        if not all([placa_veiculo, modelo_veiculo, cor_veiculo, motorista_nome, motorista_cpf, motorista_telefone, data_coleta, data_entrega_prevista]):
            messages.error(request, 'Todos os campos obrigatórios devem ser preenchidos.')
            return render(request, 'fretes/agendar_frete.html', {
                'frete': frete,
                'destinos': destinos
            })
        
        try:
            from datetime import datetime
            data_coleta_dt = datetime.strptime(data_coleta, '%Y-%m-%dT%H:%M')
            data_entrega_dt = datetime.strptime(data_entrega_prevista, '%Y-%m-%dT%H:%M')
            
            # Criar agendamento
            agendamento = AgendamentoFrete.objects.create(
                frete=frete,
                transportadora=frete.transportadora_selecionada,
                placa_veiculo=placa_veiculo,
                modelo_veiculo=modelo_veiculo,
                cor_veiculo=cor_veiculo,
                motorista_nome=motorista_nome,
                motorista_cpf=motorista_cpf,
                motorista_telefone=motorista_telefone,
                data_coleta=data_coleta_dt,
                data_entrega_prevista=data_entrega_dt,
                observacoes_agendamento=observacoes_agendamento,
                usuario_agendamento=request.user
            )
            
            # Criar primeiro registro de tracking
            TrackingFrete.objects.create(
                agendamento=agendamento,
                status='agendado',
                localizacao_atual=frete.origem.nome if frete.origem else 'Origem',
                observacoes='Frete agendado com sucesso',
                usuario_atualizacao=request.user
            )
            
            # Atualizar status do frete
            frete.status = 'agendado'
            frete.save()
            
            messages.success(request, f'Frete #{frete.id} agendado com sucesso!')
            return redirect('tracking_frete', frete_id=frete.id)
            
        except ValueError:
            messages.error(request, 'Formato de data inválido.')
            return render(request, 'fretes/agendar_frete.html', {
                'frete': frete,
                'destinos': destinos
            })
        except Exception as e:
            messages.error(request, f'Erro ao agendar frete: {str(e)}')
            return render(request, 'fretes/agendar_frete.html', {
                'frete': frete,
                'destinos': destinos
            })
    
    return render(request, 'fretes/agendar_frete.html', {
        'frete': frete,
        'destinos': destinos
    })


@login_required(login_url='/login/')
def tracking_frete(request, frete_id):
    """Dashboard de tracking para acompanhar o frete"""
    ensure_tables_exist()  # Garantir que as tabelas existam
    frete = get_object_or_404(FreteRequest, id=frete_id)
    agendamento = getattr(frete, 'agendamento', None)
    
    if not agendamento:
        messages.error(request, 'Frete não foi agendado ainda.')
        return redirect('meus_fretes')
    
    # Verificar permissões
    try:
        user_profile = request.user.userprofile
        pode_ver = (
            user_profile.is_usuario_master() or
            user_profile.is_gerente() or
            frete.usuario == request.user or
            (user_profile.is_transportadora() and agendamento.transportadora == user_profile.transportadora)
        )
        
        if not pode_ver:
            messages.error(request, 'Você não tem permissão para ver este tracking.')
            return redirect('home')
    except UserProfile.DoesNotExist:
        if frete.usuario != request.user:
            messages.error(request, 'Você não tem permissão para ver este tracking.')
            return redirect('home')
    
    # Buscar histórico de tracking
    tracking_history = TrackingFrete.objects.filter(agendamento=agendamento).order_by('-data_atualizacao')
    status_atual = tracking_history.first() if tracking_history.exists() else None
    
    return render(request, 'fretes/tracking_frete.html', {
        'frete': frete,
        'agendamento': agendamento,
        'tracking_history': tracking_history,
        'status_atual': status_atual
    })


@login_required(login_url='/login/')
def fretes_em_tracking(request):
    """Lista de fretes em tracking para o transportador"""
    ensure_tables_exist()  # Garantir que as tabelas existam
    try:
        user_profile = request.user.userprofile
        if not (user_profile.is_transportadora() or user_profile.is_usuario_master()):
            messages.error(request, 'Você não tem permissão para acessar esta área.')
            return redirect('home')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Perfil de usuário não encontrado.')
        return redirect('home')
    
    # Buscar fretes com agendamento da transportadora do usuário
    if user_profile.is_usuario_master():
        # Master vê todos os fretes em tracking
        fretes_em_tracking = FreteRequest.objects.filter(
            status__in=['agendado', 'em_transito', 'entregue']
        ).select_related(
            'usuario', 'origem', 'transportadora_selecionada'
        ).prefetch_related(
            'destinos', 'agendamento__tracking'
        ).order_by('-data_criacao')
    else:
        # Transportadora vê apenas seus fretes em tracking
        if user_profile.transportadora:
            fretes_em_tracking = FreteRequest.objects.filter(
                status__in=['agendado', 'em_transito', 'entregue'],
                transportadora_selecionada=user_profile.transportadora
            ).select_related(
                'usuario', 'origem', 'transportadora_selecionada'
            ).prefetch_related(
                'destinos', 'agendamento__tracking'
            ).order_by('-data_criacao')
        else:
            fretes_em_tracking = FreteRequest.objects.none()
    
    # Estatísticas
    total_em_tracking = fretes_em_tracking.count()
    fretes_agendados = fretes_em_tracking.filter(status='agendado').count()
    fretes_em_transito = fretes_em_tracking.filter(status='em_transito').count()
    fretes_entregues = fretes_em_tracking.filter(status='entregue').count()
    
    return render(request, 'fretes/fretes_em_tracking.html', {
        'fretes_em_tracking': fretes_em_tracking,
        'total_em_tracking': total_em_tracking,
        'fretes_agendados': fretes_agendados,
        'fretes_em_transito': fretes_em_transito,
        'fretes_entregues': fretes_entregues,
        'user_profile': user_profile
    })


@login_required(login_url='/login/')
def atualizar_tracking(request, frete_id):
    """Atualizar status do tracking"""
    ensure_tables_exist()  # Garantir que as tabelas existam
    frete = get_object_or_404(FreteRequest, id=frete_id)
    agendamento = getattr(frete, 'agendamento', None)
    
    if not agendamento:
        return JsonResponse({'error': 'Frete não agendado'}, status=400)
    
    # Verificar permissões
    try:
        user_profile = request.user.userprofile
        if not (user_profile.is_transportadora() or user_profile.is_usuario_master()):
            return JsonResponse({'error': 'Sem permissão'}, status=403)
        
        if not user_profile.is_usuario_master() and agendamento.transportadora != user_profile.transportadora:
            return JsonResponse({'error': 'Sem permissão para este frete'}, status=403)
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'Perfil não encontrado'}, status=403)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        localizacao = request.POST.get('localizacao', '').strip()
        observacoes = request.POST.get('observacoes', '').strip()
        tipo_problema = request.POST.get('tipo_problema', '').strip()
        descricao_problema = request.POST.get('descricao_problema', '').strip()
        
        if not status:
            return JsonResponse({'error': 'Status é obrigatório'}, status=400)
        
        try:
            # Criar novo registro de tracking
            tracking = TrackingFrete.objects.create(
                agendamento=agendamento,
                status=status,
                localizacao_atual=localizacao,
                observacoes=observacoes,
                usuario_atualizacao=request.user,
                tipo_problema=tipo_problema if status == 'problema' else None,
                descricao_problema=descricao_problema if status == 'problema' else None
            )
            
            # Atualizar status do frete principal
            if status == 'entregue':
                frete.status = 'entregue'
                frete.save()
            elif status == 'em_transito':
                frete.status = 'em_transito'
                frete.save()
            elif status == 'cancelado':
                frete.status = 'cancelado'
                frete.save()
            
            return JsonResponse({
                'success': True, 
                'tracking_id': tracking.id,
                'status': tracking.get_status_display(),
                'data_atualizacao': tracking.data_atualizacao.strftime('%d/%m/%Y %H:%M')
            })
            
        except Exception as e:
            return JsonResponse({'error': f'Erro ao atualizar tracking: {str(e)}'}, status=500)
    
    return render(request, 'fretes/atualizar_tracking.html', {
        'frete': frete,
        'agendamento': agendamento
    })
