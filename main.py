from flask import Flask, render_template, request, jsonify
from datetime import date

from flask.wrappers import Response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['TESTING'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

date = date.today()

class User(db.Model):
    __tablename__ = "User"
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(db.DateTime)
    nome_do_cliente = db.Column(db.String(80), unique=False, nullable=False)
    cidade = db.Column(db.String(30), unique=False)
    endereco = db.Column(db.String(120), unique=False, nullable=True)
    cep = db.Column(db.Integer, unique=False, nullable=False)
    telefone = db.Column(db.Integer, unique=False, nullable=False)
    kwp = db.Column(db.Integer, unique=False, nullable=False)
    marca_do_inversor = db.Column(db.String(30), unique=False, nullable=True)
    marca_da_placa = db.Column(db.String(16), unique=False, nullable=False)
    monitorando = db.Column(db.Boolean, default=False)

@app.route("/")
def index():
    dados = User.query.order_by(User.data).all()
    return render_template('index.html', dados=dados)

@app.route("/status")
def home():
    dados = User.query.filter_by(monitorando=True)
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
        inserir = User(data=date,nome_do_cliente=nome,endereco=adress,cep=cep_cliente,telefone=tel,kwp=kilowp,marca_do_inversor=inv,marca_da_placa=placa)
        db.session.add(inserir)
        db.session.commit()
        return render_template('index.html')
    else:
        return render_template('novo.html')

@app.route("/atualizar/<int:id>", methods=['POST','GET'])
def atualizar(id):
    if request.method == 'POST':
        nome = request.form['nome']
        adress = request.form['endereco']
        city = request.form['cidade']
        cep_cliente = request.form['cep']
        tel = request.form['telefone']
        kilowp = request.form['kwp']
        inv = request.form['inv']
        placa = request.form['placa']
        monitor = request.form['monitor']
        if monitor == 'on':
            monitor = True
        else:
            monitor = False
        inserir = User.query.filter_by(_id=id).update(nome_do_cliente=nome,endereco=adress,cep=cep_cliente,telefone=tel,kwp=kilowp,marca_do_inversor=inv,marca_da_placa=placa,monitorando=monitor)
        db.session.add(inserir)
        db.session.commit()
        return render_template('index.html')
    else:
        dados = User.query.filter_by(_id=id).all()
        return render_template('atualizar.html', dados=dados)

'''
def deletar():
'''