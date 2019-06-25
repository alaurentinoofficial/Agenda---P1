import re
import sys
import time
import datetime

TODO_FILE = 'todo.txt'
ARCHIVE_FILE = 'done.txt'

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = "\033[0;33m"

ADICIONAR = 'a'
REMOVER = 'r'
FAZER = 'f'
PRIORIZAR = 'p'
LISTAR = 'l'

# Imprime texto com cores. Por exemplo, para imprimir "Oi mundo!" em vermelho, basta usar
#
# printCores('Oi mundo!', RED)
# printCores('Texto amarelo e negrito', YELLOW + BOLD)

def printCores(texto, cor) :
  print(cor + texto + RESET)

def cor(texto, cor) :
  return cor + texto + RESET
  

# Adiciona um compromisso aa agenda. Um compromisso tem no minimo
# uma descrição. Adicionalmente, pode ter, em caráter opcional, uma
# data (formato DDMMAAAA), um horário (formato HHMM), uma prioridade de A a Z, 
# um contexto onde a atividade será realizada (precedido pelo caractere
# '@') e um projeto do qual faz parte (precedido pelo caractere '+'). Esses
# itens opcionais são os elementos da tupla "extras", o segundo parâmetro da
# função.
#
# extras ~ (data, hora, prioridade, contexto, projeto)
#
# Qualquer elemento da tupla que contenha um string vazio ('') não
# deve ser levado em consideração. 
def adicionar(descricao, extras):

  # não é possível adicionar uma atividade que não possui descrição. 
  if descricao  == '' :
    return False
  
  data, hora, prioridade, contexto, projeto = extras

  novaAtividade = ''

  if data != '' and dataValida(data) : novaAtividade += data + ' '
  if hora != '' and horaValida(hora) : novaAtividade += hora + ' '
  if prioridade != '' and prioridadeValida(prioridade) : novaAtividade += prioridade + ' ' 

  novaAtividade += descricao

  if contexto != '' and contextoValido(contexto) : novaAtividade += ' ' + contexto
  if projeto != '' and projetoValido(projeto) : novaAtividade += ' ' + projeto

  # Escreve no TODO_FILE. 
  fp = open(TODO_FILE, 'a')
  fp.write(novaAtividade + "\n")
  fp.close()

  return True


# Valida a prioridade.
def prioridadeValida(pri):
  return len(pri) == 3 and pri[0] == "(" and pri[2] == ")" and (pri[1] >= "A" and pri[1] <= "Z" or pri[1] >= "a" and pri[1] <= "z")


# Valida a hora. Consideramos que o dia tem 24 horas, como no Brasil, ao invés
# de dois blocos de 12 (AM e PM), como nos EUA.
def horaValida(horaMin) :
  if len(horaMin) != 4 or not soDigitos(horaMin):
    return False
  else:
    return int(horaMin[:2]) >= 0 and int(horaMin[:2]) <= 23 and int(horaMin[2:]) >= 0 and int(horaMin[2:]) <= 59

# Valida datas. Verificar inclusive se não estamos tentando
# colocar 31 dias em fevereiro. Não precisamos nos certificar, porém,
# de que um ano é bissexto. 
def dataValida(data) :
  try:
      datetime.datetime.strptime(data, '%d%m%Y')
      return True
  except ValueError:
      return False

# Valida que o string do projeto está no formato correto. 
def projetoValido(proj):
  return len(proj) >= 2 and proj[0] == "+" and (" " not in proj)

# Valida que o string do contexto está no formato correto. 
def contextoValido(cont):
  return len(cont) >= 2 and cont[0] == "@" and (" " not in cont)

# Valida que a data ou a hora contém apenas dígitos, desprezando espaços
# extras no início e no fim.
def soDigitos(numero) :
  if type(numero) != str :
    return False
  for x in numero :
    if x < '0' or x > '9' :
      return False
  return True


# Dadas as linhas de texto obtidas a partir do arquivo texto todo.txt, devolve
# uma lista de tuplas contendo os pedaços de cada linha, conforme o seguinte
# formato:
#
# (descrição, prioridade, (data, hora, contexto, projeto))
#
# É importante lembrar que linhas do arquivo todo.txt devem estar organizadas de acordo com o
# seguinte formato:
#
# DDMMAAAA HHMM (P) DESC @CONTEXT +PROJ
#
# Todos os itens menos DESC são opcionais. Se qualquer um deles estiver fora do formato, por exemplo,
# data que não tem todos os componentes ou prioridade com mais de um caractere (além dos parênteses),
# tudo que vier depois será considerado parte da descrição.  
def organizar(linhas):
  itens = []

  for l in linhas:
    data = '' 
    hora = ''
    pri = ''
    desc = ''
    contexto = ''
    projeto = ''
  
    l = l.strip() # remove espaços em branco e quebras de linha do começo e do fim
    tokens = l.split() # quebra o string em palavras

    for item in tokens:
      if dataValida(item): data = item
      elif horaValida(item): hora = item
      elif prioridadeValida(item): pri = item
      elif contextoValido(item): contexto = item
      elif projetoValido(item): projeto = item
      else: desc += item + ' '

    desc = desc[:-1]

    itens.append((desc, (data, hora, pri, contexto, projeto)))

  return itens


