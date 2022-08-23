from cProfile import label
from django.db import models

class Cotacao(models.Model):
    date = models.DateField()
    base = models.CharField(max_length=45)
    rate = models.CharField(max_length=45)
    symbol = models.CharField(max_length=45)

class FormDateRange(models.Model):
    start_date = models.DateField(verbose_name='Data Início')
    end_date = models.DateField(verbose_name='Data Fim')
