from flask import Flask, render_template, request, send_file, url_for, redirect, jsonify, session
import pandas as pd
from pathlib import Path
import secrets

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)

# Asegurarse de que el directorio 'data' existe
data_dir = Path('data')
data_dir.mkdir(exist_ok=True)


def initialize_dataframe(Ques, Comos):
    """Inicializa el DataFrame con Ques y Comos dinámicos"""
    df = pd.DataFrame(columns=['Ques'] + Comos + ['Resultado Interno'])
    for Que in Ques:
        df.loc[len(df)] = [Que] + [0] * (len(Comos) + 1)
    return df


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/LosQFD')
def LosQFD():
    return render_template('LosQFD.html')


@app.route('/casa')
def casa():
    return render_template('casa.html')


@app.route('/Tabla1')
def tabla():
    # Inicializar listas vacías si no existen en la sesión
    if 'Ques' not in session:
        session['Ques'] = []
    if 'Comos' not in session:
        session['Comos'] = []
    return render_template('Tabla1.html',
                           Que=session['Ques'],
                           Comos=session['Comos'])


@app.route('/agregar_Que', methods=['POST'])
def agregar_Que():
    nuevo_Que = request.form.get('Que')
    if nuevo_Que:
        if 'Ques' not in session:
            session['Ques'] = []
        Ques = session['Ques']
        if nuevo_Que not in Ques:
            Ques.append(nuevo_Que)
            session['Ques'] = Ques
    return redirect(url_for('tabla'))


@app.route('/agregar_Como', methods=['POST'])
def agregar_Como():
    nueva_Como = request.form.get('Como')
    if nueva_Como:
        if 'Comos' not in session:
            session['Comos'] = []
        Comos = session['Comos']
        if nueva_Como not in Comos:
            Comos.append(nueva_Como)
            session['Comos'] = Comos
    return redirect(url_for('tabla'))


@app.route('/eliminar_Que', methods=['POST'])
def eliminar_Que():
    Que_a_eliminar = request.form.get('Que')
    if Que_a_eliminar and 'Ques' in session:
        session['Ques'] = [Que for Que in session['Ques']
                           if Que != Que_a_eliminar]
    return redirect(url_for('tabla'))


@app.route('/eliminar_Como', methods=['POST'])
def eliminar_Como():
    Como_a_eliminar = request.form.get('Como')
    if Como_a_eliminar and 'Comos' in session:
        session['Comos'] = [Como for Como in session['Comos']
                            if Como != Como_a_eliminar]
    return redirect(url_for('tabla'))


@app.route('/generar_tabla', methods=['POST'])
def generar_tabla():
    # Obtener Ques y Comos de la sesión
    Ques = session.get('Ques', [])
    Comos = session.get('Comos', [])

    # Verificar si hay Ques y Comos
    if not Ques or not Comos:
        return redirect(url_for('tabla'))

    # Crear nuevo DataFrame con los Ques y Comos actuales
    df = initialize_dataframe(Ques, Comos)
    df.to_excel(data_dir / 'matriz_qfd.xlsx', index=False)

    valores = df.to_dict('records')

    return render_template('tabla_editable.html',
                           Que=Ques,
                           Comos=Comos,
                           valores=valores)


@app.route('/guardar_tabla', methods=['POST'])
def guardar_tabla():
    try:
        data = request.get_json()
        df = pd.DataFrame(data['valores'])

        # Obtener las columnas actuales de la sesión
        Comos = session.get('Comos', [])
        required_columns = ['Ques'] + Comos + ['Resultado Interno']

        # Asegurarse de que todas las columnas necesarias estén presentes
        for col in required_columns:
            if col not in df.columns:
                df[col] = 0

        # Guardar el DataFrame
        df.to_excel(data_dir / 'matriz_qfd.xlsx', index=False)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


@app.route('/descargar_excel')
def descargar_excel():
    try:
        return send_file(
            data_dir / 'matriz_qfd.xlsx',
            as_attachment=True,
            download_name='matriz_qfd.xlsx'
        )
    except Exception as e:
        return str(e), 400


if __name__ == '__main__':
    app.run(port=3000, debug=True)
