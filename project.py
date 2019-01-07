# next steps: add flashed messages, login
from flask import Flask, render_template, url_for, jsonify, request, redirect
from flask_bootstrap import Bootstrap
app = Flask(__name__)
Bootstrap(app)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item

from flask import session as login_session
import random, string

engine = create_engine('sqlite:///catalog.db',
connect_args={'check_same_thread': False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


@app.route('/')
@app.route('/home/')
def home():
    categories = session.query(Category).all()
    items = session.query(Item).all()
    return render_template('home.html', categories=categories, items=items)

@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase +
    string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)



@app.route('/category/<int:category_id>/')
def showCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return render_template('category.html', category=category, items=items)

@app.route('/category/<int:category_id>/JSON')
def showCategoryJSON(category_id):
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify([item.serialize for item in items])

@app.route('/category/<int:category_id>/item/new/', methods=['GET', 'POST'])
def newItem(category_id):
    if request.method == 'POST':
        newItem = Item(
            name=request.form['name'],
            description=request.form['description'],
            category_id=category_id
        )
        session.add(newItem)
        session.commit()
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template('newitem.html', category_id=category_id)

@app.route('/category/<int:category_id>/item/<int:item_id>/')
def showItem(category_id, item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).filter_by(id=item_id).one()
    return render_template('item.html', category=category, item=item)

@app.route('/category/<int:category_id>/item/<int:item_id>/edit/', methods=['GET', 'POST'])
def editItem(category_id, item_id):
    categories = session.query(Category).all()
    item = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        if request.form['description']:
            item.description = request.form['description']
        item.category_id = int(request.form['category'])
        session.add(item)
        session.commit()
        return redirect(url_for('showItem', category_id=category_id, item_id=item_id))
    else:
        return render_template('edititem.html', item=item, categories=categories)

@app.route('/category/<int:category_id>/item/<int:item_id>/delete/', methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        return redirect(url_for('showItem', category_id=category_id, item_id=item_id))
    else:
        return render_template('deleteitem.html', item=item)


if __name__ == '__main__':
    app.secret_key = '17_no_0)(31'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
