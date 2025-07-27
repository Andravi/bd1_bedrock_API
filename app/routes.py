from flask import Blueprint, request, jsonify
from app import db


main_bp = Blueprint('main', __name__)

# Universos
# Categorias
# Anotação
# Tabela
# Propriedade
# Menções
# TipoAnotação
# templateAnot
# Coluna
# Linha
# Lugar
# Evento
# Localização
# Duração
# Catego_anotacao
#
@main_bp.route('/universos', methods=['GET'])
def get_users():
    
    return jsonify({
        'universos': "ok"
    }), 200


# @main_bp.route('/users', methods=['GET'])
# def get_users():
#     users = Usuario.query.all()
#     return jsonify({
#         'users': [usuario.to_dict() for usuario in users]
#     }), 200