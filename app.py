import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv  # Importar dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] =  os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Modelo de la base de datos para productos
class Producto(db.Model):
    __tablename__ = 'productos'
    __table_args__ = {'schema': 'productoss'}  # Especifica el esquema

    producto_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    categoria_id = db.Column(db.Integer, nullable=True)

    def to_dict(self):
        return {
            'producto_id': self.producto_id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': str(self.precio),
            'categoria_id': self.categoria_id
        }

# Rutas con vistas

# Mostrar todos los alumnos
@app.route('/')
def index():
    productos = Producto.query.all()
    return render_template('index.html', productos=productos)


# Crear un nuevo producto (formulario)
@app.route('/productos/new', methods=['GET', 'POST'])
def create_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        categoria_id = request.form['categoria_id']

        nuevo_producto = Producto(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            categoria_id=categoria_id
        )
        db.session.add(nuevo_producto)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('create_producto.html')


# Actualizar un producto (formulario)
@app.route('/productos/update/<int:producto_id>', methods=['GET', 'POST'])
def update_producto(producto_id):
    producto = Producto.query.get(producto_id)
    if request.method == 'POST':
        producto.nombre = request.form['nombre']
        producto.descripcion = request.form['descripcion']
        producto.precio = request.form['precio']
        producto.categoria_id = request.form['categoria_id']

        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update_producto.html', producto=producto)

# Eliminar un producto
@app.route('/productos/delete/<int:producto_id>')
def delete_producto(producto_id):
    producto = Producto.query.get(producto_id)
    if producto:
        db.session.delete(producto)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

