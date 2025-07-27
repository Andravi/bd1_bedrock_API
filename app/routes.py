from flask import Blueprint, request, jsonify
from app.models import *
from app import db
from datetime import datetime, timezone

main_bp = Blueprint('main', __name__, url_prefix='/api')

# Universos
@main_bp.route('/universos', methods=['GET', 'POST'])
def universos():
    if request.method == 'GET':
        universos = Universo.query.all()
        return jsonify([{
            'nome': u.nome,
            'resumo': u.resumo,
            'ultima_edicao': u.ultima_edicao.isoformat() if u.ultima_edicao else None,
            'data_criacao': u.data_criacao.isoformat() if u.data_criacao else None
        } for u in universos])
    
    elif request.method == 'POST':
        data = request.get_json()
        novo_universo = Universo(
            nome=data['nome'],
            resumo=data.get('resumo'),
            ultima_edicao=data.get('ultima_edicao'),
            data_criacao=data.get('data_criacao')
        )
        db.session.add(novo_universo)
        db.session.commit()
        return jsonify({'message': 'Universo criado com sucesso'}), 201

@main_bp.route('/universos/<string:nome>', methods=['GET', 'PUT', 'DELETE'])
def universo(nome):
    universo = Universo.query.get_or_404(nome)
    
    if request.method == 'GET':
        return jsonify({
            'nome': universo.nome,
            'resumo': universo.resumo,
            'ultima_edicao': universo.ultima_edicao.isoformat() if universo.ultima_edicao else None,
            'data_criacao': universo.data_criacao.isoformat() if universo.data_criacao else None
        })
    
    elif request.method == 'PUT':
        data = request.get_json()
        universo.resumo = data.get('resumo', universo.resumo)
        universo.ultima_edicao = datetime.now(timezone.utc)
        db.session.commit()
        return jsonify({'message': 'Universo atualizado com sucesso'})
    
    elif request.method == 'DELETE':
        db.session.delete(universo)
        db.session.commit()
        return jsonify({'message': 'Universo removido com sucesso'})

@main_bp.route('/universos/pers_count/<string:nome>', methods=['GET'])
def get_personagens_count(nome):
    return jsonify({'total_personagens': Universo.contar_personagens(nome)})

# Categorias
@main_bp.route('/categorias', methods=['GET', 'POST'])
def categorias():
    if request.method == 'GET':
        categorias = Categoria.query.all()
        return jsonify([{
            'nome': c.nome,
            'descricao': c.descricao
        } for c in categorias])
    
    elif request.method == 'POST':
        data = request.get_json()
        nova_categoria = Categoria(
            nome=data['nome'],
            descricao=data.get('descricao')
        )
        db.session.add(nova_categoria)
        db.session.commit()
        return jsonify({'message': 'Categoria criada com sucesso'}), 201

@main_bp.route('/categorias/<string:nome>', methods=['GET', 'PUT', 'DELETE'])
def categoria(nome):
    categoria = Categoria.query.get_or_404(nome)
    
    if request.method == 'GET':
        return jsonify({
            'nome': categoria.nome,
            'descricao': categoria.descricao
        })
    
    elif request.method == 'PUT':
        data = request.get_json()
        categoria.descricao = data.get('descricao', categoria.descricao)
        db.session.commit()
        return jsonify({'message': 'Categoria atualizada com sucesso'})
    
    elif request.method == 'DELETE':
        db.session.delete(categoria)
        db.session.commit()
        return jsonify({'message': 'Categoria removida com sucesso'})
# Anotação
@main_bp.route('/anotacoes', methods=['GET', 'POST'])
def anotacoes():
    if request.method == 'GET':
        anotacoes = Anotacao.query.all()
        return jsonify([{
            'titulo': a.titulo,
            'descricao': a.descricao,
            'data_criacao': a.data_criacao.isoformat() if a.data_criacao else None,
            'ultima_edicao': a.ultima_edicao.isoformat() if a.ultima_edicao else None,
            'nuniverso': a.nuniverso,
            'tipoAnota': a.tipo_anota,
            'ntemplate_anot': a.ntemplate_anot
        } for a in anotacoes])
    
    elif request.method == 'POST':
        data = request.get_json()
        print(data.get('tipoAnota'))
        nova_anotacao = Anotacao(
            titulo=data['titulo'],
            descricao=data.get('descricao'),
            data_criacao=data.get('data_criacao'),
            ultima_edicao=data.get('ultima_edicao'),
            nuniverso=data.get('nuniverso'),
            tipo_anota=data.get('tipoAnota'),
            ntemplate_anot=data.get('ntemplate_anot')
        )
        db.session.add(nova_anotacao)
        db.session.commit()
        return jsonify({'message': 'Anotação criada com sucesso'}), 201

