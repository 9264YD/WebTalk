from flask import Flask
from .routes import index,login,register, result, chat, submit_answer, help, meet, group, logout, account, search ,delete_data
from config import Config

from .models import db

config = Config()
secret_key = config.SECRET_KEY
app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  
# database_initialization()
app.add_url_rule('/', view_func=index)
app.add_url_rule('/login', view_func=login, methods=['GET', 'POST'])
app.add_url_rule('/register', view_func=register, methods=['GET', 'POST'])
app.add_url_rule('/result', view_func=result, methods=['POST'])
app.add_url_rule('/chat', view_func=chat)
app.add_url_rule('/submit_answer', view_func=submit_answer, methods=['POST'])
app.add_url_rule('/help', view_func=help)
app.add_url_rule('/meet', view_func=meet, methods=['POST'])
app.add_url_rule('/group', view_func=group)
app.add_url_rule('/logout', view_func=logout)
app.add_url_rule('/account', view_func=account, methods=['GET', 'POST'])
app.add_url_rule('/search', view_func=search, methods=['GET'])
app.add_url_rule('/delete', view_func=delete_data, methods=['POST'])

if __name__ == '__main__':
    app.run()