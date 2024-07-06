from flask import Flask, flash, redirect, request, render_template, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'conservationaware'
app.secret_key = 'your_secret_key'
mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sobre_nosotros')
def sobre_nosotros():
    return render_template('sobre_nosotros.html')


@app.route('/animales')
def animales():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM animals")
        animals = cursor.fetchall()
        cursor.close()
        return render_template('animales.html', animals=animals)
    except Exception as e:
        print(e)
        flash('Error al obtener los datos de la base de datos', 'error')
        return redirect(url_for('index'))


@app.route('/donar')
def donar():
    return render_template('donar.html')


@app.route('/asociaciones')
def asociaciones():
    return render_template('asociaciones.html')


@app.errorhandler(404)
def pagina_no(e):
    return 'PÁGINA NO ENCONTRADA'


if __name__ == '__main__':
    app.run(port=3000, debug=True)
