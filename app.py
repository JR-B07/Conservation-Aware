from flask import Flask, render_template, request, send_file, jsonify
import pandas as pd
import os

app = Flask(__name__)

# Ruta principal


@app.route('/')
def index():
    return render_template('index.html')

# Nueva ruta para la tabla interactiva basada en la imagen


@app.route('/tabla', methods=['GET', 'POST'])
def tabla():
    # Ruta relativa dentro de tu proyecto
    file_path = os.path.join('data', 'Equipoo4 (1).xlsx')

    if request.method == 'POST':
        # Obtener los datos del formulario y crear un DataFrame
        data = request.form.to_dict(flat=False)
        columnas = list(data.keys())
        filas = zip(*data.values())

        df = pd.DataFrame(filas, columns=columnas)

        # Guardar los datos modificados en un archivo Excel
        output_path = os.path.join('data', 'tabla_modificada.xlsx')
        df.to_excel(output_path, index=False)

        # Enviar el archivo al usuario
        return send_file(output_path, as_attachment=True)

    # Leer el archivo Excel original
    df = pd.read_excel(file_path)
    columnas = df.columns.tolist()
    datos = df.values.tolist()

    return render_template('tabla.html', columnas=columnas, datos=datos)
# Ruta adicional para otra página (LosQFD)


@app.route('/guardar', methods=['POST'])
def guardar():
    # Obtener los datos enviados desde el formulario
    data = request.form.to_dict(flat=False)

    # Extraer la estructura de los datos
    filas = []
    for i in range(len(data['valor_0_0'])):
        fila = []
        for clave in data:
            fila.append(data[clave][i])
        filas.append(fila)

    # Crear un DataFrame de Pandas con los datos modificados
    columnas = ["PRIORIDAD", "Características", "Recepción del maíz", "Almacenaje",
                "Elaboración", "Lavado", "Molienda", "Deshidratado", "Envasado"]
    df = pd.DataFrame(filas, columns=columnas)

    # Guardar el DataFrame en un archivo Excel
    output_path = 'tabla_modificada.xlsx'
    df.to_excel(output_path, index=False)

    # Enviar el archivo Excel al cliente para descargar
    return send_file(output_path, as_attachment=True)


@app.route('/LosQFD')
def LosQFD():
    return render_template('LosQFD.html')


@app.route('/update_table', methods=['POST'])
def update_table():
    headers = request.json.get('headers')  # Nombres de las columnas
    data = request.json.get('data')  # Datos de la tabla
    print("Encabezados recibidos:", headers)
    print("Datos recibidos:", data)
    # Aquí podrías procesar los datos o almacenarlos en una base de datos
    return jsonify({"status": "success"})


# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(port=3000, debug=True)
