from django.db import models

# Create your models here.

class Loja(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=200)
    telefone = models.CharField(max_length=20)
    email = models.EmailField()
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class DadosLoja(models.Model):
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE)
    data = models.DateField()
    vendas = models.DecimalField(max_digits=10, decimal_places=2)
    clientes = models.IntegerField()
    ticket_medio = models.DecimalField(max_digits=10, decimal_places=2)
    meta = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Campos para status dos produtos
    total_produtos = models.IntegerField(default=0)
    produtos_respondidos = models.IntegerField(default=0)
    produtos_nao_respondidos = models.IntegerField(default=0)
    produtos_gondola = models.IntegerField(default=0)
    produtos_ruptura = models.IntegerField(default=0)
    produtos_presente = models.IntegerField(default=0)
    produtos_presente_reposto = models.IntegerField(default=0)
    
    observacoes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.loja.nome} - {self.data}"

    def calcular_porcentagens(self):
        return {
            'respondidos_percent': (self.produtos_respondidos / self.total_produtos * 100) if self.total_produtos > 0 else 0,
            'nao_respondidos_percent': (self.produtos_nao_respondidos / self.total_produtos * 100) if self.total_produtos > 0 else 0,
            'gondola_percent': (self.produtos_gondola / self.total_produtos * 100) if self.total_produtos > 0 else 0,
            'ruptura_percent': (self.produtos_ruptura / self.total_produtos * 100) if self.total_produtos > 0 else 0,
            'presente_percent': (self.produtos_presente / self.total_produtos * 100) if self.total_produtos > 0 else 0,
            'presente_reposto_percent': (self.produtos_presente_reposto / self.total_produtos * 100) if self.total_produtos > 0 else 0,
        }
