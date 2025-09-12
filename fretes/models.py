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

	@property
	def nome_loja(self):
		"""Alias para o campo nome para compatibilidade com templates"""
		return self.nome

	@property
	def endereco_completo(self):
		"""Retorna o endereço completo formatado"""
		parts = [self.endereco]
		if self.numero:
			parts.append(self.numero)
		parts.extend([self.municipio, self.estado])
		if self.cep:
			parts.append(f"CEP: {self.cep}")
		return ", ".join(parts)

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
	
	# Campos para ajudante
	precisa_ajudante = models.BooleanField(default=False, verbose_name="Precisa de Ajudante", help_text="Indica se o frete necessita de ajudante")
	quantidade_ajudantes = models.PositiveIntegerField(default=0, verbose_name="Quantidade de Ajudantes", help_text="Número de ajudantes necessários")
	
	# Campos para nota fiscal e pagamento
	nota_fiscal_emitida = models.BooleanField(default=False, verbose_name="Nota Fiscal Emitida", help_text="Indica se a nota fiscal já foi emitida")
	anexo_nota_fiscal = models.FileField(upload_to='anexos/nota_fiscal/', blank=True, null=True, verbose_name="Anexo da Nota Fiscal", help_text="Arquivo da nota fiscal (PDF, Excel)")
	quem_paga_frete = models.CharField(max_length=100, blank=True, null=True, verbose_name="Quem Paga o Frete", help_text="Loja responsável pelo pagamento do frete")
	
	STATUS_CHOICES = [
		('pendente', 'Pendente'),
		('cotacao_enviada', 'Cotação Enviada'),
		('cotacao_recebida', 'Cotação Recebida'),
		('cotacao_aprovada', 'Cotação Aprovada'),
		('rejeitado', 'Rejeitado'),
		('rejeitado_transportadora', 'Rejeitado pela Transportadora'),
		('cancelado', 'Cancelado'),
		('finalizado', 'Finalizado'),
	]
	status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pendente')
	
	# Campos para aprovação
	centro_custo = models.CharField(max_length=100, blank=True, null=True, verbose_name="Centro de Custo", help_text="Centro de custo aprovado para o frete")
	aprovador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='fretes_aprovados', verbose_name="Aprovador")
	data_aprovacao = models.DateTimeField(null=True, blank=True, verbose_name="Data de Aprovação")
	observacoes_aprovacao = models.TextField(blank=True, null=True, verbose_name="Observações da Aprovação")
	justificativa_rejeicao = models.TextField(blank=True, null=True, verbose_name="Justificativa da Rejeição")
	
	# Campos para cancelamento
	motivo_cancelamento = models.TextField(blank=True, null=True, verbose_name="Motivo do Cancelamento", help_text="Justificativa para o cancelamento do frete")
	usuario_cancelamento = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='fretes_cancelados', verbose_name="Usuário que Cancelou")
	data_cancelamento = models.DateTimeField(null=True, blank=True, verbose_name="Data do Cancelamento")
	
	# Campos para cotação (mantidos para compatibilidade)
	transportadora = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='fretes_cotados', verbose_name="Transportadora", help_text="Transportadora responsável pela cotação")
	valor_frete = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Valor do Frete", help_text="Valor cobrado pelo frete")
	valor_pedagio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Valor do Pedágio", help_text="Valor cobrado pelo pedágio")
	valor_ajudante = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Valor do Ajudante", help_text="Valor cobrado pelo ajudante")
	valor_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Valor Total", help_text="Soma total da cotação")
	data_cotacao = models.DateTimeField(null=True, blank=True, verbose_name="Data da Cotação")
	observacoes_cotacao = models.TextField(blank=True, null=True, verbose_name="Observações da Cotação")
	motivo_rejeicao_transportadora = models.TextField(blank=True, null=True, verbose_name="Motivo da Rejeição pela Transportadora")

	def calcular_valor_total(self):
		"""Calcula o valor total da cotação"""
		total = 0
		if self.valor_frete:
			total += self.valor_frete
		if self.valor_pedagio:
			total += self.valor_pedagio
		if self.valor_ajudante:
			total += self.valor_ajudante
		return total
	
	def save(self, *args, **kwargs):
		# Calcular valor total automaticamente
		if self.valor_frete or self.valor_pedagio or self.valor_ajudante:
			self.valor_total = self.calcular_valor_total()
		super().save(*args, **kwargs)

	def __str__(self):
		return f"Frete #{self.id} por {self.usuario.username}"


