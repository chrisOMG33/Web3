from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

from data.clsConexion import clsConexion
from data.clsDatos import clsDatos

conex = clsConexion()

@app.route('/login')
def login():
    return redirect('http://127.0.0.1:8000/accounts/login')


@app.route('/')
def index():
    return render_template('index.html', datos=conex.consultar())


@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == "POST":
        if conex.agregar(clsDatos(0, request.form['txtTexto'], request.form['txtDescrip'])):
            app.logger.debug("Datos almacenados correctamente")
        else:
            app.logger.debug("Se presentó un problema con los datos")
        return redirect(url_for("index"))
    else:
        return render_template('agregar.html')


@app.route('/modificar/<int:ide>', methods=['GET'])
def modificar(ide):
    return render_template('modificar.html', datos=conex.consultar(ide))


@app.route('/exec_modificar', methods=['POST'])
def exec_modificar():
    if conex.editar(clsDatos(request.form['txtID'], request.form['txtTexto'], request.form['txtDescrip'])):
        app.logger.debug("Datos modificados correctamente")
    else:
        app.logger.debug("Se presentó un problema con los datos")
    return redirect(url_for('index'))


@app.route('/exec_eliminar/<int:ide>', methods=['GET'])


def exec_eliminar(ide):
    if conex.borrar(ide):
        app.logger.debug("Datos eliminado correctamente")
    else:
        app.logger.debug("Se presentó un problema con los datos")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
