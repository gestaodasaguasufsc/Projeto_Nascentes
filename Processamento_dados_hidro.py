# -*- coding: utf-8 -*-
"""
Created on Fri Aug  8 13:43:33 2025

@author: Djesser
"""
import os
import pandas as pd
#import chardet

pasta = 'G:/Meu Drive/Gestão das Águas - Pastas compartilhadas/p04 - Córregos e Lagoas/2019 - Nascentes Campus Trindade/Análise dos Dados - Python/Dados LabHidro/dadosPrecipitação/'
prec1 = pd.read_csv(os.path.join(pasta,'feb-may.csv'), sep = ';')

for i in range(2,7):
   prec1.iloc[:,i] = prec1.iloc[:,i].str.replace(',','.',regex=False)
prec1.to_csv(os.path.join(pasta,'feb-may_.csv'), index=False)

data = []
#prec1 = prec1.drop(index=0)
#data.append(prec1)

# Detect encoding

links = ['feb-may_.csv','may-aug.csv','aug-oct.csv']
for i, link in enumerate(links):
    data_link = os.path.join(pasta,link)
    #with open(data_link, 'rb') as f:
        #result = chardet.detect(f.read())
        #encoding = result['encoding']
        #print(encoding)
    data_ = pd.read_csv(data_link, encoding = 'ISO-8859-1')
    data_ = data_.drop(index=0)
    data.append(data_)

data[0].columns = data[1].columns
dados_hidro = pd.DataFrame(columns = data[0].columns)

for item in data:
    dados_hidro = pd.concat([dados_hidro, item]) #result
    
#precipitação acumulada

# Convertendo a coluna 'data' para datetime
dados_hidro['Data'] = pd.to_datetime(dados_hidro['Data'],dayfirst=True)


for i in range(2,7):
   print(i)
   dados_hidro.iloc[:,i] = pd.to_numeric(dados_hidro.iloc[:,i], errors='coerce')
   
   
dados_hidro.iloc[:,2] = dados_hidro.iloc[:,2]*25.4 #converte polegadas em mm
dados_hidro.info()

dados_hidro.to_csv(os.path.join(pasta,'dados_hidro.csv'), index=False)
# Somando a precipitação diária

df_diario = dados_hidro.groupby('Data')['Pluviógrafo'].sum().reset_index().round(3)
df_diario.rename(columns={'Pluviógrafo': 'prec_diaria'}, inplace=True)
#df_diario['prec_diaria'] = df_diario['prec_diaria'].round(2)
df_diario.to_csv(os.path.join(pasta,'df_diario.csv'), index=False)

# Adicionando a precipitação acumulada
#df_diario['precipitacao_acumulada'] = df_diario['prec_diaria'].cumsum()

#print(df_diario)

    
