from flask import Flask, render_template, request, redirect, url_for
from datetime import date
from imprimircontrato import impContrato
from imprimirchecklist import printExcel
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

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
    cidade = db.Column(db.String(30))
    endereco = db.Column(db.String(120), unique=False, nullable=True)
    cep = db.Column(db.Integer, unique=False, nullable=False)
    cpf = db.Column(db.Integer)
    telefone = db.Column(db.Integer, unique=False, nullable=False)
    kwp = db.Column(db.Integer, unique=False, nullable=False)
    preco = db.Column(db.Integer, unique=False, nullable=False)
    marca_do_inversor = db.Column(db.String(30), unique=False, nullable=True)
    marca_da_placa = db.Column(db.String(16), unique=False, nullable=False)
    monitorando = db.Column(db.Boolean, default=False)

@app.route("/")
def index():
    dados = User.query.order_by(User.data).all()
    return render_template('index.html', dados=dados)

@app.route("/status")
def home():
    dados = User.query.filter_by(monitorando=False)
    return render_template('index.html', dados=dados)

@app.route("/novo", methods=['POST','GET'])
def novo():
    if request.method == 'POST':
        nome = request.form['nome']
        adress = request.form['endereco']
        city = request.form['cidade']
        cep_cliente = request.form['cep']
        cpf = request.form['cpf']
        tel = request.form['telefone']
        kilowp = request.form['kwp']
        preco = request.form['preco']
        inv = request.form['inv']
        placa = request.form['placa']
        try:
            inserir = User(data=date,nome_do_cliente=nome,endereco=adress,cep=cep_cliente,cpf=cpf,cidade=city,telefone=tel,kwp=kilowp,preco=preco,marca_do_inversor=inv,marca_da_placa=placa)
            db.session.add(inserir)
            db.session.commit()
            print('commit to db successful')
        except:
            print('database commit error')
        return redirect(url_for('novo'))
    else:
        return render_template('novo.html')

@app.route("/atualizar/<int:id>", methods=['POST','GET'])
def atualizar(id):
    if request.method == 'POST':
        usuarioobj = User.query.filter_by(_id=id).first()
        try:
            preco = request.form['preco']
            monitor = request.form['monitor']
            usuarioobj.monitorando = True
            usuarioobj.preco = preco
        except:
            usuarioobj.monitorando = False
            usuarioobj.preco = preco               
        db.session.add(usuarioobj)
        db.session.commit() 
        return redirect(url_for('index'))
    else:
        dados = User.query.filter_by(_id=id).all()
        return render_template('atualizar.html', dados=dados)

@app.route("/contrato/<int:id>")
def contrato(id):
    objeto = User.query.filter_by(_id=id).first()
    try:
        impContrato(
        objeto.nome_do_cliente,
        objeto.endereco,
        objeto.cidade,
        objeto.cpf,
        objeto.kwp,
        objeto.marca_da_placa,
        objeto.marca_do_inversor,
        str(objeto.preco))
        print("contrato sucesso")
        return redirect(url_for('index'))
    except:
        print("contrato falhou")
        return redirect(url_for('index'))


@app.route("/deletar/<int:id>")
def deletar(id):
    usuarioobj = User.query.filter_by(_id=id).first()
    db.session.delete(usuarioobj)
    db.session.commit()    
    return redirect(url_for('index'))
