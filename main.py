from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import psycopg2.extras
import os


app = Flask(__name__)

def connectDB():
    connectionString='dbname=taxhelp user=cata password=catacata host=localhost'
    print(connectionString)
    try:
        return psycopg2.connect(connectionString)
    except:
        print("No se pudo conectar.")

@app.route('/')
def index():

    conectar = connectDB()
    cursor=conectar.cursor()
    cursor.execute("""SELECT distinct anio FROM IA;""")
        
    anios=cursor.fetchall()

    return render_template('index.html', anios=anios)

@app.route('/calculo/<int:anio>')
def calculo(anio):

    conectar = connectDB()
    cursor=conectar.cursor()
    cursor.execute(f"""SELECT * FROM IA WHERE anio={anio};""")
        
    ans=cursor.fetchall()
   
    return render_template('calculo.html', ans=ans)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method=='GET':
        return render_template('adminlogin.html')
    else:

        user = request.form.get("password")

        if user=='sii123':

            conectar = connectDB()
            cursor=conectar.cursor()
            cursor.execute("""SELECT desde, hasta, factor, CR, anio
                            FROM IA order by anio, factor; """)
        
            datos=cursor.fetchall()

            conectar = connectDB()
            cursor=conectar.cursor()
            cursor.execute("""SELECT mes, porcentaje, anio
                            FROM CM order by anio; """)

            cm=cursor.fetchall()

            ctx = {
            "datos" : datos,
            "cm" : cm
            }

            return render_template('admin.html', contexto=ctx)

        else:
             return render_template('index.html')

@app.route('/ingresarcm', methods=['GET', 'POST'])
def ingresarcm():

    if request.method=='GET':
        return render_template('ingresarcm.html')

    else:

        mes = request.form.get("mes")
        porcentaje = request.form.get("porcentaje")
        anio = request.form.get("anio")

        sql = 'INSERT INTO CM (mes, porcentaje, anio) VALUES(%s,%s,%s)'

        datos = (mes, porcentaje, anio)

        conectar = connectDB()
        cursor=conectar.cursor()

        cursor.execute(sql, datos)

        conectar.commit()

    return render_template('admin.html')

@app.route('/ingresaria')
def ingresaria():

    return render_template('ingresaria.html')


if __name__ == '__main__':
    app.run(debug=True)