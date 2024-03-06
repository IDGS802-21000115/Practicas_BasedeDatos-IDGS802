from flask import Flask, render_template,request,Response
import forms

from flask_wtf.csrf import CSRFProtect
from flask import g
from flask import flash
from config import DevelopmentConfig
from models import Pizzas, db
from models import Alumnos
from models import Maestros
from pizzas import Guardar

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)


csrf=CSRFProtect()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


@app.route("/index",methods=["GET", "POST"])
def index():
    alum_form=forms.UserForm2(request.form)
    if request.method == "POST" and alum_form.validate():
        alum=Alumnos(nombre=alum_form.nombre.data,
                 apaterno=alum_form.apaterno.data,
                 email=alum_form.email.data)
        db.session.add(alum)
        db.session.commit()
    return render_template("index.html", form=alum_form)

@app.route("/ABC_Complemento", methods=["GET", "POST"])
def ABCompleto():
    alum_form=forms.UserForm2(request.form)
    alumno=Alumnos.query.all()
    return render_template("ABC_Completo.html", alumno=alumno)



@app.route("/indexmaestro",methods=["GET", "POST"])
def indexmaestro():
    maestro_form=forms.UserForm3(request.form)
    if request.method == "POST" and maestro_form.validate():
        maestro= Maestros(nombre=maestro_form.nombre.data,
                 apaterno=maestro_form.apaterno.data,
                 email=maestro_form.email.data,
                 genero=maestro_form.genero.data,
                 materia=maestro_form.materia.data,
                 )
        db.session.add(maestro)
        db.session.commit()
    return render_template("indexmaestro.html", form=maestro_form)

@app.route("/ABC_Complementomaestro", methods=["GET", "POST"])
def ABCompletoM():
    maestro_form=forms.UserForm3(request.form)
    maestro=Maestros.query.all()
    return render_template("ABC_Completomaestro.html", maestro=maestro)



@app.route("/alumnos", methods=["GET", "POST"])
def alumnos():
    
    nom=""
    apaterno=""
    correo=""
    alum_form=forms.UserForm(request.form)
    if request.method == "POST" and alum_form.validate():
        nom = alum_form.nombre.data
        correo = alum_form.email.data
        apaterno = alum_form.apaterno.data
        mensaje='Bienvenido: {}'.format(nom)
        flash(mensaje)
        print("nombre: {}".format(nom))
        print("correo: {}".format(correo))
        print("apaterno: {}".format(apaterno))
    return render_template("alumnos.html", form=alum_form, nom=nom, apaterno=apaterno,correo=correo)

@app.route("/pizzas", methods=["GET", "POST"])
def pizzas():
    pizzas_form =forms.UserForm4(request.form)
    datos_archivo = Guardar.leer_datos_archivo()  
    pizzass_bd = Pizzas.query.all() 
    try:
        if request.method == "POST" and pizzas_form.validate():
            tamaño = str(pizzas_form.tamaño.data)
            jamon = str(pizzas_form.jamon.data)
            piña = str(pizzas_form.piña.data)
            champinones = str(pizzas_form.champiñones.data)
            numero = pizzas_form.numero.data
            
            print (pizzas_form.jamon.data)
            print (pizzas_form.piña.data)
            if request.form.get("accion") == "insertar_bd":
                pizzas = Pizzas(
                    nombre=pizzas_form.nombre.data,
                    direccion=pizzas_form.direccion.data,
                    telefono=pizzas_form.telefono.data,
                    total=Guardar.sumar_subtotales()
                )
            
                db.session.add(pizzas)
                db.session.commit()
                
                flash("¡Muy bien insertado en la base de datos!")
                pizzass_bd = Pizzas.query.all() 
            elif request.form.get("accion") == "insertar_archivo":
                r = Guardar()
                result, nuevo_dato = r.unapizza(tamaño, {"jamon": jamon, "piña": piña, "champinones": champinones}, numero)

                if nuevo_dato:
                    flash("¡Muy bien insertado en el archivo de texto!")
                    datos_archivo.append(nuevo_dato) 
                else:
                    flash(f"Error al insertar en el archivo de texto: {result}")

    except Exception as e:
        flash(f"Error general: {e}")

    return render_template("pizzas.html", form=pizzas_form, datos_archivo=datos_archivo, pizzass_bd=pizzass_bd)

if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()