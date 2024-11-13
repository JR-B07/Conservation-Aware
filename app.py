from flask import Flask, render_template, request, send_file, url_for, redirect, jsonify, session
import pandas as pd
from pathlib import Path
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Asegurarse de que el directorio 'data' existe
data_dir = Path('data')
data_dir.mkdir(exist_ok=True)


def initialize_dataframe(Que, etapas):
    """Inicializa el DataFrame con Que y etapas dinámicos"""
    df = pd.DataFrame(columns=['Que'] + etapas + ['Resultado Interno'])
    for Que in Que:
        df.loc[len(df)] = [Que] + [0] * (len(etapas) + 1)
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
    if 'Que' not in session:
        session['Que'] = []
    if 'etapas' not in session:
        session['etapas'] = []
    return render_template('Tabla1.html',
                           Que=session['Que'],
                           etapas=session['etapas'])


@app.route('/agregar_Que', methods=['POST'])
def agregar_Que_route():
    nuevo_Que = request.form.get('Que')
    if nuevo_Que:
        if 'Que' not in session:
            session['Que'] = []
        Que = session['Que']
        if nuevo_Que not in Que:
            Que.append(nuevo_Que)
            session['Que'] = Que
    return redirect(url_for('tabla'))


@app.route('/agregar_etapa', methods=['POST'])
def agregar_etapa_route():
    nueva_etapa = request.form.get('etapa')
    if nueva_etapa:
        if 'etapas' not in session:
            session['etapas'] = []
        etapas = session['etapas']
        if nueva_etapa not in etapas:
            etapas.append(nueva_etapa)
            session['etapas'] = etapas
    return redirect(url_for('tabla'))


@app.route('/eliminar_Que', methods=['POST'])
def eliminar_Que():
    Que_a_eliminar = request.form.get('Que')
    if Que_a_eliminar and 'Que' in session:
        session['Que'] = [Que for Que in session['Ques']
                          if Que != Que_a_eliminar]
    return redirect(url_for('tabla'))


@app.route('/eliminar_etapa', methods=['POST'])
def eliminar_etapa():
    etapa_a_eliminar = request.form.get('etapa')
    if etapa_a_eliminar and 'etapas' in session:
        session['etapas'] = [etapa for etapa in session['etapas']
                             if etapa != etapa_a_eliminar]
    return redirect(url_for('tabla'))


@app.route('/generar_tabla', methods=['POST'])
def generar_tabla():
    # Obtener Ques y etapas de la sesión
    Que = session.get('Que', [])
    etapas = session.get('etapas', [])

    # Verificar si hay Ques y etapas
    if not Ques or not etapas:
        return redirect(url_for('tabla'))

    # Crear nuevo DataFrame con los Ques y etapas actuales
    df = initialize_dataframe(Que, etapas)
    df.to_excel(data_dir / 'matriz_qfd.xlsx', index=False)

    valores = df.to_dict('records')

    return render_template('tabla_editable.html',
                           Que=Que,
                           etapas=etapas,
                           valores=valores)


@app.route('/guardar_tabla', methods=['POST'])
def guardar_tabla():
    try:
        data = request.get_json()
        df = pd.DataFrame(data['valores'])

        # Obtener las columnas actuales de la sesión
        etapas = session.get('etapas', [])
        required_columns = ['Que'] + etapas + ['Resultado Interno']

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
