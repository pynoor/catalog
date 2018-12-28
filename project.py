from flask import Flask
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Item, Category


engine = create_engine('sqlite:///restaurantmenu.db',
connect_args={'check_same_thread': False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/home/')
def home():
    return "Welcome"

if __name__ == '__main__':
    app.secret_key = '17_no_0)(31'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
