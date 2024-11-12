from flask import Flask, render_template, request, send_file, url_for, redirect, jsonify, session
import pandas as pd
from pathlib import Path
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Asegurarse de que el directorio 'data' existe
data_dir = Path('data')
data_dir.mkdir(exist_ok=True)


def initialize_dataframe(aspectos, etapas):
    """Inicializa el DataFrame con aspectos y etapas dinámicos"""
    df = pd.DataFrame(columns=['Aspecto'] + etapas + ['Resultado Interno'])
    for aspecto in aspectos:
        df.loc[len(df)] = [aspecto] + [0] * (len(etapas) + 1)
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
    if 'aspectos' not in session:
        session['aspectos'] = []
    if 'etapas' not in session:
        session['etapas'] = []
    return render_template('Tabla1.html',
                           aspectos=session['aspectos'],
                           etapas=session['etapas'])


@app.route('/agregar_aspecto', methods=['POST'])
def agregar_aspecto_route():
    nuevo_aspecto = request.form.get('aspecto')
    if nuevo_aspecto:
        if 'aspectos' not in session:
            session['aspectos'] = []
        aspectos = session['aspectos']
        if nuevo_aspecto not in aspectos:
            aspectos.append(nuevo_aspecto)
            session['aspectos'] = aspectos
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


@app.route('/generar_tabla', methods=['POST'])
def generar_tabla():
    # Obtener aspectos y etapas de la sesión
    aspectos = session.get('aspectos', [])
    etapas = session.get('etapas', [])

    # Verificar si hay aspectos y etapas
    if not aspectos or not etapas:
        return redirect(url_for('tabla'))

    # Crear nuevo DataFrame con los aspectos y etapas actuales
    df = initialize_dataframe(aspectos, etapas)
    df.to_excel(data_dir / 'matriz_qfd.xlsx', index=False)

    valores = df.to_dict('records')

    return render_template('tabla_editable.html',
                           aspectos=aspectos,
                           etapas=etapas,
                           valores=valores)


@app.route('/guardar_tabla', methods=['POST'])
def guardar_tabla():
    try:
        data = request.get_json()
        df = pd.DataFrame(data['valores'])

        # Obtener las columnas actuales de la sesión
        etapas = session.get('etapas', [])
        required_columns = ['Aspecto'] + etapas + ['Resultado Interno']

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
