import xml.etree.ElementTree as ET
import unidecode
import csv
import csv
import unicodedata
import re
import nltk
import numpy as np
import math
import time
from datetime import datetime


#global colunas 
nltk.download('punkt')

from nltk.tokenize import word_tokenize

def geradorModelo():
  start = time.time()
  print("geradorModelo")
  with open('arquivo.csv','r') as f:
    reader = csv.reader(f,delimiter=';')
    lista = [] 
    colunas=[]
    max =0;

    #print(list(reader)[1][1])

    for linha in reader :
    # print("linha 0", linha[0])
    # print("linha 1" , linha[1])
      #print(len(linha[1]))
      colunas.append(linha[0])
      lista.append(linha[1])
      #print(len(linha[1]))
      #if(max < len(linha[1])):
        #max = len(linha[1])
  lista_completa = []
  for j in range (0,len(lista),1) :
    lista_teste = lista[j].split(", ")
    lista_final = []

    #print(lista_teste[0].replace('[',"").replace("'",""))
    #lista_teste[len(lista_teste)-1].replace(']',"")
    #lista_final.append(lista_teste[0].replace('[',"").replace("'",""))
    for i in range(0,len(lista_teste),1):
      lista_final.append(lista_teste[i].replace("'","").replace(" ","").replace('[',"").replace("'","").replace(']',""))
      #print(lista_teste[i].replace("'","").replace(" ",""))

    lista_completa.append(lista_final)
  
  s = (len(lista_completa),1240)
  matriz_termo_documento = np.zeros(s)
  #print(len(lista_completa))
  for i in range(0,len(lista_completa),1):
    #print('i == ', i)
    for j in range(0,len(lista_completa[i]),1):
      #print(len(lista_completa[i]))
      #print('j == ',j)
      if(lista_completa[i][j]!= ''):
        #print(lista_completa[i][j])
        k = int(lista_completa[i][j])
        matriz_termo_documento[i][k] = matriz_termo_documento[i][k] + 1

  d_ =  (len(lista_completa),1)
  df= np.zeros(d_)
  print(len(df))
  #esse maximo vai normalizar a matriz_termo_documento
  maximo = 1
  for i in range(0,len(matriz_termo_documento),1):
    contador =0
    for j in range(0,len(matriz_termo_documento[i]),1):
      
      if(matriz_termo_documento[i][j] != 0.0 ):
        #print(matriz_termo_documento[i][j] )
        contador = contador+1
        #verifico se aquele máximo está disponível
        if(matriz_termo_documento[i][j]>maximo):
         # print(matriz_termo_documento[i][j])
          maximo = matriz_termo_documento[i][j]
        #print(matriz_termo_documento[i][j])
    
    df[i]= contador
  #wi,j = tfi,j xlog(N/df(i))
  #tf(i,j) : frequência da palavra i no documento j
  #df(i,j) : número de documentos que contenham i
  #N : número total de documentos
  #maximo : é o valor do termo com a maior frequencia
  N = 1240
  #precisa calcular df(i)
  w_ = (len(lista_completa),1240)
  w = np.zeros(w_)

  for i in range(0,len(matriz_termo_documento),1):
    for j in range(0,len(matriz_termo_documento[i]),1):
      # print(len(matriz_termo_documento[i]))
      #print(float((matriz_termo_documento[i][j]/maximo)*np.log(N/df[i])))
      w[i][j]  = float((matriz_termo_documento[i][j]/maximo)*np.log(N/df[i]))
      if(math.isnan(float((matriz_termo_documento[i][j]/maximo)*np.log(N/df[i])))):
          w[i][j]=0
      # if( matriz_termo_documento[i][j]*np.log(N/df[i])!=0):

  end = time.time()
  now = datetime.now()
  with open('logGeradorModelo.csv', 'a') as csvfile:
       csv.writer(csvfile, delimiter=';').writerow(["Modelo Executado em : "])
       csv.writer(csvfile, delimiter=';').writerow([now])
       csv.writer(csvfile, delimiter=';').writerow(["Tempo de processamento para gerar o MODELO"])
       csv.writer(csvfile, delimiter=';').writerow([end-start ]+ [" Segundos"])
  w_retornar = w
  a = np.array(w)
  np.savetxt('modelo.csv', a, delimiter=',')
  with open('colunas.csv', 'w') as col: 
    wr = csv.writer(col, quoting=csv.QUOTE_ALL)
    wr.writerow(colunas)
  return w_retornar




