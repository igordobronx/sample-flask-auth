from flask_sqlalchemy import SQLAlchemy 
db =  SQLAlchemy()
#ao iniciar, o BC inicia uma session -> conexao ativa
#comandos:
# flask shell 
# >>> db.create_all()
# >>> db.session
# >>> db.session.commit()
# >>> exit()