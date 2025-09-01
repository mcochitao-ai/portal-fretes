
from django.db import models
from django.contrib.auth.models import User

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
	horario_coleta = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return f"Frete #{self.id} por {self.usuario.username}"


class Destino(models.Model):
	frete = models.ForeignKey(FreteRequest, related_name='destinos', on_delete=models.CASCADE)
	endereco = models.CharField(max_length=255)
	cidade = models.CharField(max_length=100)
	estado = models.CharField(max_length=2)
	cep = models.CharField(max_length=10)
	volume = models.PositiveIntegerField(default=1)

	def __str__(self):
		return f"{self.endereco}, {self.cidade}-{self.estado} (Vol: {self.volume})"
