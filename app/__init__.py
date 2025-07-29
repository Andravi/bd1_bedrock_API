from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import text


db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    with app.app_context():
        # Criar tabelas primeiro (se não existirem)
        db.create_all()
        
        # Criar a view apenas se não existir
        criar_view_resumo_universo()
    
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    return app

from app.models import *


def criar_view_resumo_universo():
    try:
        # Verifica se a view já existe
        view_exists = db.session.execute(text("""
            SELECT EXISTS (
                SELECT 1 FROM pg_views 
                WHERE viewname = 'resumo_universo_completo'
            )
        """)).scalar()

        if not view_exists:
            db.session.execute(text("""
            CREATE OR REPLACE VIEW Resumo_Universo_Completo AS
            SELECT 
                u.Nome AS Universo,
                COUNT(DISTINCT a.Titulo) AS Total_Anotacoes,
                COUNT(DISTINCT CASE WHEN a.tipo_anota = 'Personagem' THEN a.Titulo END) AS Personagens,
                COUNT(DISTINCT CASE WHEN ta.tipo_pai_nome = 'Local' THEN a.Titulo END) AS Locais,
                COUNT(DISTINCT CASE WHEN ta.tipo_pai_nome = 'Evento' THEN a.Titulo END) AS Eventos,
                (
                    SELECT STRING_AGG(l.Nome, ', ')
                    FROM Lugar l
                    WHERE l.Nome IN (
                        SELECT a2.Titulo 
                        FROM Anotacao a2 
                        WHERE a2.Nuniverso = u.Nome
                        AND a2.tipo_anota IN (
                            SELECT Nome FROM tipo_anotacao 
                            WHERE tipo_pai_nome = 'Local'
                        )
                    )
                ) AS Lista_Lugares
            FROM 
                Universo u
            LEFT JOIN 
                Anotacao a ON u.Nome = a.Nuniverso
            LEFT JOIN 
                tipo_anotacao ta ON a.tipo_anota = ta.Nome
            GROUP BY 
                u.Nome;
            """))
            db.session.commit()
            print("View criada com sucesso!")
        else:
            print("View já existe - nenhuma ação necessária")
            
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao verificar/criar view: {str(e)}")