@main_bp.route('/anotacoes/<string:titulo>', methods=['GET', 'PUT', 'DELETE'])
def anotacao(titulo):
    anotacao = Anotacao.query.get_or_404(titulo)
    
    if request.method == 'GET':
        return jsonify({
            'titulo': anotacao.titulo,
            'descricao': anotacao.descricao,
            'data_criacao': anotacao.data_criacao.isoformat() if anotacao.data_criacao else None,
            'ultima_edicao': anotacao.ultima_edicao.isoformat() if anotacao.ultima_edicao else None,
            'nuniverso': anotacao.nuniverso,
            'tipoAnota': anotacao.tipo_anota,
            'ntemplate_anot': anotacao.ntemplate_anot
        })
    
    elif request.method == 'PUT':
        data = request.get_json()
        anotacao.descricao = data.get('descricao', anotacao.descricao)
        anotacao.ultima_edicao = datetime.now(timezone.utc)
        anotacao.nuniverso = data.get('nuniverso', anotacao.nuniverso)
        anotacao.tipo_anota = data.get('tipoAnota', anotacao.tipo_anota)
        anotacao.ntemplate_anot = data.get('ntemplate_anot', anotacao.ntemplate_anot)
        db.session.commit()
        return jsonify({'message': 'Anotação atualizada com sucesso'})
    
    elif request.method == 'DELETE':
        db.session.delete(anotacao)
        db.session.commit()
        return jsonify({'message': 'Anotação removida com sucesso'})
# Tabela
@main_bp.route('/tabelas', methods=['GET', 'POST'])
def tabelas():
    if request.method == 'GET':
        tabelas = Tabela.query.all()
        return jsonify([{
            'titulo': t.titulo,
            'titu_anotacao': t.titu_anotacao
        } for t in tabelas])
    
    elif request.method == 'POST':
        data = request.get_json()
        nova_tabela = Tabela(
            titulo=data['titulo'],
            titu_anotacao=data['titu_anotacao']
        )
        db.session.add(nova_tabela)
        db.session.commit()
        return jsonify({'message': 'Tabela criada com sucesso'}), 201

@main_bp.route('/tabelas/<string:titulo>', methods=['GET', 'PUT', 'DELETE'])
def tabela(titulo):
    tabela = Tabela.query.get_or_404(titulo)
    
    if request.method == 'GET':
        return jsonify({
            'titulo': tabela.titulo,
            'titu_anotacao': tabela.titu_anotacao
        })
    
    elif request.method == 'PUT':
        data = request.get_json()
        tabela.titu_anotacao = data.get('titu_anotacao', tabela.titu_anotacao)
        db.session.commit()
        return jsonify({'message': 'Tabela atualizada com sucesso'})
    
    elif request.method == 'DELETE':
        db.session.delete(tabela)
        db.session.commit()
        return jsonify({'message': 'Tabela removida com sucesso'})
# Propriedade
@main_bp.route('/propriedades', methods=['GET', 'POST'])
def propriedades():
    if request.method == 'GET':
        propriedades = Propriedade.query.all()
        return jsonify([{
            'nome': p.nome,
            'chave_valor': p.chave_valor,
            'formato': p.formato,
            'tipo': p.tipo,
            'valor': p.valor,
            'valor_bruto': p.valor_bruto,
            'nanotacao': p.nanotacao
        } for p in propriedades])
    
    elif request.method == 'POST':
        data = request.get_json()
        nova_propriedade = Propriedade(
            nome=data['nome'],
            chave_valor=data.get('chave_valor'),
            formato=data.get('formato'),
            tipo=data.get('tipo'),
            valor=data.get('valor'),
            valor_bruto=data.get('valor_bruto'),
            nanotacao=data.get('nanotacao')
        )
        db.session.add(nova_propriedade)
        db.session.commit()
        return jsonify({'message': 'Propriedade criada com sucesso'}), 201

