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
    df = pd.DataFrame(columns=['Ques'] + Comos + ['Total', 'Valor'])
    for Que in Ques:
        # Inicializar cada fila con 0 y calcular Total y Valor
        row = [Que] + [0] * len(Comos) + [0, 0]
        df.loc[len(df)] = row
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


@app.route('/tabla_editable')
def tabla_editable():
    """Vista para mostrar la tabla generada"""
    qfd_data = session.get('qfd_data', [])
    return render_template('tabla_editable.html', qfd_data=qfd_data)


@app.route('/generar_tabla', methods=['POST'])
def generar_tabla():
    try:
        Ques = request.form.get('ques').split(',')
        Comos = request.form.get('comos').split(',')

        # Validar que los datos sean correctos
        if not Ques or not Comos:
            return redirect(url_for('tabla_editable'))

        # Crear la tabla
        df = initialize_dataframe(Ques, Comos)
        session['qfd_data'] = df.to_dict('records')

        return redirect(url_for('tabla_editable'))
    except Exception as e:
        return f"Error al generar la tabla: {str(e)}", 400


@app.route('/guardar_tabla', methods=['POST'])
def guardar_tabla():
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Alignment, Font, PatternFill

        # Obtener los valores de la tabla desde la sesión
        qfd_data = session.get('qfd_data', [])
        if not qfd_data:
            return jsonify({'status': 'error', 'message': 'No hay datos para guardar'}), 400

        # Obtener Ques y Comos desde los datos
        Ques = [row['Ques'] for row in qfd_data]
        Comos = list(qfd_data[0].keys())
        Comos.remove('Ques')
        Comos.remove('Total')
        Comos.remove('Valor')

        # Crear un libro de Excel
        excel_path = data_dir / 'matriz_qfd.xlsx'
        wb = Workbook()
        ws = wb.active
        ws.title = "Matriz QFD"

        # Escribir los encabezados de los Comos
        for col, como in enumerate(Comos, start=2):
            cell = ws.cell(row=1, column=col, value=como)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.fill = PatternFill(
                start_color="CCFFFF", end_color="CCFFFF", fill_type="solid")

        # Escribir los encabezados adicionales (Total, Valor)
        extra_headers = ["Total", "Valor"]
        for col, header in enumerate(extra_headers, start=2 + len(Comos)):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.fill = PatternFill(
                start_color="CCFFFF", end_color="CCFFFF", fill_type="solid")

        # Escribir las filas de Ques y sus datos
        for row, que in enumerate(Ques, start=2):
            ws.cell(row=row, column=1, value=que).font = Font(bold=True)
            for col, como in enumerate(Comos, start=2):
                ws.cell(row=row, column=col,
                        value=qfd_data[row - 2].get(como, 0))

            # Escribir valores de Total y Valor
            ws.cell(row=row, column=2 + len(Comos),
                    value=qfd_data[row - 2].get('Total', 0))
            ws.cell(row=row, column=3 + len(Comos),
                    value=qfd_data[row - 2].get('Valor', 0))

        # Ajustar tamaño de las columnas
        for col in ws.columns:
            max_length = 0
            col_letter = col[0].column_letter
            for cell in col:
                try:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                except:
                    pass
            ws.column_dimensions[col_letter].width = max_length + 2

        # Guardar el archivo
        if excel_path.exists():
            excel_path.unlink()  # Elimina si ya existe
        wb.save(excel_path)

        return jsonify({
            'status': 'success',
            'redirect_url': url_for('tabla_editable'),
            'message': 'Tabla guardada correctamente'
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


@app.route('/descargar_excel')
def descargar_excel():
    try:
        file_path = data_dir / 'matriz_qfd.xlsx'  # Ruta del archivo generado
        if not file_path.exists():
            return "Archivo no encontrado. Asegúrate de haber generado la tabla antes de descargar.", 400

        return send_file(
            file_path,
            as_attachment=True,
            download_name='matriz_qfd1.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(port=3000, debug=True)