def geradorListaInvertida(words,dicionario_tokenizado,f):

  start = time.time()

  lista_invertida = {}

  for wordn in range(len(words)):
    lista_invertida[words[wordn]]=[]
    for chaves in dicionario_tokenizado:
      for x in range(0,len(dicionario_tokenizado[chaves]),1):
        if(words[wordn] == dicionario_tokenizado[chaves][x]):
          lista_invertida[words[wordn]].append(chaves)
  nome_arquivo  = open('arquivo.csv', 'w', newline='', encoding='utf-8')
  w = csv.writer(f)
  with open('arquivo.csv', 'r+', newline='') as csvfile: 
    spamwriter = csv.writer(csvfile, delimiter=';') 
   # spamwriter.writerow(['palavra'] + ['vetor de documentos']) 
    for key, value in lista_invertida.items() :
        spamwriter.writerow([key.upper(), value])

  end = time.time()
  now = datetime.now()
  with open('logGeradorListaInvertida.csv', 'a') as csvfile:
       csv.writer(csvfile, delimiter=';').writerow(["Lista invertida executada em : "])
       csv.writer(csvfile, delimiter=';').writerow([now])
       csv.writer(csvfile, delimiter=';').writerow(["Tempo de processamento para gerar a lista invertida"])
       csv.writer(csvfile, delimiter=';').writerow([end-start] + [" Segundos"])









def indexador():
  start = time.time()
  with open("/content/drive/MyDrive/Mineração/data/cf80.xml",'r') as f: #80 são todos os arquivos juntos
    mytree = ET.parse(f)
    myroot = mytree.getroot()
  dicionario = {}
  for x in range(0,len(myroot),1):
    for y in range(0,len(myroot[x]),1):
      if(myroot[x][y].tag == 'RECORDNUM'):
        #print(myroot[x][y].tag,' ',myroot[x][y].text)
        var = myroot[x][y].text
      if(myroot[x][y].tag == 'ABSTRACT' or myroot[x][y].tag =='EXTRACT'):
            aux = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", str(myroot[x][y].text)).split())
            aux2= re.sub(r'^RT[\s]+', '', aux)
            aux3 = ''.join([i for i in aux2 if not i.isdigit()])
            #print(myroot[x][y].tag,' ',myroot[x][y].text)
            #dicionario[var] = myroot[x][y].text
            dicionario[var] = aux3 

    dicionario_tokenizado= {}
    texto = ''
  for chaves in dicionario:
    dicionario_tokenizado[chaves] = word_tokenize(dicionario[chaves].upper())
    texto = texto + dicionario[chaves].upper() 
  texto = word_tokenize(texto)
  lista_invertida = {}
    #essa words vai ter que ser lida de algum lugar vamos criar uma para teste.
    #words= ['fibrosis','because','homozygotes','is','this','normal','gabriel']
  words = texto
    #for i in range(len(words)):
      #print(words[i])
  print(len(words))
  words = sorted(set(words))
  words = words[1:]
  print(words)
  print(len(words))
  
  geradorListaInvertida(words,dicionario_tokenizado,f)
  geradorModelo()
  end = time.time()
  now = datetime.now()
  with open('logGeradorIndexador.csv', 'a') as csvfile:
       csv.writer(csvfile, delimiter=';').writerow(["Indexador executado em :"])
       csv.writer(csvfile, delimiter=';').writerow([now])
       csv.writer(csvfile, delimiter=';').writerow(["Tempo de processamento para gerar o modulo Indexador"])
       csv.writer(csvfile, delimiter=';').writerow([end-start]+[" Segundos"])




  








