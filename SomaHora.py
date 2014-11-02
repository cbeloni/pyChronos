#!/usr/data_daysin/env python
# -*- coding: UTF-8 -*-
from datetime import *
from time import strptime

data = '27-06-2014 09:30'
tempo_de_desenvolvimento = '48'
tempo = int(tempo_de_desenvolvimento)

data_formatada = datetime.strptime(data, '%d-%m-%Y %H:%M')

hora_diferenca = data_formatada.hour - 8
if hora_diferenca != 0:
	hora_diferenca *= -1
	data_formatada = data_formatada + timedelta(hours = hora_diferenca)

horas = tempo % 8
print ("horas: " + str(horas))

dias = tempo / 8
print ("dias: " + str(dias))

data_days = data_formatada + timedelta(days = dias)
data_final = data_days + timedelta(hours = horas)

#for i in range(1,10):
#    dia_da_semana = datetime(strptime('2011-03-08  0:27:41', '%Y-%m-%d  %H:%M:%S')[0:6]).weekday()

#adiciona novamente as horas subtraidas para o cálculo de dias e horas
if hora_diferenca != 0:
	hora_diferenca *= -1
	data_final = data_final + timedelta(hours = hora_diferenca)

#verifica se o horário de almoço será adicionado somente para o dia corrente
if data_final.hour >= 12 and data_final.hour <= 18:
    data_final = data_final + timedelta(hours = 1)

#Caso após adicionar a diferença de horas o valor ultrapassar o horário comercial é adicionado mais um dia e inclída as horas da 
#diferença
if  data_final.hour >= 18:
	hora_diferenca = data_final.hour - 17
	data_final = data_final + timedelta(days = 1)
	data_final = data_final + timedelta(hours = -data_final.hour)
	data_final = data_final + timedelta(hours = 8 + hora_diferenca)


for i in range(0,dias):
    data_formatada = data_formatada + timedelta(days = 1)
    #dia_semana = datetime(strptime(data, '%d-%m-%Y  %H:%M')[0:6]).weekday()
    dia_semana = data_formatada.weekday()
    print (dia_semana)
    if (dia_semana == 5):
        data_final = data_final + timedelta(days = 2)
        data_formatada = data_formatada + timedelta(days = 2)
        print ("somou mais dois")

print (data_final.strftime('%d-%m-%Y %H:%M'))