@main_bp.route('/propriedades/<string:nome>', methods=['GET', 'PUT', 'DELETE'])
def propriedade(nome):
    propriedade = Propriedade.query.get_or_404(nome)
    
    if request.method == 'GET':
        return jsonify({
            'nome': propriedade.nome,
            'chave_valor': propriedade.chave_valor,
            'formato': propriedade.formato,
            'tipo': propriedade.tipo,
            'valor': propriedade.valor,
            'valor_bruto': propriedade.valor_bruto,
            'nanotacao': propriedade.nanotacao
        })
    
    elif request.method == 'PUT':
        data = request.get_json()
        propriedade.chave_valor = data.get('chave_valor', propriedade.chave_valor)
        propriedade.formato = data.get('formato', propriedade.formato)
        propriedade.tipo = data.get('tipo', propriedade.tipo)
        propriedade.valor = data.get('valor', propriedade.valor)
        propriedade.valor_bruto = data.get('valor_bruto', propriedade.valor_bruto)
        propriedade.nanotacao = data.get('nanotacao', propriedade.nanotacao)
        db.session.commit()
        return jsonify({'message': 'Propriedade atualizada com sucesso'})
    
    elif request.method == 'DELETE':
        db.session.delete(propriedade)
        db.session.commit()
        return jsonify({'message': 'Propriedade removida com sucesso'})
# Menções
@main_bp.route('/mencoes', methods=['GET', 'POST'])
def mencoes():
    if request.method == 'GET':
        mencoes = Mencao.query.all()
        return jsonify([{
            'anot_mencionada': m.anot_mencionada,
            'anot_mencionando': m.anot_mencionando,
            'palavra_chave': m.palavra_chave,
            'posicao_no_texto': m.posicao_no_texto
        } for m in mencoes])
    
    elif request.method == 'POST':
        data = request.get_json()
        nova_mencao = Mencao(
            anot_mencionada=data['anot_mencionada'],
            anot_mencionando=data['anot_mencionando'],
            palavra_chave=data.get('palavra_chave'),
            posicao_no_texto=data.get('posicao_no_texto')
        )
        db.session.add(nova_mencao)
        db.session.commit()
        return jsonify({'message': 'Menção criada com sucesso'}), 201

@main_bp.route('/mencoes/<string:anot_mencionada>/<string:anot_mencionando>', methods=['GET', 'PUT', 'DELETE'])
def mencao(anot_mencionada, anot_mencionando):
    mencao = Mencao.query.get_or_404((anot_mencionada, anot_mencionando))
    
    if request.method == 'GET':
        return jsonify({
            'anot_mencionada': mencao.anot_mencionada,
            'anot_mencionando': mencao.anot_mencionando,
            'palavra_chave': mencao.palavra_chave,
            'posicao_no_texto': mencao.posicao_no_texto
        })
    
    elif request.method == 'PUT':
        data = request.get_json()
        mencao.palavra_chave = data.get('palavra_chave', mencao.palavra_chave)
        mencao.posicao_no_texto = data.get('posicao_no_texto', mencao.posicao_no_texto)
        db.session.commit()
        return jsonify({'message': 'Menção atualizada com sucesso'})
    
    elif request.method == 'DELETE':
        db.session.delete(mencao)
        db.session.commit()
        return jsonify({'message': 'Menção removida com sucesso'})
# TipoAnotação
@main_bp.route('/tipos_anotacao', methods=['GET', 'POST'])
def tipos_anotacao():
    if request.method == 'GET':
        tipos = TipoAnotacao.query.all()
        return jsonify([{
            'nome': t.nome,
            'descricao': t.descricao,
            'tipo_pai': t.tipo_pai_nome
        } for t in tipos])
    
    elif request.method == 'POST':
        data = request.get_json()
        novo_tipo = TipoAnotacao(
            nome=data['nome'],
            descricao=data.get('descricao'),
            tipo_pai_nome=data.get('tipo_pai')
        )
        db.session.add(novo_tipo)
        db.session.commit()
        return jsonify({'message': 'Tipo de anotação criado com sucesso'}), 201

