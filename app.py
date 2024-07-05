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
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM albums')
        consultaA = cursor.fetchall()
        return render_template('index.html', albums=consultaA)
    except Exception as e:
        print(e)
        return "Error al realizar la consulta", 500

@app.route('/guardarAlbum', methods=['POST'])
def guardarAlbum():
    if request.method == 'POST':
        FTitulo = request.form['txtTitulo']
        FArtista = request.form['txtArtista']
        FAño = request.form['txtAnio']
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO albums (titulo, artista, anio) VALUES (%s, %s, %s)", (FTitulo, FArtista, FAño))
            mysql.connection.commit()
            flash('Álbum Guardado Correctamente')
            return redirect(url_for('index'))
        except Exception as e:
            print(e)
            flash('Error al guardar en la base de datos', 'error')
            return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM albums WHERE id=%s', [id])
        albumE = cursor.fetchone()
        return render_template('editar.html', album=albumE)
    except Exception as e:
        print(e)
        return "Error al realizar la consulta", 500

@app.route('/ActualizarAlbum/<int:id>', methods=['POST'])
def ActualizarAlbum(id):
    if request.method == 'POST':
        try:
            Ftitulo = request.form['txtTitulo']
            Fartista = request.form['txtArtista']
            Fanio = request.form['txtAnio']

            cursor = mysql.connection.cursor()
            cursor.execute('UPDATE albums SET titulo=%s, artista=%s, anio=%s WHERE id=%s', (Ftitulo, Fartista, Fanio, id))
            mysql.connection.commit()
            flash('Álbum editado correctamente')
            return redirect(url_for('index'))
        except Exception as e:
            print(e)
            flash('Error al actualizar el álbum', 'error')
            return redirect(url_for('editar', id=id))

@app.route('/EliminarAlbum/<int:id>')
def eliminar(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM albums WHERE id=%s', [id])
        mysql.connection.commit()
        flash('Álbum eliminado')
        return redirect(url_for('index'))
    except Exception as e:
        print(e)
        flash('Error al eliminar álbum', 'error')
        return redirect(url_for('index'))

@app.errorhandler(404)
def paginanotfound(e):
    return 'Revisa tu sintaxis: No encontré nada', 404

if __name__ == '__main__':
    app.run(port=3000, debug=True)