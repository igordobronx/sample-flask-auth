from flask import Flask, request, jsonify
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from models.user import User
from database import db
import bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/flask-crud'

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
#view login
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id) #busca no banco de dados 

#session <- conexao ativa
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        #login
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            login_user(user)
            print(current_user.is_authenticated)
            return jsonify({"mensagem": "autenticacao realizada com sucesso"})

    return jsonify({"mensagem": "credenciais invalidas"}), 400

@app.route('/logout', methods=['GET'])
@login_required #protege a rota para apenas autenticados.
def logout():
    logout_user()
    return jsonify({"mensagem": "logout realizado com sucesso"})


@app.route('/user', methods=['POST'])

def create_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    role = data.get("role")

    if username and password:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        if role:
            user = User(username=username, password=hashed_password, role=role)
        else:
            user = User(username=username, password=hashed_password)
        
        db.session.add(user)
        db.session.commit()
        return jsonify({"mensagem": "usuario cadastrado com sucesso"})

    return jsonify({"mensagem": "dados invalidas"}), 400


@app.route('/user/<int:id_user>', methods=['GET'])
@login_required
def read_user(id_user):
    user = User.query.get(id_user)

    if user:
        return {"username": user.username}
    
    return jsonify({"mensagem": "usuário nao encontrado"}), 404

@app.route('/user/<int:id_user>', methods=['PUT'])
@login_required
def update_user(id_user):
    data = request.json
    user = User.query.get(id_user)

    if id_user != current_user.id and current_user.role == "user": #nao poermite ele se excluir e nao permite alterar caso n for admin
        return jsonify({"mensagem": "operacoa nao permitida, voce nao é admin"}), 403

    if user and data.get("password"):
        new_password = data.get("password")
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user.password = hashed_password
        db.session.commit()

        return jsonify({"mensagem": f"usuario {user.username} atualizado com sucesso"})
    
    return jsonify({"mensagem": "usuário nao encontrado"}), 404

@app.route('/user/<int:id_user>', methods=['DELETE'])
@login_required
def delete_user(id_user):
    user = User.query.get(id_user)

    if current_user.role != 'admin':
        return jsonify({"mensagem": "operacao n permitida, voce nao é admin"}), 403


    if id_user == current_user.id: #verifica se o  user logado nao vai excluir ele mesmo
        return jsonify({"mensagem": "deleção não permitida"}), 403

    if user: 
        db.session.delete(user)
        db.session.commit()
        return jsonify({"mensagem": "usuario deletado com sucesso"})
    
    return jsonify({"Mensagem": "usuario nao encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)