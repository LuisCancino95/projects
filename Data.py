#!/usr/bin/env python3


import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import os.path
import pandas as pd


url = "https://www.yapo.cl/region_metropolitana/autos?ca=15_s&st=s&ps=2&cg=2020&q=auto&o="


Links = []

for i in range (1,30):
    URL = url+str(i)
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    data = []

    for link in soup.find_all('a'):
        data.append(link.get('href'))

    links = []

    for i in range(len(data)):
        if i>=(len(data)-5):
            pass
        elif data[i]==data[i+4]:
            links.append(data[i])
        else:
            pass

    links.pop(0)
    if len(links)==51:
        links.pop(50)
    #print(links)
    for j in links:
        Links.append(j)

df = pd.DataFrame(columns=['Nombre','Marca','Precio','Año','Km','Combustible','Transmisión','Link'])

nombre = []
precio = []
year = []
km = []
combu = []
trans = []


for k in range(len(Links)):
    URL = Links[k]
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text()
    data = text.split()
    Sup_cut =  data.index('Detalles')
    fin = []

    for i in range(Sup_cut,len(data)-1):
        fin.append(data[i])

    Inf_cut = fin.index('Tipo')
    autos = []

    for i in range(0,Inf_cut):
        autos.append(fin[i])

    name = ''
    A = "Kilómetros" in autos
    if A==False:
        continue
    for i in range (len(autos)):
        if autos[i]=='Precio' and autos[i+1]=='$':
            for j in range(1,i):
                name = name + ' ' + autos[j]
            nombre.append(name)
            precio.append(autos[i+1]+autos[i+2])
        elif autos[i] == 'Año':
            year.append(autos[i+1])
            km.append(autos[i+3])
            combu.append(autos[i+5])
            trans.append(autos[i+8])
        else:
            pass
    print(k)


print(len(nombre))
print(len(precio))
print(len(year))
print(len(km))
print(len(combu))
print(len(trans))


marca = pd.read_excel('marcas.xls', index_col=0)
modelo = pd.read_excel('modelos.xls', index_col=0)


mcs = []
mdl = []

for i in range(len(marca)):
    mcs.append(marca.iloc[i,0])
    mcs[i] = mcs[i].upper()


for i in range(len(modelo)):
    mdl.append(str(modelo.iloc[i,2]))
    mdl[i] = mdl[i].upper()

mc = []
ml = []
	    
for i in range(len(nombre)):
    k = 0
    for j in range(len(mcs)):
        A = nombre[i].find(mcs[j])
        if A !=-1 and A < 5 :
            mc.append(marca.iloc[j,1])
            k = k + 1
        elif nombre[i].find(mcs[j])==-1:
           pass 
        else:
            pass
    if k == 0:
        mc.append('Sin Marca')
    else:
        pass

print(len(nombre))
print(len(mc))
print(mc)
	    
df = pd.DataFrame({'Nombre': nombre, 'Marca': mc,'Precio': precio, 'Año': year,'Km': km,'Transmision':trans,'Link':Links })

print(len(df))

df.to_excel("Data_autos.xlsx")












