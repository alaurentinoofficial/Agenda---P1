from agenda import organizar, listar, adicionar, remover, ordenarPorDataHora, ordenarPorPrioridade

def test_organizar():
	lines = [
	"Comer menos açúcar"
	, "23052017 1030 Reunião com Huguinho, Luizinho e Zezinho. @Skype +Pesquisa"
	, "(B) Terminar a especificação do projeto de IF968. +IF968"
	, "(B) Publicar a especificação do projeto de IF968 terminada. +IF968"
	, "(A) Corrigir provas de IF968 +IF968"
	, "23052017 (A) Ler artigo IST. +Serviço"
	, "2330 Dormir cedo @Casa"
	, "(B) Revisar artigo IST +Service"
	, "(B) Revisar artigos SBES +Service"
	, "(B) Revisar artigos SBES Education +Service"
	, "(B) Revisar artigos SBES Insightful Ideas +Service"
	, "(B) Revisar artigos SBLP +Service"
	, "(D) Read \"Optimizing energy consumption of GUIs in android apps: A multi-objective approach.\""
	]

	result = organizar(lines)

	expexted = [
		('Comer menos açúcar', ('', '', '', '', ''))
		, ('Reunião com Huguinho, Luizinho e Zezinho.', ('23052017', '1030', '', '@Skype', '+Pesquisa'))
		, ('Terminar a especificação do projeto de IF968.', ('', '', '(B)', '', '+IF968'))
		, ('Publicar a especificação do projeto de IF968 terminada.', ('', '', '(B)', '', '+IF968'))
		, ('Corrigir provas de IF968', ('', '', '(A)', '', '+IF968'))
		, ('Ler artigo IST.', ('23052017', '', '(A)', '', '+Serviço'))
		, ('Dormir cedo', ('', '2330', '', '@Casa', ''))
		, ('Revisar artigo IST', ('', '', '(B)', '', '+Service'))
		, ('Revisar artigos SBES', ('', '', '(B)', '', '+Service'))
		, ('Revisar artigos SBES Education', ('', '', '(B)', '', '+Service'))
		, ('Revisar artigos SBES Insightful Ideas', ('', '', '(B)', '', '+Service'))
		, ('Revisar artigos SBLP', ('', '', '(B)', '', '+Service'))
		, ('Read "Optimizing energy consumption of GUIs in android apps: A multi-objective approach."', ('', '', '(D)', '', ''))
	]

	return expexted == result

def test_save():
	return adicionar('Test', ('23052017', '0620', '', '@Hangouts', '+UnitTest'))

def test_remove():
	todo = listar()
	return remover(str(len(todo)))

if __name__ == "__main__":
	print('organizar()   ->   ', 'OK' if test_organizar() else "FAILED")
	print('adicionar()   ->   ', 'OK' if test_save() else "FAILED")
	print('remover()   ->   ', 'OK' if test_remove() else "FAILED")
