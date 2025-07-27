from app import create_app
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'
API_URL = '/static/api_docs.yml'  # Coloque seu arquivo YAML na pasta static

app = create_app()

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "API BedRock"
    }
)

app.register_blueprint(swaggerui_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
