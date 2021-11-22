from flask import Flask, render_template, request, jsonify
from datetime import date

from flask.wrappers import Response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['TESTING'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/d/ecollisapi/bancodados.db'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "User"
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(db.DateTime, default=date.today())
    nome_do_cliente = db.Column(db.String(80), unique=False, nullable=False)
    cidade = db.Column(db.String(30), unique=False)
    endereco = db.Column(db.String(120), unique=False, nullable=True)
    cep = db.Column(db.Integer, unique=False, nullable=False)
    telefone = db.Column(db.Integer, unique=False, nullable=False)
    kwp = db.Column(db.Integer, unique=False, nullable=False)
    marca_do_inversor = db.Column(db.String(30), unique=False, nullable=True)
    marca_da_placa = db.Column(db.String(16), unique=False, nullable=False)
    vendedor = db.Column(db.String(16), unique=False, nullable=True)

@app.route("/")
def index():
    dados = User.query.all().order_by(User.data.asc())
    return render_template('index.html', dados=dados)

@app.route("/novo", methods=['POST','GET'])
def novo():
    if request.method == 'POST':
        nome = request.form['nome']
        adress = request.form['endereco']
        city = request.form['cidade']
        cep_cliente = request.form['cep']
        tel = request.form['telefone']
        kilowp = request.form['kwp']
        inv = request.form['inv']
        placa = request.form['placa']
        vendedo = request.form['vendedor']
        inserir = User(nome_do_cliente=nome,endereco=adress,cep=cep_cliente,telefone=tel,kwp=kilowp,marca_do_inversor=inv,marca_da_placa=placa,vendedor=vendedo)
        db.session.add(inserir)
        db.session.commit()
        return render_template('index.html')
    else:
        return render_template('novo.html')

@app.route("/atualizar")
def atualizar():
    return render_template('atualizar.html')

'''
def atualizar(username):
def deletar():
'''