@main_bp.route('/tipos_anotacao/<string:nome>', methods=['GET', 'PUT', 'DELETE'])
def tipo_anotacao(nome):
    tipo = TipoAnotacao.query.get_or_404(nome)
    
    if request.method == 'GET':
        return jsonify({
            'nome': tipo.nome,
            'descricao': tipo.descricao,
            'tipo_pai': tipo.tipo_pai_nome,
            'subtipos': [st.nome for st in tipo.tipo_pai]
        })
    
    elif request.method == 'PUT':
        data = request.get_json()
        tipo.descricao = data.get('descricao', tipo.descricao)
        tipo.tipo_pai_nome = data.get('tipo_pai', tipo.tipo_pai_nome)
        db.session.commit()
        return jsonify({'message': 'Tipo de anotação atualizado com sucesso'})
    
    elif request.method == 'DELETE':
        db.session.delete(tipo)
        db.session.commit()
        return jsonify({'message': 'Tipo de anotação removido com sucesso'})
# templateAnot
@main_bp.route('/templates_anot', methods=['GET', 'POST'])
def templates_anot():
    if request.method == 'GET':
        templates = TemplateAnot.query.all()
        return jsonify([{
            'nome': t.nome,
            'descricao': t.descricao,
            'tipo_padrao': t.tipo_padrao_nome
        } for t in templates])
    
    elif request.method == 'POST':
        data = request.get_json()
        novo_template = TemplateAnot(
            nome=data['nome'],
            descricao=data.get('descricao'),
            tipo_padrao_nome=data.get('tipo_padrao')
        )
        db.session.add(novo_template)
        db.session.commit()
        return jsonify({'message': 'Template criado com sucesso'}), 201

@main_bp.route('/templates_anot/<string:nome>', methods=['GET', 'PUT', 'DELETE'])
def template_anot(nome):
    template = TemplateAnot.query.get_or_404(nome)
    
    if request.method == 'GET':
        return jsonify({
            'nome': template.nome,
            'descricao': template.descricao,
            'tipo_padrao': template.tipo_padrao_nome
        })
    
    elif request.method == 'PUT':
        data = request.get_json()
        template.descricao = data.get('descricao', template.descricao)
        template.tipo_padrao_nome = data.get('tipo_padrao', template.tipo_padrao_nome)
        db.session.commit()
        return jsonify({'message': 'Template atualizado com sucesso'})
    
    elif request.method == 'DELETE':
        db.session.delete(template)
        db.session.commit()
        return jsonify({'message': 'Template removido com sucesso'})
# Coluna
@main_bp.route('/colunas', methods=['POST'])
def criar_coluna():
    data = request.get_json()
    nova_coluna = Coluna(
        titulo=data['titulo'],
        ttabela=data['ttabela']
    )
    db.session.add(nova_coluna)
    db.session.commit()
    return jsonify({'message': 'Coluna criada com sucesso'}), 201

@main_bp.route('/tabelas/<string:titulo_tabela>/colunas', methods=['GET'])
def listar_colunas(titulo_tabela):
    colunas = Coluna.query.filter_by(ttabela=titulo_tabela).all()
    return jsonify([{
        'titulo': c.titulo,
        'ttabela': c.ttabela
    } for c in colunas])

@main_bp.route('/tabelas/<string:titulo_tabela>/colunas/<string:titulo_coluna>', methods=['GET', 'DELETE'])
def gerenciar_coluna(titulo_tabela, titulo_coluna):
    coluna = Coluna.query.get_or_404((titulo_coluna, titulo_tabela))
    
    if request.method == 'GET':
        return jsonify({
            'titulo': coluna.titulo,
            'ttabela': coluna.ttabela
        })
    
    elif request.method == 'DELETE':
        db.session.delete(coluna)
        db.session.commit()
        return jsonify({'message': 'Coluna removida com sucesso'})
# Linha
@main_bp.route('/tabelas/<string:titulo_tabela>/linhas', methods=['GET', 'POST'])
def linhas(titulo_tabela):
    if request.method == 'GET':
        linhas = Linha.query.filter_by(TTabela=titulo_tabela).all()
        return jsonify([{
            'id': l.id,
            'celulas': l.celulas,
            'ttabela': l.TTabela
        } for l in linhas])
    
    elif request.method == 'POST':
        data = request.get_json()
        nova_linha = Linha(
            TTabela=titulo_tabela,
            celulas=data.get('celulas', {})
        )
        db.session.add(nova_linha)
        db.session.commit()
        return jsonify({'message': 'Linha criada com sucesso'}), 201

