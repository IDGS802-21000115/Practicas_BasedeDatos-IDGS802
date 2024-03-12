from wtforms import Form
from wtforms import StringField, TextAreaField, SelectField, RadioField, IntegerField,BooleanField,SelectMultipleField
from wtforms import EmailField
from wtforms import validators

 
class UserForm(Form):
    nombre = StringField("nombre",[validators.DataRequired(message='el campo es requerido'), validators.Length(min=4,max=10,message='ingresa nombre valido')])
    email = EmailField("materno")
    apaterno = StringField("apaterno")
    edad=IntegerField('edad',[validators.number_range(min=1,max=20,message='valor no valido')])
    materias = SelectField(choices=[('Español','Esp'),('Mat','Matematicas'),('Ingles','Ing')])
    radios = RadioField('Curso',choices=[("1", "1"),("2", "2"),("3", "3")])
    correo=EmailField('correo',[validators.Email(message='Ingrese un correo valido')])

 
class UserForm2(Form):
    id =IntegerField("id")
    nombre = StringField("nombre",[validators.DataRequired(message='el campo es requerido'), validators.Length(min=4,max=10,message='ingresa nombre valido')])
    apaterno = StringField("apaterno")
    email=EmailField('email')

class UserForm3(Form):
    id =IntegerField("id")
    nombre = StringField("nombre",[validators.DataRequired(message='el campo es requerido'), validators.Length(min=4,max=10,message='ingresa nombre valido')])
    apaterno = StringField("apaterno")
    email=EmailField('email')
    genero=StringField('genero')
    materia=StringField('materia')


class UserForm4(Form):
    id =IntegerField("id")
    nombre = StringField("nombre",[validators.DataRequired(message='el campo es requerido'), validators.Length(min=1,max=10,message='ingresa nombre valido')])
    telefono = StringField("telefono")
    total =IntegerField("total")
    direccion=StringField('direccion')
    tamaño = RadioField('tamaño',choices=[("chica", "chica"),("mediana", "mediana"),("grande", "grande")])
    jamon = BooleanField("Jamon")
    piña = BooleanField("Piña")
    champiñones = BooleanField("Champiñon")
    
    numero =IntegerField("numero")
    ventasm=StringField("ventasm")
    ventasd=StringField("ventasd")
    fecha=StringField("fecha")