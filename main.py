#Libreria para el uso de Flask
from flask import Flask, render_template, request, url_for, redirect


#libreria para el uso de la base de datos 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column  

app = Flask(__name__)
#configuro parametro SQLALCHEMY_DATABASE_URI con la ubicacion de la BD
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.sqlite"

db = SQLAlchemy(app)

#crear la base de datos y tablas 
class Todo(db.Model):
    id: Mapped [int] = mapped_column(db.Integer, primary_key=True,autoincrement=True)
    name: Mapped [str] = mapped_column(db.String, nullable=False)
    state: Mapped [str] = mapped_column(db.String, nullable=False,default='Imcompleto')

#Crea la base y las tablas necesarias con el contexto de la aplicacion
with app.app_context():
    db.create_all()

#rutas
@app.route("/", methods=['GET', 'POST'])
def home():
    #si diste click en agregar
    if request.method == 'POST' :
        name = request.form.get('name')
        if name:
            obj = Todo(name=name)
            db.session.add(obj)
            db.session.commit()
            #return f'Agregado{name}'
    py_lista_tareas = Todo.query.all()
    return render_template('select.html', lista_tareas = py_lista_tareas)

@app.route("/insert")
def insert(): 
    return'hola esto es una prueba de insertar de modificar'


@app.route("/update/<id>")
def update(id):
    obj=Todo.query.filter_by(id=id).first()
    obj.state = "Completo"
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/delete/<id>")
def delete(id):
    obj=Todo.query.filter_by(id=id).first()
    db.session.delete(obj)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