@main_bp.route('/tabelas/<string:titulo_tabela>/linhas/<int:id_linha>', methods=['GET', 'PUT', 'DELETE'])
def linha(titulo_tabela, id_linha):
    linha = Linha.query.filter_by(id=id_linha, TTabela=titulo_tabela).first_or_404()
    
    if request.method == 'GET':
        return jsonify({
            'id': linha.id,
            'celulas': linha.celulas,
            'ttabela': linha.TTabela
        })
    
    elif request.method == 'PUT':
        data = request.get_json()
        linha.celulas = data.get('celulas', linha.celulas)
        db.session.commit()
        return jsonify({'message': 'Linha atualizada com sucesso'})
    
    elif request.method == 'DELETE':
        db.session.delete(linha)
        db.session.commit()
        return jsonify({'message': 'Linha removida com sucesso'})
# Lugar
@main_bp.route('/lugares', methods=['GET', 'POST'])
def lugares():
    if request.method == 'GET':
        lugares = Lugar.query.all()
        return jsonify([{
            'nome': l.nome,
            'tamanho': l.tamanho,
            'descricao': l.tipo_anotacao.descricao if l.tipo_anotacao else None
        } for l in lugares])
    
    elif request.method == 'POST':
        data = request.get_json()
        # Primeiro cria o tipo de anotação
        tipo = TipoAnotacao(
            nome=data['nome'],
            descricao=data.get('descricao')
        )
        db.session.add(tipo)
        
        # Depois cria o lugar
        novo_lugar = Lugar(
            nome=data['nome'],
            tamanho=data.get('tamanho')
        )
        db.session.add(novo_lugar)
        db.session.commit()
        return jsonify({'message': 'Lugar criado com sucesso'}), 201

@main_bp.route('/lugares/<string:nome>', methods=['GET', 'PUT', 'DELETE'])
def lugar(nome):
    lugar = Lugar.query.get_or_404(nome)
    
    if request.method == 'GET':
        return jsonify({
            'nome': lugar.nome,
            'tamanho': lugar.tamanho,
            'descricao': lugar.tipo_anotacao.descricao if lugar.tipo_anotacao else None,
            'localizacoes': [loc.nprop for loc in lugar.localizacoes]
        })
    
    elif request.method == 'PUT':
        data = request.get_json()
        lugar.tamanho = data.get('tamanho', lugar.tamanho)
        if lugar.tipo_anotacao and 'descricao' in data:
            lugar.tipo_anotacao.descricao = data['descricao']
        db.session.commit()
        return jsonify({'message': 'Lugar atualizado com sucesso'})
    
    elif request.method == 'DELETE':
        # Remove primeiro o lugar, depois o tipo de anotação associado
        tipo = TipoAnotacao.query.get(lugar.nome)
        db.session.delete(lugar)
        if tipo:
            db.session.delete(tipo)
        db.session.commit()
        return jsonify({'message': 'Lugar removido com sucesso'})
# Evento
@main_bp.route('/eventos', methods=['GET', 'POST'])
def eventos():
    if request.method == 'GET':
        eventos = Evento.query.all()
        return jsonify([{
            'nome': e.nome,
            'razao_inicio': e.razao_inicio,
            'descricao': e.tipo_anotacao.descricao if e.tipo_anotacao else None
        } for e in eventos])
    
    elif request.method == 'POST':
        data = request.get_json()
        # Primeiro cria o tipo de anotação
        tipo = TipoAnotacao(
            nome=data['nome'],
            descricao=data.get('descricao')
        )
        db.session.add(tipo)
        
        # Depois cria o evento
        novo_evento = Evento(
            nome=data['nome'],
            razao_inicio=data.get('razao_inicio')
        )
        db.session.add(novo_evento)
        db.session.commit()
        return jsonify({'message': 'Evento criado com sucesso'}), 201

@main_bp.route('/eventos/<string:nome>', methods=['GET', 'PUT', 'DELETE'])
def evento(nome):
    evento = Evento.query.get_or_404(nome)
    
    if request.method == 'GET':
        return jsonify({
            'nome': evento.nome,
            'razao_inicio': evento.razao_inicio,
            'descricao': evento.tipo_anotacao.descricao if evento.tipo_anotacao else None,
            'duracoes': [dur.nprop for dur in evento.duracoes]
        })
    
    elif request.method == 'PUT':
        data = request.get_json()
        evento.razao_inicio = data.get('razao_inicio', evento.razao_inicio)
        if evento.tipo_anotacao and 'descricao' in data:
            evento.tipo_anotacao.descricao = data['descricao']
        db.session.commit()
        return jsonify({'message': 'Evento atualizado com sucesso'})
    
    elif request.method == 'DELETE':
        # Remove primeiro o evento, depois o tipo de anotação associado
        tipo = TipoAnotacao.query.get(evento.nome)
        db.session.delete(evento)
        if tipo:
            db.session.delete(tipo)
        db.session.commit()
        return jsonify({'message': 'Evento removido com sucesso'})
