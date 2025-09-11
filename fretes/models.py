from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Modelo de Loja

class Loja(models.Model):
	nome = models.CharField(max_length=100)
	endereco = models.CharField(max_length=255)
	numero = models.CharField(max_length=20)
	municipio = models.CharField(max_length=100)
	estado = models.CharField(max_length=2)
	cep = models.CharField(max_length=15, blank=True)
	regional = models.CharField(max_length=100, blank=True)
	latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

	def __str__(self):
		return self.nome

# Create your models here.

class Transportadora(models.Model):
	nome = models.CharField(max_length=100)
	email = models.EmailField()

	def __str__(self):
		return self.nome


class FreteRequest(models.Model):
	usuario = models.ForeignKey(User, on_delete=models.CASCADE)
	data_criacao = models.DateTimeField(auto_now_add=True)
	descricao = models.TextField(blank=True)
	transportadora_selecionada = models.ForeignKey(Transportadora, null=True, blank=True, on_delete=models.SET_NULL)
	origem = models.ForeignKey(Loja, null=True, blank=True, on_delete=models.SET_NULL, related_name='fretes_origem')
	horario_coleta = models.CharField(max_length=50, blank=True, null=True)
	observacoes_origem = models.TextField(blank=True, null=True, verbose_name="Observações da Coleta")
	anexo_origem = models.FileField(upload_to='anexos/origem/', blank=True, null=True, verbose_name="Anexo da Origem", help_text="Arquivo Excel ou PDF relacionado à origem")
	
	TIPO_VEICULO_CHOICES = [
		('carreta', 'Carreta'),
		('truck', 'Truck'),
		('vuc', 'VUC'),
		('toco', 'Toco'),
		('3_4', '3/4'),
		('van', 'Van'),
	]
	tipo_veiculo = models.CharField(max_length=10, choices=TIPO_VEICULO_CHOICES, blank=True, null=True, verbose_name="Tipo de Veículo", help_text="Tipo de veículo necessário para o frete")
	
	STATUS_CHOICES = [
		('pendente', 'Pendente'),
		('cotacao_enviada', 'Cotação enviada'),
		('finalizado', 'Finalizado'),
	]
	status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pendente')

	def __str__(self):
		return f"Frete #{self.id} por {self.usuario.username}"


class Destino(models.Model):
	frete = models.ForeignKey(FreteRequest, related_name='destinos', on_delete=models.CASCADE)
	endereco = models.CharField(max_length=255)
	cidade = models.CharField(max_length=100)
	estado = models.CharField(max_length=2)
	cep = models.CharField(max_length=10)
	volume = models.PositiveIntegerField(default=1)
	loja = models.CharField(max_length=100, blank=True, null=True)  # Adicione esta linha
	numero = models.CharField(max_length=20, blank=True, null=True)
	data_entrega = models.DateTimeField(blank=True, null=True, verbose_name="Data de Entrega", help_text="Data e horário previstos para entrega")
	observacao = models.TextField(blank=True, null=True)
	anexo_destino = models.FileField(upload_to='anexos/destino/', blank=True, null=True, verbose_name="Anexo do Destino", help_text="Arquivo Excel ou PDF relacionado ao destino")

	def __str__(self):
		return f"{self.endereco}, {self.cidade}-{self.estado} (Vol: {self.volume})"


# Modelo de Perfil de Usuário para definir permissões
class UserProfile(models.Model):
	ACESSO_CHOICES = [
		('limitado', 'Acesso Limitado - Apenas solicitar e ver lista'),
		('completo', 'Acesso Completo - Pode editar e ver detalhes'),
	]
	
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	tipo_acesso = models.CharField(max_length=20, choices=ACESSO_CHOICES, default='limitado', verbose_name="Tipo de Acesso")
	is_master = models.BooleanField(default=False, verbose_name="Usuário Master", help_text="Pode ver todos os fretes de todos os usuários")
	
	def __str__(self):
		return f"{self.user.username} - {self.get_tipo_acesso_display()}"
	
	def pode_editar_fretes(self):
		"""Verifica se o usuário pode editar fretes"""
		return self.tipo_acesso == 'completo'
	
	def pode_ver_detalhes_frete(self):
		"""Verifica se o usuário pode ver detalhes dos fretes"""
		return self.tipo_acesso == 'completo' or self.is_master
	
	def is_usuario_master(self):
		"""Verifica se o usuário é master (pode ver todos os fretes)"""
		return self.is_master


# Signal para criar automaticamente o perfil quando um usuário é criado
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	if hasattr(instance, 'userprofile'):
		instance.userprofile.save()
