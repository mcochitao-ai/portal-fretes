from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Tela 1: Seleção de origem
@login_required(login_url='/login/')
def selecionar_origem(request):
	lojas_qs = Loja.objects.all()
	lojas_list = sorted(lojas_qs, key=lambda l: int(l.nome) if str(l.nome).isdigit() else 0)
	lojas_choices = [(str(loja.id), loja.nome, loja.latitude, loja.longitude) for loja in lojas_list]
	if request.method == 'POST':
		loja_id = request.POST.get('origem')
		horario_coleta = request.POST.get('horario_coleta')
		if loja_id and horario_coleta:
			# Passar dados via GET para a próxima tela
			return redirect(f"{reverse('selecionar_destino')}?origem_id={loja_id}&horario_coleta={horario_coleta}")
	return render(request, 'fretes/selecionar_origem.html', {'lojas_choices': lojas_choices})


# Tela 2: Seleção de destino estruturada
@login_required(login_url='/login/')
def selecionar_destino(request):
	origem_id = request.GET.get('origem_id') or request.POST.get('origem_id')
	horario_coleta = request.GET.get('horario_coleta') or request.POST.get('horario_coleta')
	if not origem_id or not horario_coleta:
		return redirect('selecionar_origem')
	lojas_qs = Loja.objects.all()
	def loja_numero(loja):
		try:
			return int(loja.nome)
		except (ValueError, TypeError):
			return 0
	lojas_list = sorted(lojas_qs, key=loja_numero)
	lojas_choices = [(str(loja.id), loja.nome) for loja in lojas_list if str(loja.id) != str(origem_id)]
	if request.method == 'POST':
		destino_ids = request.POST.getlist('destino')
		descricao = request.POST.get('descricao')
		origem_loja = Loja.objects.filter(id=origem_id).first()
		frete = FreteRequest.objects.create(
			usuario=request.user,
			origem=origem_loja,
			descricao=descricao,
			horario_coleta=horario_coleta
		)
		for loja_id in destino_ids:
			loja = Loja.objects.filter(id=loja_id).first()
			if loja:
				volume = request.POST.get(f'volume_{loja_id}', 1)
				try:
					volume = int(volume)
				except Exception:
					volume = 1
				Destino.objects.create(
					frete=frete,
					endereco=loja.nome,
					cidade=loja.municipio,
					estado=loja.estado,
					cep=loja.cep,
					volume=volume
				)
		return redirect('home')
	return render(request, 'fretes/selecionar_destino.html', {'lojas_choices': lojas_choices, 'origem_id': origem_id, 'horario_coleta': horario_coleta})
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Loja, FreteRequest, Destino

@login_required(login_url='/login/')
def loja_info(request, loja_id):
	loja = Loja.objects.filter(id=loja_id).first()
	if loja:
		data = {
			'endereco': loja.endereco,
			'numero': loja.numero,
			'municipio': loja.municipio,
			'estado': loja.estado,
			'latitude': str(loja.latitude) if loja.latitude else '',
			'longitude': str(loja.longitude) if loja.longitude else '',
		}
		return JsonResponse(data)
	return JsonResponse({'error': 'Loja não encontrada'}, status=404)
from django.contrib.auth import login as auth_login
from django import forms


@login_required(login_url='/login/')
def meus_fretes(request):
	fretes = FreteRequest.objects.filter(usuario=request.user).order_by('-data_criacao')
	return render(request, 'fretes/meus_fretes.html', {'fretes': fretes})

from .models import Transportadora

@login_required(login_url='/login/')
def frete_detalhe(request, frete_id):
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

class FreteForm(forms.ModelForm):
	origem = forms.ChoiceField(choices=[], label='Origem')
	destino = forms.MultipleChoiceField(choices=[], label='Destino')
	horario_coleta = forms.DateTimeField(label='Horário de Coleta', widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

	class Meta:
		model = FreteRequest
		fields = ['descricao']


# --- Nova view para selecionar origem ---
from django.urls import reverse

@login_required(login_url='/login/')
def selecionar_origem(request):
	lojas_qs = Loja.objects.all()
	def loja_numero(loja):
		try:
			return int(loja.nome)
		except (ValueError, TypeError):
			return 0
	lojas_list = sorted(lojas_qs, key=loja_numero)
	lojas_choices = [(str(loja.id), loja.nome, loja.latitude, loja.longitude) for loja in lojas_list]
	if request.method == 'POST':
		origem_id = request.POST.get('origem')
		if origem_id:
			return redirect(reverse('selecionar_destino') + f'?origem_id={origem_id}')
	return render(request, 'fretes/selecionar_origem.html', {'lojas_choices': lojas_choices})

# --- Nova view para selecionar destinos e finalizar frete ---
@login_required(login_url='/login/')
def selecionar_destino(request):
	origem_id = request.GET.get('origem_id') or request.POST.get('origem_id')
	if not origem_id:
		return redirect('selecionar_origem')
	lojas_qs = Loja.objects.all()
	def loja_numero(loja):
		try:
			return int(loja.nome)
		except (ValueError, TypeError):
			return 0
	lojas_list = sorted(lojas_qs, key=loja_numero)
	lojas_choices = [(str(loja.id), loja.nome) for loja in lojas_list if str(loja.id) != str(origem_id)]
	mensagem = None
	erro = None
	horario_coleta = request.GET.get('horario_coleta') or request.POST.get('horario_coleta')
	if request.method == 'POST':
		destino_ids = request.POST.getlist('destino')
		descricao = request.POST.get('descricao')
		origem_loja = Loja.objects.filter(id=origem_id).first()
		if not origem_loja:
			erro = 'Origem inválida.'
		elif not destino_ids:
			erro = 'Selecione pelo menos um destino.'
		elif not horario_coleta:
			erro = 'Informe o horário de coleta.'
		else:
			frete = FreteRequest.objects.create(
				usuario=request.user,
				origem=origem_loja,
				descricao=descricao,
				horario_coleta=horario_coleta
			)
			for loja_id in destino_ids:
				loja = Loja.objects.filter(id=loja_id).first()
				if loja:
					volume = request.POST.get(f'volume_{loja_id}', 1)
					try:
						volume = int(volume)
						if volume < 1:
							raise ValueError
					except Exception:
						volume = 1
					Destino.objects.create(
						frete=frete,
						endereco=loja.nome,
						cidade=loja.municipio,
						estado=loja.estado,
						cep=loja.cep,
						volume=volume
					)
			return redirect(f"{reverse('home')}?mensagem=Frete+enviado+com+sucesso")
	return render(request, 'fretes/selecionar_destino.html', {
		'lojas_choices': lojas_choices,
		'origem_id': origem_id,
		'horario_coleta': horario_coleta,
		'erro': erro
	})

def signup(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			auth_login(request, user)
			return redirect('home')
	else:
		form = UserCreationForm()
	return render(request, 'fretes/signup.html', {'form': form})

@login_required(login_url='/login/')
def home(request):
	fretes = FreteRequest.objects.select_related('usuario', 'transportadora_selecionada').all().order_by('-data_criacao')
	mensagem = request.GET.get('mensagem')
	return render(request, 'fretes/home.html', {'fretes': fretes, 'mensagem': mensagem})
