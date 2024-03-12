from cgitb import text
import datetime
import os
from flask import Flask, render_template,request,Response
import forms
from sqlalchemy import cast, Date
from flask_wtf.csrf import CSRFProtect
from flask import g
from flask import flash
from config import DevelopmentConfig
from models import Pizzas, db
from models import Alumnos
from models import Maestros
from pizzas import Guardar
from datetime import datetime
from datetime import date
from sqlalchemy import extract, func


from datetime import date


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
    total_ventas_mes=0
    total_ventas_hoy=0
    pizzass_bdd=[]
    pizzas_form =forms.UserForm4(request.form)
    datos_archivo = []
    pizzass_bd =[]
    
    try:
        if request.method == "POST" and pizzas_form.validate():
            tamaño = str(pizzas_form.tamaño.data)
            numero = pizzas_form.numero.data
            ingredientes = {}
            if pizzas_form.jamon.data:
                ingredientes["jamon"] = True
            if pizzas_form.piña.data:
                ingredientes["piña"] = True
            if pizzas_form.champiñones.data:
                ingredientes["champiñones"] = True
            
            
            print (pizzas_form.jamon.data)
            print (pizzas_form.piña.data)
            if request.form.get("accion") == "insertar_bd":
            
                pizzas = Pizzas(
                    nombre=pizzas_form.nombre.data,
                    direccion=pizzas_form.direccion.data,
                    telefono=pizzas_form.telefono.data,
                    fecha=pizzas_form.fecha.data,
                    total=Guardar.sumar_subtotales()
                )
            
                db.session.add(pizzas)
                db.session.commit()
                
                flash("¡Muy bien insertado en la base de datos!")
                os.remove("pizzas.txt")

            elif request.form.get("accion") == "insertar_archivo":
                r = Guardar()
                
                print(ingredientes)
                result = r.unapizza(tamaño, ingredientes, numero)

                if result:
                    flash("¡Muy bien insertado en el archivo de texto!")
                    datos_archivo.append(result) 
                    datos_archivo = Guardar.leer_datos_archivo()
                    print(datos_archivo)
                else:
                    flash(f"Error al insertar en el archivo de texto: {result}")
                    
            elif request.form.get("accion") == "eliminar_ultima_archivo":
                r = Guardar()
                result = r.eliminar_ultima_pizza()
                flash(result)
                datos_archivo = Guardar.leer_datos_archivo()
                print(datos_archivo)
            
            elif request.form.get("accion") == "consultar_bd":
                dia_actual = pizzas_form.ventasd.data.lower()  
    
                print(dia_actual)
    
                dias_ingles = {
                'lunes': 2,  
                'martes': 3,
                'miércoles': 4,
                'jueves': 5,
                'viernes': 6,
                'sábado': 7,
                'domingo': 1  
                }

                dia_ingles = dias_ingles.get(dia_actual)
                

                if dia_ingles:
                    pizzass_bd = Pizzas.query.filter(func.DAYOFWEEK(Pizzas.fecha) ==  dia_ingles).all()
                    print(pizzass_bd)
                    total_ventas_hoy = sum(pizza.total for pizza in pizzass_bd)
                    print(total_ventas_hoy)
                    for pizza in pizzass_bd:
                        print(f"Pizza ID: {pizza.id}, Nombre: {pizza.nombre}, Total: {pizza.total}, Fecha de Creación: {pizza.create_date}")
                else:
                    print("Día no válido")
                    pizzass_bd = []
                

            elif request.form.get("accion") == "consultar_bd_mes":
              mes_actual = pizzas_form.ventasm.data.lower()  
    
              print(mes_actual)
              
              meses_ingles = {
                'enero': '01',
                'febrero': '02',
                'marzo': '03',
                'abril': '04',
                'mayo': '05',
                'junio': '06',
                'julio': '07',
                'agosto': '08',
                'septiembre': '09',
                'octubre': '10',
                'noviembre': '11',
                'diciembre':  '12'
               }
        
    
              mes_ingles = meses_ingles.get(mes_actual)
              
              if mes_ingles:

        
                pizzass_bd = Pizzas.query.filter(func.extract('month', Pizzas.fecha) == int(mes_ingles)).all()
                
                print(pizzass_bd)
                total_ventas_mes = sum(pizza.total for pizza in pizzass_bd)
                print(total_ventas_mes)
                for pizza in pizzass_bd:
                 print(f"Pizza ID: {pizza.id}, Nombre: {pizza.nombre}, Total: {pizza.total}, Fecha de Creación: {pizza.create_date}")
                 
              else:
                print("Mes no válido")
                total_ventas_mes = 0
           
           
        
    except Exception as e:
        print(f"Error general: {e}")
    totalito=Guardar.sumar_subtotales()
    return render_template("pizzas.html", form=pizzas_form, datos_archivo=datos_archivo, pizzass_bd=pizzass_bd, total_ventas_hoy=total_ventas_hoy, pizzass_bdd=pizzass_bdd, totalito=totalito, total_ventas_mes=total_ventas_mes)

if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()