# Datas e horas são armazenadas nos formatos DDMMAAAA e HHMM, mas são exibidas
# como se espera (com os separadores apropridados). 
#
# Uma extensão possível é listar com base em diversos critérios: (i) atividades com certa prioridade;
# (ii) atividades a ser realizadas em certo contexto; (iii) atividades associadas com
# determinado projeto; (vi) atividades de determinado dia (data específica, hoje ou amanhã). Isso não
# é uma das tarefas básicas do projeto, porém. 
def listar():
  linhas = []
  
  with open(TODO_FILE) as file:
    for linha in file:
      linhas.append(linha)

    itens = organizar(linhas)

  return ordenarPorPrioridade(ordenarPorDataHora(itens))


def timestamp(date):
  return time.mktime(datetime.datetime.strptime(date, "%d%m%Y").timetuple()) if dataValida(date) else 0

def tempoParaMinutos(time):
  return int(time[:2]) * 60 + int(time[2:]) if horaValida(time) else 0


# (descrição, (data, hora, prioridade, contexto, projeto))
def ordenarPorDataHora(itens):
  ordem_itens = []

  for item in itens:
    ordem_itens.append( (item, timestamp(item[1][0]), tempoParaMinutos(item[1][1])) )

  ordem_itens = sorted(ordem_itens,  key=lambda x: (x[1], x[2]), reverse=True)
  
  return [x[0] for x in ordem_itens]

def ordenarPorPrioridade(itens):
  ordem_itens = []

  for item in itens:
    ordem_itens.append( (item, ord(item[1][2][1].upper()) if prioridadeValida(item[1][2]) else ord("Z") + 1) )
  
  ordem_itens = sorted(ordem_itens,  key=lambda x: x[1])
  
  return [x[0] for x in ordem_itens]


def salvarTarefas(todos):
  linhas = []
  
  for todo in todos:
      linhas.append( re.sub(' +', ' ',"%s %s %s %s %s %s" % (todo[1][0], todo[1][1], todo[1][2], todo[0], todo[1][3], todo[1][4])).strip() + "\n" )
  
  with open(TODO_FILE, 'w') as file:
    file.writelines(linhas)
    file.close()


def fazer(index):
  todo = remover(index)

  if todo != None:
    with open(ARCHIVE_FILE, 'a') as file:
      file.write(re.sub(' +', ' ',"%s %s %s %s %s %s" % (todo[1][0], todo[1][1], todo[1][2], todo[0], todo[1][3], todo[1][4])).strip() + "\n")
      file.close()
      return todo
  
  return None

def remover(index):
  if soDigitos(index):
    todos = listar()
    index = int(index)-1
      
    if index <= len(todos) and index >= 0:
      todo = todos[index]
      todos.pop(index)
      salvarTarefas(todos)
      return todo

  return None



# prioridade é uma letra entre A a Z, onde A é a mais alta e Z a mais baixa.
# num é o número da atividade cuja prioridade se planeja modificar, conforme
# exibido pelo comando 'l'. 
def priorizar(index, prioridade):
  if soDigitos(index) and prioridade >= "A" and prioridade <= "Z":
    todos = listar()
    index = int(index)-1
      
    if index <= len(todos) and index >= 0:
      todos[index] = (todos[index][1][0], (todos[index][1][1], "(%s)" % prioridade, todos[index][0], todos[index][1][3], todos[index][1][4]))
      salvarTarefas(todos)
      return True

  return None



# Esta função processa os comandos e informações passados através da linha de comando e identifica
# que função do programa deve ser invocada. Por exemplo, se o comando 'adicionar' foi usado,
# isso significa que a função adicionar() deve ser invocada para registrar a nova atividade.
# O bloco principal fica responsável também por tirar espaços em branco no início e fim dos strings
# usando o método strip(). Além disso, realiza a validação de horas, datas, prioridades, contextos e
# projetos. 
def processarComandos(comandos) :
  if comandos[1] == ADICIONAR:
    comandos.pop(0) # remove 'agenda.py'
    comandos.pop(0) # remove 'adicionar'
    itemParaAdicionar = organizar([' '.join(comandos)])[0]
    try: 
      adicionar(itemParaAdicionar[0], itemParaAdicionar[1]) # novos itens não têm prioridade
    except IOError as err:
      print("Não foi possível escrever para o arquivo " + TODO_FILE)
      print(err)
  
  elif comandos[1] == LISTAR:
    todos = listar()

    for i, todo in enumerate(todos):
      data = "{}/{}/{}".format(todo[1][0][:2], todo[1][0][2:4], todo[1][0][4:]) if dataValida(todo[1][0]) else ""
      hora = "{}:{}".format(todo[1][1][:2], todo[1][1][2:]) if horaValida(todo[1][1]) else ""

      prioridade = todo[1][2].upper()

      if prioridade == "(A)": prioridade = cor(prioridade, BLUE)
      elif prioridade == "(B)": prioridade = cor(prioridade, RED)
      elif prioridade == "(C)": prioridade = cor(prioridade, YELLOW)
      elif prioridade == "(D)": prioridade = cor(prioridade, GREEN)

      print(re.sub(' +', ' ', "{} - {} {} {} {} {} {}".format(i+1, data, hora, prioridade, todo[0], todo[1][3], todo[1][4])).strip() )

  elif comandos[1] == REMOVER:
    if len(comandos) != 3 or remover(comandos[2]) == None:
      print("Tarefa invalida.")

  elif comandos[1] == FAZER:
    if len(comandos) != 3 or fazer(comandos[2]) == None:
      print("Tarefa invalida.")

  elif comandos[1] == PRIORIZAR:
    if len(comandos) != 4 or not priorizar(comandos[2], comandos[3][0].upper()):
      print("Tarefa ou Prioridade invalidas")

  else :
    print("Comando inválido.")

processarComandos(sys.argv)