# Localização
@main_bp.route('/localizacoes', methods=['POST'])
def criar_localizacao():
    data = request.get_json()
    nova_localizacao = Localizacao(
        nprop=data['nprop'],
        pontos_referencia=data.get('pontos_referencia'),
        nlugar=data.get('nlugar')
    )
    db.session.add(nova_localizacao)
    db.session.commit()
    return jsonify({'message': 'Localização criada com sucesso'}), 201

@main_bp.route('/localizacoes/<string:nprop>', methods=['GET', 'PUT', 'DELETE'])
def localizacao(nprop):
    localizacao = Localizacao.query.get_or_404(nprop)
    
    if request.method == 'GET':
        return jsonify({
            'nprop': localizacao.nprop,
            'pontos_referencia': localizacao.pontos_referencia,
            'nlugar': localizacao.nlugar
        })
    
    elif request.method == 'PUT':
        data = request.get_json()
        localizacao.pontos_referencia = data.get('pontos_referencia', localizacao.pontos_referencia)
        localizacao.nlugar = data.get('nlugar', localizacao.nlugar)
        db.session.commit()
        return jsonify({'message': 'Localização atualizada com sucesso'})
    
    elif request.method == 'DELETE':
        db.session.delete(localizacao)
        db.session.commit()
        return jsonify({'message': 'Localização removida com sucesso'})
# Duração
@main_bp.route('/duracoes', methods=['POST'])
def criar_duracao():
    data = request.get_json()
    nova_duracao = Duracao(
        nprop=data['nprop'],
        desc_periodo=data.get('desc_periodo'),
        nevento=data.get('nevento')
    )
    db.session.add(nova_duracao)
    db.session.commit()
    return jsonify({'message': 'Duração criada com sucesso'}), 201

@main_bp.route('/duracoes/<string:nprop>', methods=['GET', 'PUT', 'DELETE'])
def duracao(nprop):
    duracao = Duracao.query.get_or_404(nprop)
    
    if request.method == 'GET':
        return jsonify({
            'nprop': duracao.nprop,
            'desc_periodo': duracao.desc_periodo,
            'nevento': duracao.nevento
        })
    
    elif request.method == 'PUT':
        data = request.get_json()
        duracao.desc_periodo = data.get('desc_periodo', duracao.desc_periodo)
        duracao.nevento = data.get('nevento', duracao.nevento)
        db.session.commit()
        return jsonify({'message': 'Duração atualizada com sucesso'})
    
    elif request.method == 'DELETE':
        db.session.delete(duracao)
        db.session.commit()
        return jsonify({'message': 'Duração removida com sucesso'})
# Catego_anotacao
@main_bp.route('/anotacoes/<string:titulo_anotacao>/categorias', methods=['GET', 'POST'])
def categorias_anotacao(titulo_anotacao):
    if request.method == 'GET':
        categorias = db.session.query(Categoria).join(
            CategoAnotacao,
            Categoria.nome == CategoAnotacao.ncategoria
        ).filter(
            CategoAnotacao.nanotacao == titulo_anotacao
        ).all()
        
        return jsonify([{
            'nome': c.nome,
            'descricao': c.descricao
        } for c in categorias])
    
    elif request.method == 'POST':
        data = request.get_json()
        relacao = CategoAnotacao(
            ncategoria=data['nome_categoria'],
            nanotacao=titulo_anotacao
        )
        db.session.add(relacao)
        db.session.commit()
        return jsonify({'message': 'Categoria associada à anotação com sucesso'}), 201

@main_bp.route('/anotacoes/<string:titulo_anotacao>/categorias/<string:nome_categoria>', methods=['DELETE'])
def remover_categoria_anotacao(titulo_anotacao, nome_categoria):
    relacao = CategoAnotacao.query.get_or_404((nome_categoria, titulo_anotacao))
    db.session.delete(relacao)
    db.session.commit()
    return jsonify({'message': 'Associação entre categoria e anotação removida com sucesso'})

