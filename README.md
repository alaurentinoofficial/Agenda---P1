# Agenda Inteligente

## Para adicionar uma nova agenda use:
* `Descição` **obrigatório** Fala um pouco sobre a tarefa
* `Prioridade` **(A-Z)** Prioridade da tarefa classificade de A à Z ex: `(B)`
* `Data` **ddmmYYYY** Data da tarefa sem usar barras ex: `25052019`
* `Data` **hhMM** Hora da tarefa sem usar dois pontos ex: `0920`
* `Contexto` **@Contexto** Contexto onde ocorrerá a tarefa ex: `@Github`
* `Projeto` **+Projeto** Em que projeto ele se enquadra ex: `+Programação1`
```
$ python ./agenda.py a [descrição] ([prioridade A-Z]) [dia][mes][ano] [hora][minuto] @[contexto] +[projeto]
```

Exemplo:
```
$ python ./agenda.py a Terminar de completar o README.md (A) 25062019 0930
```
<br/>

## Para lista as tarefas
```
$ python ./agenda.py l
```

Exemplo:
```
$ python ./agenda.py l

1 - 27/03/2019 20:35 (A) Reunião com Huguinho, Luizinho e Zezinho. Teste de uma nova atividade @Skype +Pesquisa27032019
2 - 27/03/2019 20:34 (A) Teste de uma nova atividade
3 - 27/03/2019 12:34 (A) Teste de uma nova atividade
4 - 27/03/2019 (A) Teste de uma nova atividade 2734
5 - 27/03/2019 (A) Teste de uma nova atividade 2734
6 - 23/05/2015 19:06 (A) fjslkdfla asdkfjlasd jaskdfj laksd @ jsadhfkjdsa @contexto +projeto
7 - 12:30 (A) Primeiro Revisar artigo IST +Service
8 - (A) Corrigir provas de IF968 +IF968
9 - 12:30 (B) Revisar artigo IST +Service
10 - (B) Revisar artigos SBES +Service
[...]
```
<br/>

## Priorizar uma tarefa
* `Número da tarefa` **Inteiro** índice da ativiada ex: `10`
* `Prioridade` **(A-Z)** Prioridade da tarefa classificade de A à Z ex: `(B)`
```
$ python ./agenda.py p [número da tarefa] [A-Z]
```
<br/>

## Remover uma atividae
* `Número da tarefa` **Inteiro** índice da ativiada ex: `10`
```
$ python ./agenda.py r [número da tarefa]
```
<br/>

## Fazer/Finalizar uma tarefa
* `Número da tarefa` **Inteiro** índice da ativiada ex: `10`
```
$ python ./agenda.py f [número da tarefa]
```
<br/>