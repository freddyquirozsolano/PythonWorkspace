from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Configuración de la base de datos
DATABASE = 'estudiantes.db'

# Crear la tabla de estudiantes si no existe
def crear_tabla():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS estudiantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            apellido TEXT,
            cedula TEXT,
            sexo TEXT,
            direccion TEXT,
            telefono TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Obtener todos los estudiantes
def obtener_estudiantes():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM estudiantes')
    estudiantes = cursor.fetchall()
    conn.close()
    return estudiantes

# Agregar un nuevo estudiante
def agregar_estudiante(nombre, apellido, cedula, sexo, direccion, telefono):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO estudiantes (nombre, apellido, cedula, sexo, direccion, telefono) VALUES (?, ?, ?, ?, ?, ?)',
                   (nombre, apellido, cedula, sexo, direccion, telefono))
    conn.commit()
    conn.close()

# Obtener un estudiante por su ID
def obtener_estudiante(id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM estudiantes WHERE id = ?', (id,))
    estudiante = cursor.fetchone()
    conn.close()
    return estudiante

# Actualizar un estudiante
def actualizar_estudiante(id, nombre, apellido, cedula, sexo, direccion, telefono):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('UPDATE estudiantes SET nombre = ?, apellido = ?, cedula = ?, sexo = ?, direccion = ?, telefono = ? WHERE id = ?',
                   (nombre, apellido, cedula, sexo, direccion, telefono, id))
    conn.commit()
    conn.close()

# Eliminar un estudiante
def eliminar_estudiante(id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM estudiantes WHERE id = ?', (id,))
    conn.commit()
    conn.close()

# Rutas de la aplicación
@app.route('/')
def index():
    estudiantes = obtener_estudiantes()
    return render_template('index.html', estudiantes=estudiantes)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        cedula = request.form['cedula']
        sexo = request.form['sexo']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        agregar_estudiante(nombre, apellido, cedula, sexo, direccion, telefono)
        return redirect(url_for('index'))
    return render_template('agregar.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    estudiante = obtener_estudiante(id)
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        cedula = request.form['cedula']
        sexo = request.form['sexo']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        actualizar_estudiante(id, nombre, apellido, cedula, sexo, direccion, telefono)
        return redirect(url_for('index'))
    return render_template('editar.html', estudiante=estudiante)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    eliminar_estudiante(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    crear_tabla()
    app.run(port=5001)