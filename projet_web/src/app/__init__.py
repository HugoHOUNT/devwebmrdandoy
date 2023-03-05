from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

from myapp import db
from myapp.app import app
from myapp.models import Data

import os
import json



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
# db.init_app(app)

class Data(db.Model):
    __tablename__ = "data"

    id = db.Column(db.Integer, primary_key=True)
    rna_id = db.Column(db.String(30), nullable=True)
    rna_id_ex = db.Column(db.String(20), nullable=True)
    gestion = db.Column(db.String(20), nullable=True)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/assos')
def assos():
    datas = Data.query.limit(10).all()
    for data in datas:
        print(f"{data.rna_id}")

    #stmt = select(Data)
    #result = db.session.execute(stmt)
    #for data in result.scalars():
    #  print(f"{data.rna_id}")

    return render_template('assos.html', datas=datas)

@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        rna_id = request.form['rna_id']
        rna_id_ex = request.form['rna_id_ex']
        gestion = request.form['gestion']

        new_data = Data(rna_id=rna_id, rna_id_ex=rna_id_ex, gestion=gestion)
        db.session.add(new_data)
        db.session.commit()

        return redirect('/assos')

    return render_template('add.html')

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    data = Data.query.get(id)

    if request.method == 'POST':
        data.rna_id = request.form['rna_id']
        data.rna_id_ex = request.form['rna_id_ex']
        data.gestion = request.form['gestion']

        db.session.commit()

        return redirect('/assos')

    return render_template('edit.html', data=data)


@app.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete(id):
    data_to_delete = Data.query.get_or_404(id)

    if request.method == 'POST':
        db.session.delete(data_to_delete)
        db.session.commit()
        return redirect(url_for('assos'))
    else:
        return render_template('delete.html', data=data_to_delete)

@app.route('/chart')
def chart():
    # Récupération des données
    query = db.session.query(Data.gestion, func.count(Data.gestion)).group_by(Data.gestion).all()
    gestion_labels = [row[0] for row in query]
    gestion_counts = [row[1] for row in query]

    # Rendu du template HTML avec les données
    return render_template('chart.html', gestion_labels=gestion_labels, gestion_counts=gestion_counts)

if __name__ == '__main__':
    app.run()
