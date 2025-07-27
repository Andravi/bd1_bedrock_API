from sqlalchemy.orm import relationship

from app import db

class Universo(db.Model):
    __tablename__ = 'universo'
    
    nome = db.Column(db.String(100), primary_key=True)
    resumo = db.Column(db.Text)
    ultima_edicao = db.Column(db.Date)
    data_criacao = db.Column(db.Date)
    
    anotacoes = relationship('Anotacao', back_populates='universo')

class Categoria(db.Model):
    __tablename__ = 'categoria'
    
    nome = db.Column(db.String(100), primary_key=True)
    descricao = db.Column(db.Text)
    
    anotacoes = relationship('Anotacao', secondary='catego_anotacao', back_populates='categorias')

class TipoAnotacao(db.Model):
    __tablename__ = 'tipo_anotacao'
    
    nome = db.Column(db.String(100), primary_key=True)
    descricao = db.Column(db.Text)
    
    # Auto-relacionamento para tipo pai
    tipo_pai_nome = db.Column(db.String(100), db.ForeignKey('tipo_anotacao.nome'))
    tipo_pai = relationship('TipoAnotacao', remote_side=[nome])
    
    # Relacionamentos com subtipos específicos
    lugar = relationship('Lugar', uselist=False, back_populates='tipo_anotacao')
    evento = relationship('Evento', uselist=False, back_populates='tipo_anotacao')
    
    anotacoes = relationship('Anotacao', back_populates='tipo_anotacao')
    templates = relationship('TemplateAnot', back_populates='tipo_padrao')

class TemplateAnot(db.Model):
    __tablename__ = 'template_anot'
    
    nome = db.Column(db.String(100), primary_key=True)
    descricao = db.Column(db.Text)
    
    tipo_padrao_nome = db.Column(db.String(100), db.ForeignKey('tipo_anotacao.nome'))
    tipo_padrao = relationship('TipoAnotacao', back_populates='templates')
    
    anotacoes = relationship('Anotacao', back_populates='template')

class Anotacao(db.Model):
    __tablename__ = 'anotacao'
    
    titulo = db.Column(db.String(100), primary_key=True)
    descricao = db.Column(db.Text)
    data_criacao = db.Column(db.Date)
    ultima_edicao = db.Column(db.Date)
    
    nuniverso = db.Column(db.String(100), db.ForeignKey('universo.nome'))
    universo = relationship('Universo', back_populates='anotacoes')
    
    tipo_anota = db.Column(db.String(100), db.ForeignKey('tipo_anotacao.nome'))
    tipo_anotacao = relationship('TipoAnotacao', back_populates='anotacoes')
    
    ntemplate_anot = db.Column(db.String(100), db.ForeignKey('template_anot.nome'))
    template = relationship('TemplateAnot', back_populates='anotacoes')
    
    categorias = relationship('Categoria', secondary='catego_anotacao', back_populates='anotacoes')
    tabelas = relationship('Tabela', back_populates='anotacao')
    propriedades = relationship('Propriedade', back_populates='anotacao')
    
    # Relacionamentos para menções
    mencionadas = relationship('Mencao', 
                              foreign_keys='Mencao.anot_mencionando',
                              back_populates='mencionando')
    mencionando = relationship('Mencao', 
                              foreign_keys='Mencao.anot_mencionada',
                              back_populates='mencionada')

class CategoAnotacao(db.Model):
    __tablename__ = 'catego_anotacao'
    
    ncategoria = db.Column(db.String(100), db.ForeignKey('categoria.nome'), primary_key=True)
    nanotacao = db.Column(db.String(100), db.ForeignKey('anotacao.titulo'), primary_key=True)

class Tabela(db.Model):
    __tablename__ = 'tabela'
    
    titulo = db.Column(db.String(100), primary_key=True)
    titu_anotacao = db.Column(db.String(100), db.ForeignKey('anotacao.titulo'))
    
    anotacao = relationship('Anotacao', back_populates='tabelas')
    colunas = relationship('Coluna', back_populates='tabela')
    linhas = relationship('Linha', back_populates='tabela')

class Coluna(db.Model):
    __tablename__ = 'coluna'
    
    titulo = db.Column(db.String(100), primary_key=True)
    ttabela = db.Column(db.String(100), db.ForeignKey('tabela.titulo'), primary_key=True)
    
    tabela = relationship('Tabela', back_populates='colunas')

class Linha(db.Model):
    __tablename__ = 'linha'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ttabela = db.Column(db.String(100), db.ForeignKey('tabela.titulo'), primary_key=True)
    celulas = db.Column(db.JSON)
    
    tabela = relationship('Tabela', back_populates='linhas')

class Lugar(db.Model):
    __tablename__ = 'lugar'
    
    nome = db.Column(db.String(100), db.ForeignKey('tipo_anotacao.nome'), primary_key=True)
    tamanho = db.Column(db.String(50))
    
    tipo_anotacao = relationship('TipoAnotacao', back_populates='lugar')
    localizacoes = relationship('Localizacao', back_populates='lugar')

class Evento(db.Model):
    __tablename__ = 'evento'
    
    nome = db.Column(db.String(100), db.ForeignKey('tipo_anotacao.nome'), primary_key=True)
    razao_inicio = db.Column(db.Text)
    
    tipo_anotacao = relationship('TipoAnotacao', back_populates='evento')
    duracoes = relationship('Duracao', back_populates='evento')

class Propriedade(db.Model):
    __tablename__ = 'propriedade'
    
    nome = db.Column(db.String(100), primary_key=True)
    chave_valor = db.Column(db.JSON)
    formato = db.Column(db.String(50))
    tipo = db.Column(db.String(50))
    valor = db.Column(db.Text)
    valor_bruto = db.Column(db.Text)
    
    nanotacao = db.Column(db.String(100), db.ForeignKey('anotacao.titulo'))
    anotacao = relationship('Anotacao', back_populates='propriedades')
    
    # Relacionamentos com subtipos
    localizacao = relationship('Localizacao', uselist=False, back_populates='propriedade')
    duracao = relationship('Duracao', uselist=False, back_populates='propriedade')

class Localizacao(db.Model):
    __tablename__ = 'localizacao'
    
    nprop = db.Column(db.String(100), db.ForeignKey('propriedade.nome'), primary_key=True)
    pontos_referencia = db.Column(db.Text)
    
    nlugar = db.Column(db.String(100), db.ForeignKey('lugar.nome'))
    lugar = relationship('Lugar', back_populates='localizacoes')
    
    propriedade = relationship('Propriedade', back_populates='localizacao')

class Duracao(db.Model):
    __tablename__ = 'duracao'
    
    nprop = db.Column(db.String(100), db.ForeignKey('propriedade.nome'), primary_key=True)
    desc_periodo = db.Column(db.Text)
    
    nevento = db.Column(db.String(100), db.ForeignKey('evento.nome'))
    evento = relationship('Evento', back_populates='duracoes')
    
    propriedade = relationship('Propriedade', back_populates='duracao')

class Mencao(db.Model):
    __tablename__ = 'mencoes'
    
    anot_mencionada = db.Column(db.String(100), db.ForeignKey('anotacao.titulo'), primary_key=True)
    anot_mencionando = db.Column(db.String(100), db.ForeignKey('anotacao.titulo'), primary_key=True)
    palavra_chave = db.Column(db.String(100))
    posicao_no_texto = db.Column(db.Integer)
    
    mencionada = relationship('Anotacao', foreign_keys=[anot_mencionada], back_populates='mencionando')
    mencionando = relationship('Anotacao', foreign_keys=[anot_mencionando], back_populates='mencionadas')