from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/filmes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Filme(db.Model):
    __tablename__ = 'filmes'
    id = db.Column(db.Integer, primary_key=True) 
    titulo = db.Column(db.String(60), nullable=False)
    genero = db.Column(db.String(30), nullable=False)
    duracao = db.Column(db.Integer, nullable=False)
    nota = db.Column(db.Float, nullable=False)


    def to_json(self):
        json_filmes = {
            'id': self.id,
            'titulo': self.titulo,
            'genero': self.genero,
            'duracao': self.duracao,
            'nota': self.nota
        }
        return json_filmes #retorna pra rota filmes


    @staticmethod
    def from_json(json_filmes):
        titulo = json_filmes.get('titulo')
        genero = json_filmes.get('genero')
        duracao = json_filmes.get('duracao')
        nota = json_filmes.get('nota')
        return Filme(titulo=titulo, genero=genero, duracao=duracao, nota=nota)

@app.route('/filmes')
def cadastro():
    # obtém todos os registros da tabela filmes
    filmes = Filme.query.all()
    # converte a lista de filmes para o formato JSON
    return jsonify([filme.to_json() for filme in filmes])

@app.route('/filmes',methods=['POST'])
def inclusao():
    filme = Filme.from_json(request.json)
    db.session.add(filme)
    db.session.commit()
    return jsonify(filme.to_json()), 201

@app.errorhandler(404)
def id_invalido(error):
    return jsonify({'id': 0, 'message': 'not found'}), 404   

@app.route('/filmes/<int:id>', methods=['PUT'])
def alteracao(id):
    # obtém o registro a ser alterado (ou gera um erro 404 - not found)
    filme = Filme.query.get_or_404(id)
    
    # recupera os dados enviados na requisição
    filme.titulo = request.json['titulo']
    filme.genero = request.json['genero']
    filme.duracao = request.json['duracao']
    filme.nota = request.json['nota']
    
    # altera (pois o id já existe)    
    db.session.add(filme)
    db.session.commit()
    return jsonify(filme.to_json()), 204

@app.route('/')
def teste():
    return '<h1>Cadastro de Filmes</h1>'


if __name__ == '__main__':
    app.run(debug=True)