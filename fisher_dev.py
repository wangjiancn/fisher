# coding = utf-8
from app import create_app
from flask_script import Manager
# from livereload import Server


app = create_app()

# app.debug = True
# server = Server(app.wsgi_app)
# server.serve(port=5000)

manager = Manager(app)

@manager.command
def dev():
    from livereload import Server
    live_server = Server(app.wsgi_app)
    live_server.watch('**/*.*')
    live_server.serve(open_url=True)



if __name__ == '__main__':
    manager.run()
