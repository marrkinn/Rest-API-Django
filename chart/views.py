from email import message
from urllib import response
from django.shortcuts import render
from chart.models import *
from chart.forms import *
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import json
from datetime import datetime, date, timedelta
from django.core import serializers


class ViewCotacao(APIView):

    form_dates = FormDate

    def get(self, request, *args, **kwargs):
        form = self.form_dates()
        messages = []
        # Inicializando datas para a pagina
        end_date = date.today()
        start_date = end_date - timedelta(days=5)

        # Fazendo requisicoes com o range das datas
        for single_date in daterange(start_date, end_date):
            if single_date.weekday() not in (5, 6):
                # print(single_date.strftime("%Y-%m-%d"))
                data = requests.get('https://api.vatcomply.com/rates?base=USD&symbols=EUR,JPY,BRL&date=' + str(single_date))
                data_status = data.status_code

                # Testando conexao
                if data_status == 200:
                    for cote in data:
                        cote = json.loads(cote)
                        date_cotacao = cote["date"]
                        base = cote["base"]

                        for moeda in cote["rates"]:
                            symbol = str(moeda)
                            rate = cote["rates"][moeda]
                            check_register(date_cotacao, base, symbol, rate)

        # Formatando QuerySet para Json
        response = serializers.serialize("json", Cotacao.objects.filter(date__range=[start_date, end_date]))

        return render(request, 'html/chart.html', {'response':response, 'form':form, 'messages':messages})
    
    def post(self, request, *args, **kwargs):
        form = self.form_dates()
        response = {}
        form_post = request.POST
        messages = []
        try:
            start_date = datetime.strptime(form_post['start_date'], "%Y-%m-%d").date()
            end_date = datetime.strptime(form_post['end_date'], "%Y-%m-%d").date()
            count_day = 0
            if(int((end_date - start_date).days) > 5):
                messages = "Exibindo intervalo máximo de 5 dias úteis a partir da Data Início"
                for single_date in daterange(start_date, end_date):
                    if count_day == 5:
                        end_date = single_date
                    if single_date.weekday() not in (5, 6):
                        count_day += 1
            if(int((end_date - start_date).days) < 0):
                messages = "Data Início maior que Data Fim"

            # Fazendo requisicoes com o range das datas
            for single_date in daterange(start_date, end_date):
                if single_date.weekday() not in (5, 6):
                    # print(single_date.strftime("%Y-%m-%d"))
                    data = requests.get('https://api.vatcomply.com/rates?base=USD&symbols=EUR,JPY,BRL&date=' + str(single_date))
                    data_status = data.status_code

                    # Testando conexao
                    if data_status == 200:
                        for cote in data:
                            cote = json.loads(cote)
                            date_cotacao = cote["date"]
                            base = cote["base"]

                            for moeda in cote["rates"]:
                                symbol = str(moeda)
                                rate = cote["rates"][moeda]
                                check_register(date_cotacao, base, symbol, rate)

            # Formatando QuerySet para Json
            response = serializers.serialize("json", Cotacao.objects.filter(date__range=[start_date, end_date]))

        except Exception as ex:
            end_date = date.today()
            start_date = end_date - timedelta(days=5)

            # Fazendo requisicoes com o range das datas
            for single_date in daterange(start_date, end_date):
                if single_date.weekday() not in (5, 6):
                    # print(single_date.strftime("%Y-%m-%d"))
                    data = requests.get('https://api.vatcomply.com/rates?base=USD&symbols=EUR,JPY,BRL&date=' + str(single_date))
                    data_status = data.status_code

                    # Testando conexao
                    if data_status == 200:
                        for cote in data:
                            cote = json.loads(cote)
                            date_cotacao = cote["date"]
                            base = cote["base"]

                            for moeda in cote["rates"]:
                                symbol = str(moeda)
                                rate = cote["rates"][moeda]
                                check_register(date_cotacao, base, symbol, rate)

            # Formatando QuerySet para Json
            response = serializers.serialize("json", Cotacao.objects.filter(date__range=[start_date, end_date]))
            messages = "Formato de data não compatível"

       
        return render(request, 'html/chart.html', {'response':response, 'form':form, 'messages':messages})

# def view_chart(request):
#     return render(request, 'html/chart.html', {})

# Funcao para checkar se ja existe na base
def check_register(date_cotacao, base, symbol, rate):
    if not Cotacao.objects.filter(date=date_cotacao,base=base,rate=rate,symbol=symbol).exists():
        cotacao = Cotacao(date=date_cotacao,base=base,rate=rate,symbol=symbol)
        cotacao.save()
        print(symbol, date_cotacao, " - CADASTRADO COM SUCESSO")
    else:
        print(symbol, date_cotacao, " - JÁ CADASTRADO")

# Criando range de datas
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)