from django.db import models

# Create your models here.

class Cliente(models.Model):
    """
    Informações do cliente
    """
    nome = models.CharField(max_length=50, default='nome')
    email = models.EmailField(max_length=100, default='email@email.com')