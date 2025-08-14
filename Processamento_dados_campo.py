import os
import pandas as pd
import matplotlib.pyplot as plt

pasta = 'G:/Meu Drive/Gestão das Águas - Pastas compartilhadas/p04 - Córregos e Lagoas/2019 - Nascentes Campus Trindade/Análise dos Dados - Python/'

dados_prec = pd.read_csv(os.path.join(pasta,'Dados LabHidro/dadosPrecipitação/','df_diario.csv'))
dados_prec['Data'] = pd.to_datetime(dados_prec['Data'],dayfirst=True)
dados_prec['prec_diaria']=dados_prec['prec_diaria'].round(1)
dados_prec.to_excel(os.path.join(pasta,'Dados LabHidro/dadosPrecipitação/','df_diario.xlsx'), index=False)
dados_campo = pd.read_csv(os.path.join(pasta,'Dados de campo.csv'), sep=';')

dados_campo['Data'] = pd.to_datetime(dados_campo['Data'], format = "%d/%m/%Y")

merged_df = pd.merge(dados_prec, dados_campo, on='Data', how='left')
merged_df['Ver_Prec_S_N']=''

for i, item in enumerate(merged_df['prec_diaria']):
    
    if item >0:
        merged_df['Ver_Prec_S_N'][i]='Sim'
    else:
        merged_df['Ver_Prec_S_N'][i]='Não'
        
data = merged_df[merged_df.index > 28]
data = data.reset_index(drop=True)

for index, row in data.iterrows():  # Dias de chuva acumulada 
    if index<4:
        pass
    else:
        p1 = row['prec_diaria']
        p2 = data.loc[index-1,'prec_diaria'] + p1
        p3 = data.loc[index-2,'prec_diaria'] + p2
       
        data.loc[index,'Ac_prec_3_dias']=p3
        
data.info()

#Data columns (total 13 columns):
 #   Column          Non-Null Count  Dtype         
#---  ------          --------------  -----         
# 0   Data            217 non-null    datetime64[ns]
# 1   prec_diaria     217 non-null    float64       
# 2   Aplic_altura    63 non-null     object        
# 3   Aplic_fluxo     63 non-null     object        
# 4   CFM_altura      64 non-null     object        
# 5   CFM_fluxo       64 non-null     object        
# 6   Bot_altura      65 non-null     object        
# 7   Bot_fluxo       65 non-null     object
# 8   Ver_Prec_S_N    217 non-null    object        
# 9   Ac_prec_3_dias  217 non-null    float64   
# =============================================================================

# =============================================================================
# Pergunta: 
# - Houve precipitação consecutiva nos três dias anteriores à verificação da nascente? 
# - Até 3 dias anteriores, quantos dias foram?
# - Quantos dias sem precipitação consecutivos?
# =============================================================================


data_CA = data.iloc[:,[0,1,2,3,8,9]]  

dias_sem_prec = 0
u=0

for index, row in data_CA.iterrows(): 
    
    # contabiliza últimos 3 dias de precipitação acumulada
    
    acumulado_dias_chuva = 0
    
    for u in range(3):
        print(u, index)
        if (index-u)>=0:
            
            if data_CA.loc[index-u, 'Ver_Prec_S_N'] == 'Sim':
                acumulado_dias_chuva += 1
                       
    else:
        pass
    data_CA.loc[index,'acumul_3d'] = acumulado_dias_chuva
    
    # contabiliza dias sem precipitação acumulada
    
    if data_CA.loc[index, 'Ver_Prec_S_N'] == 'Não':
        dias_sem_prec += 1
    else:
        dias_sem_prec = 0
    
    data_CA.loc[index,'dias_sem_prec'] = dias_sem_prec
    
      
data_CA_group = data_CA.groupby(['Aplic_altura','acumul_3d'],as_index=False).size()






# =============================================================================
# # Define custom order
# #order = ['Baixo', 'Médio', 'Alto']
# #data_CA['Aplic_altura'] = pd.Categorical(data_CA['Aplic_altura'], categories=order, ordered=True)
# 
# #grouped = df.groupby(['Category', 'Subcategory'])[['Value1', 'Value2']].sum()
# 
# # Plot
# 
# data_CA.loc[data_CA['Aplic_altura'] == 'Baixo', 'Aplic_altura_n'] = 1
# data_CA.loc[data_CA['Aplic_altura'] == 'Médio', 'Aplic_altura_n'] = 2
# data_CA.loc[data_CA['Aplic_altura'] == 'Alto', 'Aplic_altura_n'] = 3
# 
# data_CA_ = data_CA.dropna(subset=['Aplic_altura'])
# 
# x = 'Aplic_altura_n'
# y = 'Ac_prec_3_dias'
# title = f'{x} vs {y}'
# ax = data_CA_.plot(x=x, y=y, kind='scatter', color='red', title = title)
# 
# # Set custom x-axis order
# #ax.set_xticklabels(['Baixo', 'Médio', 'Alto'])
# plt.xlabel(x)
# plt.ylabel(y)
# plt.show()
# =============================================================================

    
    
    
# =============================================================================
#     for dias_prec in range(3):
#         # Quantidade da variável Baixo
#         if row[2] == "Baixo" and row[9] == dias_prec: #
#             if "Low" + str(y4) in dataComp:
#                 dataComp["Low" + str(y4)] += 1
#             else:
#                 dataComp.update({"Low" + str(y4) : 1})
# 
#         # Quantidade da variável Médio
#         elif dataOutput[i][0] == "Médio" and dataOutput[i][1] == y4:
#             if "Med" + str(y4) in dataComp:
#                 dataComp["Med" + str(y4)] += 1
#             else:
#                 dataComp.update({"Med" + str(y4): 1})
# 
# 
#         # Quantidade da variàvel Alta
#         elif dataOutput[i][0] == "Alto" and dataOutput[i][1] == y4:
#             if "High" + str(y4) in dataComp:
#                 dataComp["High" + str(y4)] += 1
#             else:
#                 dataComp.update({"High" + str(y4) : 1})
# 
# total = sum(dataComp.values())
# 
# for u in range(len(data)):  # Dias sem chuva
#     if data[u][0] == "Não":
#         acumulado_dias_chuva += 1
#     else:
#         acumulado_dias_chuva = 0
# 
#     dataVar = [data[u][1], acumulado_dias_chuva]
#     dataOutput.update({u : dataVar})
# 
# for u in range(len(dataOutput)):
#     cont.append(dataOutput[u][1])
# =============================================================================
