from flask import Flask, render_template, request, redirect, url_for
from datetime import date
from officepack import impContrato, printExcel
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

class Estoque(db.Model):
    __tablename__ = "Estoque"
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    placa360 = db.Column(db.Integer)
    placa440 = db.Column(db.Integer)
    placa445 = db.Column(db.Integer)
    placa450 = db.Column(db.Integer)
    placa455 = db.Column(db.Integer)
    placa545 = db.Column(db.Integer)
    placa550 = db.Column(db.Integer)
    microinversor = db.Column(db.Integer)
    microinversor2k = db.Column(db.Integer)
    inversor2k = db.Column(db.Integer)
    inversor3k = db.Column(db.Integer)
    inversor5k = db.Column(db.Integer)
    inversor6k = db.Column(db.Integer)
    inversorupper = db.Column(db.String(30))

@app.route("/")
def index():
    dados = User.query.order_by(User.data).all()
    return render_template('index.html', dados=dados)

@app.route("/estoque", methods=['POST','GET'])
def estoque():
    if request.method == 'POST':
        objetosolar = Estoque.query.filter_by(_id=1).first()
        try:
            objetosolar.placa360 = request.form['placa360']
            objetosolar.placa440 = request.form['placa440']
            objetosolar.placa445 = request.form['placa445']
            objetosolar.placa450 = request.form['placa450']
            objetosolar.placa455 = request.form['placa455']
            objetosolar.placa545 = request.form['placa545']
            objetosolar.placa550 = request.form['placa550']
            objetosolar.microinversor = request.form['microinversor']
            objetosolar.microinversor2k = request.form['microinversor2k']
            objetosolar.inversor2k = request.form['inversor2k']
            objetosolar.inversor3k = request.form['inversor3k']
            objetosolar.inversor5k = request.form['inversor5k']
            objetosolar.inversor6k = request.form['inversor6k']
            objetosolar.inversorupper = request.form['inversorupper']
            #inserir = Estoque(placa360=placa360,placa440=placa440,placa445=placa445,placa450=placa450,placa455=placa455,placa545=placa545,placa550=placa550,microinversor=microinversor,microinversor2k=microinversor2k,inversor2k=inversor2k,inversor3k=inversor3k,inversor5k=inversor5k,inversor6k=inversor6k,inversorupper=inversorupper)
            db.session.add(objetosolar)
            db.session.commit()
            printExcel()
        except:
            return redirect(url_for('estoque'))
    else:
        dados = Estoque.query.order_by(Estoque._id).all()
        return render_template('estoque.html', dados=dados)

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
        inserir = User(data=date,nome_do_cliente=nome,endereco=adress,cep=cep_cliente,cpf=cpf,cidade=city,telefone=tel,kwp=kilowp,preco=preco,marca_do_inversor=inv,marca_da_placa=placa)
        db.session.add(inserir)
        db.session.commit()
        impContrato(nome, adress, city, cpf, kilowp,placa,inv,preco)
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

@app.route("/deletar/<int:id>")
def deletar(id):
    usuarioobj = User.query.filter_by(_id=id).first()
    db.session.delete(usuarioobj)
    db.session.commit()    
    return redirect(url_for('index'))
