from flask import Flask
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Item, Category


engine = create_engine('sqlite:///catalog.db',
connect_args={'check_same_thread': False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/home/')
def home():
    return "Welcome"

@app.route('/category/<int:category_id>/')
def showCategory(category_id):
    return "Welcome"

@app.route('/category/<int:category_id>/item/new/', methods=['GET', 'POST'])
def newItem(category_id):
    return "This page is for creating a new item"

@app.route('/category/<int:category_id>/item/<int:item_id>/')
def showItem(category_id, item_id):
    return "this is the item view"


@app.route('/category/<int:category_id>/item/<int:item_id>/edit/', methods=['GET', 'POST'])
def editItem(item_id):
    return "This page is for editing an item"

@app.route('/category/<int:category_id>/item/<int:item_id>/delete/', methods=['GET', 'POST'])
def deleteItem(item_id):
    return "This page is for deleting an item"


if __name__ == '__main__':
    app.secret_key = '17_no_0)(31'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
