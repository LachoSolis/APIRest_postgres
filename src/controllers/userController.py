from flask import jsonify
from src.models.user import User, db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

@jwt_required()
def crear_usuario(data):
    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')
    direccion = data.get('direccion')
    
    if not nombre or not email or not password:
        return jsonify({"mensaje": "Faltan campos obligatorios"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"mensaje": "El email ya está registrado"}), 400

    # Aquí se debería cifrar la contraseña
    hashed_password = User.generate_password_hash(password)

    nuevo_usuario = User(nombre=nombre, email=email, password=hashed_password, direccion=direccion)
    db.session.add(nuevo_usuario)
    db.session.commit()
    
    return jsonify({
        "mensaje": "Usuario creado con bcrypt",
        "id": nuevo_usuario.id,
        "nombre": nuevo_usuario.nombre,
        "email": nuevo_usuario.email,
        "direccion": nuevo_usuario.get_direccion()
    }), 201

def crear_usuario_base(data):
    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')
    direccion = data.get('direccion')

    if not nombre or not email or not password or not direccion:
        return jsonify({"mensaje": "Faltan campos obligatorios"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"mensaje": "El email ya está registrado"}), 400

    nuevo_usuario = User(nombre=nombre, email=email, password=password, direccion=direccion)
    db.session.add(nuevo_usuario)
    db.session.commit()
    
    return jsonify({
        "mensaje": "Usuario creado sin bcrypt",
        "id": nuevo_usuario.id,
        "nombre": nuevo_usuario.nombre,
        "email": nuevo_usuario.email,
        "direccion": nuevo_usuario.get_direccion()
    }), 201

def login_usuario(data):
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"mensaje": "Credenciales inválidas"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({"mensaje": "Inicio de sesión exitoso", "token": access_token}), 200

@jwt_required()
def obtener_usuario():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404
    
    return jsonify({
        "id": user.id,
        "nombre": user.nombre,
        "email": user.email,
        "direccion": user.get_direccion()
    }), 200

@jwt_required()
def eliminar_usuario(user_id):
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({"mensaje": "Usuario eliminado"}), 200
