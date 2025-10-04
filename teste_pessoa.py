from database import PessoaDAO, Session

session = Session()


dao = PessoaDAO(session)
pessoas = dao.obter_todas_pessoas()

print(pessoas)