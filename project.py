# next steps: add flashed messages, login
from flask import Flask, render_template, url_for, jsonify, request, redirect, flash
from flask_bootstrap import Bootstrap
app = Flask(__name__)
Bootstrap(app)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item

from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog Application"



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

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print ("done!")
    return output

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
        flash("New item added!")
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
        flash("Edited %s" % item.name)
        return redirect(url_for('showItem', category_id=category_id, item_id=item_id))
    else:
        return render_template('edititem.html', item=item, categories=categories)

@app.route('/category/<int:category_id>/item/<int:item_id>/delete/', methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash("Item deleted.")
        return redirect(url_for('showItem', category_id=category_id, item_id=item_id))
    else:
        return render_template('deleteitem.html', item=item)


if __name__ == '__main__':
    app.secret_key = '17_no_0)(31'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