class CotacaoFrete(models.Model):
	"""Modelo para cotações de múltiplas transportadoras para um frete"""
	frete = models.ForeignKey(FreteRequest, on_delete=models.CASCADE, related_name='cotacoes')
	transportadora = models.ForeignKey(Transportadora, on_delete=models.CASCADE, related_name='cotacoes_feitas')
	
	# Valores da cotação
	valor_frete = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Valor do Frete")
	valor_pedagio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Valor do Pedágio")
	valor_ajudante = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Valor do Ajudante")
	valor_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Valor Total")
	
	# Status da cotação
	STATUS_COTACAO_CHOICES = [
		('pendente', 'Pendente'),
		('enviada', 'Enviada'),
		('aprovada', 'Aprovada'),
		('rejeitada', 'Rejeitada'),
		('rejeitada_transportadora', 'Rejeitada pela Transportadora'),
	]
	status = models.CharField(max_length=30, choices=STATUS_COTACAO_CHOICES, default='pendente')
	
	# Datas e observações
	data_cotacao = models.DateTimeField(null=True, blank=True, verbose_name="Data da Cotação")
	observacoes_cotacao = models.TextField(blank=True, null=True, verbose_name="Observações da Cotação")
	motivo_rejeicao_transportadora = models.TextField(blank=True, null=True, verbose_name="Motivo da Rejeição pela Transportadora")
	
	# Aprovação
	aprovador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='cotacoes_aprovadas', verbose_name="Aprovador")
	data_aprovacao = models.DateTimeField(null=True, blank=True, verbose_name="Data de Aprovação")
	observacoes_aprovacao = models.TextField(blank=True, null=True, verbose_name="Observações da Aprovação")
	justificativa_rejeicao = models.TextField(blank=True, null=True, verbose_name="Justificativa da Rejeição")
	
	def calcular_valor_total(self):
		"""Calcula o valor total da cotação"""
		total = 0
		if self.valor_frete:
			total += self.valor_frete
		if self.valor_pedagio:
			total += self.valor_pedagio
		if self.valor_ajudante:
			total += self.valor_ajudante
		return total
	
	def save(self, *args, **kwargs):
		# Calcular valor total automaticamente
		if self.valor_frete or self.valor_pedagio or self.valor_ajudante:
			self.valor_total = self.calcular_valor_total()
		super().save(*args, **kwargs)
	
	def __str__(self):
		return f"Cotação #{self.id} - Frete #{self.frete.id} - {self.transportadora.username}"


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

	@property
	def endereco_completo(self):
		"""Retorna o endereço completo formatado"""
		parts = [self.endereco]
		if self.numero:
			parts.append(self.numero)
		parts.extend([self.cidade, self.estado])
		if self.cep:
			parts.append(f"CEP: {self.cep}")
		return ", ".join(parts)

	def __str__(self):
		return f"{self.endereco}, {self.cidade}-{self.estado} (Vol: {self.volume})"


# Modelo de Perfil de Usuário para definir permissões
class UserProfile(models.Model):
	ACESSO_CHOICES = [
		('limitado', 'Acesso Limitado - Apenas solicitar e ver lista'),
		('completo', 'Acesso Completo - Pode editar e ver detalhes'),
	]
	
	TIPO_USUARIO_CHOICES = [
		('master', 'Usuário Master'),
		('gerente', 'Gerente'),
		('solicitante', 'Solicitante'),
		('transportadora', 'Transportadora'),
	]
	
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	tipo_acesso = models.CharField(max_length=20, choices=ACESSO_CHOICES, default='limitado', verbose_name="Tipo de Acesso")
	is_master = models.BooleanField(default=False, verbose_name="Usuário Master", help_text="Pode ver todos os fretes de todos os usuários")
	tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES, default='solicitante', verbose_name="Tipo de Usuário")
	transportadora = models.ForeignKey(Transportadora, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Transportadora", help_text="Transportadora associada ao usuário")
	
	def __str__(self):
		return f"{self.user.username} - {self.get_tipo_acesso_display()}"
	
	def pode_editar_fretes(self):
		"""Verifica se o usuário pode editar fretes"""
		return self.tipo_acesso == 'completo'
	
	def pode_ver_detalhes_frete(self):
		"""Verifica se o usuário pode ver detalhes dos fretes"""
		return self.tipo_acesso == 'completo' or self.is_master
	
	def is_usuario_master(self):
		"""Verifica se é usuário master"""
		return self.is_master or self.tipo_usuario == 'master'
	
	def is_gerente(self):
		"""Verifica se é gerente"""
		return self.tipo_usuario == 'gerente'
	
	def is_solicitante(self):
		"""Verifica se é solicitante"""
		return self.tipo_usuario == 'solicitante'
	
	def is_transportadora(self):
		"""Verifica se é transportadora"""
		return self.tipo_usuario == 'transportadora'


# Signal para criar automaticamente o perfil quando um usuário é criado
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	if hasattr(instance, 'userprofile'):
		instance.userprofile.save()
