# coding = utf-8
from app import create_app
app = create_app()



if __name__ == '__main__':
    app.run(host=app.config['RUN_HOST'], port=app.config['RUN_PORT'], debug=app.config['DEBUG'])
