from flask import *
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
        animales = cursor.fetchall()
        cursor.close()
        return render_template('animales.html', animals=animales)
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


@app.route('/guardarAnimal', methods=['POST'])
def guardarAnimal():
    if request.method == 'POST':
        common_name = request.form['common_name']
        scientific_name = request.form['scientific_name']
        description = request.form['description']
        estimated_population = request.form['estimated_population']
        image_url = request.form['image_url']
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                "INSERT INTO animals (common_name, scientific_name, description, estimated_population, image_url) VALUES (%s, %s, %s, %s, %s)",
                (common_name, scientific_name, description, estimated_population, image_url))
            mysql.connection.commit()
            flash('Animal guardado correctamente')
            return redirect(url_for('animales'))
        except Exception as e:
            print(e)
            flash('Error al guardar en la base de datos', 'error')
            return redirect(url_for('animales'))


@app.route('/editar/<int:id>')
def editar(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM animals WHERE id=%s', [id])
        animal = cursor.fetchone()
        return render_template('editar.html', animal=animal)
    except Exception as e:
        print(e)
        return "Error al realizar la consulta", 500


@app.route('/ActualizarAnimal/<int:id>', methods=['POST'])
def ActualizarAnimal(id):
    if request.method == 'POST':
        try:
            common_name = request.form['common_name']
            scientific_name = request.form['scientific_name']
            description = request.form['description']
            estimated_population = request.form['estimated_population']
            image_url = request.form['image_url']

            cursor = mysql.connection.cursor()
            cursor.execute(
                'UPDATE animals SET common_name=%s, scientific_name=%s, description=%s, estimated_population=%s, image_url=%s WHERE id=%s',
                (common_name, scientific_name, description, estimated_population, image_url, id))
            mysql.connection.commit()
            flash('Animal editado correctamente')
            return redirect(url_for('animales'))
        except Exception as e:
            print(e)
            flash('Error al actualizar el animal', 'error')
            return redirect(url_for('editar', id=id))


@app.errorhandler(404)
def pagina_no(e):
    return 'PÁGINA NO ENCONTRADA'


if __name__ == '__main__':
    app.run(port=3000, debug=True)
