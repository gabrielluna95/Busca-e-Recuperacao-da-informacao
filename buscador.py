
import xml.etree.ElementTree as ET
import unidecode
import unicodedata
import re
import csv
import time
from datetime import datetime

#with open("/content/drive/MyDrive/Mineração/data/cf78.xml",'r') as f:
with open("/content/drive/MyDrive/Mineração/data/cfquery.xml",'r') as perguntas: #80 são todos os arquivos juntos

  mytree = ET.parse(perguntas)
  myroot = mytree.getroot()


def buscador():
  w = geradorModelo()
  start = time.time()
  #print('valor de w eh ', w)
  
  with open('colunas.csv','r') as colunas:
    reader = csv.reader(colunas,delimiter=',')
    colunas=[]
    for linha in reader :
     print(linha)
   
    for i in range(0, len(linha),1):
       colunas.append(linha[i])
  with open("/content/drive/MyDrive/Mineração/data/cfquery.xml",'r') as perguntas: #80 são todos os arquivos juntos
  

    mytree = ET.parse(perguntas)
    myroot = mytree.getroot()
    dicionario = {}
  for x in range(0,len(myroot),1):
    for y in range(0,len(myroot[x]),1):
      if(myroot[x][y].tag == 'QueryNumber'):
        #print(myroot[x][y].tag,' ',myroot[x][y].text)
        var = myroot[x][y].text
      if(myroot[x][y].tag == 'QueryText'):
            aux = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", str(myroot[x][y].text)).split())
            aux2= re.sub(r'^RT[\s]+', '', aux)
            aux3 = ''.join([i for i in aux2 if not i.isdigit()])
            #print(myroot[x][y].tag,' ',myroot[x][y].text)
            #dicionario[var] = myroot[x][y].text
            dicionario[var] = aux3
    # print(myroot[x][y].tag,' ',myroot[y[x].text)
    #print('Mudou \n\n\n')  
  dicionario_tokenizado= {}
  texto = ''
  for chaves in dicionario:
    dicionario_tokenizado[chaves] = word_tokenize(dicionario[chaves].upper())
    #texto = texto+ dicionario[chaves].upper()
    #texto = texto+ dicionario[chaves]
    #print(chaves,' ',dicionario[chaves])
  #aqui é feito o calculo de cada valor para cada pergunta.

  for chaves in dicionario_tokenizado:
    print("Query : ",dicionario[chaves],'Identificador da query : ',chaves)
    
  
    lst = [] 
    for i in range(0,1240,1):
      lst.append([]) 
      for j in range(0,10539,1): 
          lst[i].append(w[j][i]) 
    vetor_similaridade = []
    dicionario_tokenizado[chaves] = sorted(set(dicionario_tokenizado[chaves]))
    q=sorted(set(dicionario_tokenizado[chaves]))
    #print(q)
    s_q = (10539)
    s_q = np.zeros(s_q)
    for i in range(0,len(q),1):
      for j in range(0,10539,1):
      # print(q[i],colunas[j])
        if(q[i] == colunas[j]):
          #print(q[i],colunas[j],i,j)
          s_q[j]=1
    for i in range(0,1240,1):
      lista1=np.array(lst[i])
      lista2 = np.array(s_q)
      similarity_scores = lista2.dot(lista1)/(np.linalg.norm(lista2)*np.linalg.norm(lista1))
      vetor_similaridade.append(similarity_scores)
    
    maior =0
    dicionario_final = {}
    for i in range (0,1240,1):
     # print('Documento : ',i,' possui similaridade : ',vetor_similaridade[i])
      if(vetor_similaridade[i]> maior):
        maior = vetor_similaridade[i]
        indice =i
      
      dicionario_final[i] = vetor_similaridade[i]
    with open('./resultado.csv', 'a') as csvfile:
       #csv.writer(csvfile, delimiter=';')
       aux=0 
       csv.writer(csvfile, delimiter=';').writerow([chaves])
       for i in sorted(dicionario_final, key = dicionario_final.get, reverse=True):
          #print(aux,i, dicionario_final[i])
          csv.writer(csvfile, delimiter=';').writerow([aux]+[i] + [dicionario_final[i]])
          aux=aux+1
    #print('Dicionario ordernado ', sorted(dicionario_final))    
    #print('Documento :',indice,' Possui similaridade : ' ,maior)
   # print("\n\n\n\n\n\n##########MUDOU############\n\n\n")
    #print(chaves,' ',dicionario_tokenizado[chaves])
  end = time.time()
  now = datetime.now()
  with open('logBuscador.csv', 'a') as csvfile:
       csv.writer(csvfile, delimiter=';').writerow(["Buscador executado em :"])
       csv.writer(csvfile, delimiter=';').writerow([now])
       csv.writer(csvfile, delimiter=';').writerow(["Tempo de processamento para realizar as consultas"])
       csv.writer(csvfile, delimiter=';').writerow([end-start ]+ [" Segundos"])
















