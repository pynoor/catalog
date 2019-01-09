# importing all necessary modules for this project
from flask import Flask, render_template
from flask import url_for, jsonify, request, redirect, flash
from flask_bootstrap import Bootstrap

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item, User

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

# initiating the application by creating a flask app object
app = Flask(__name__)
Bootstrap(app)

# loading the client id from the client_secrets JSON file downloaded
# from the google console
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog Application"


# connecting to the database
engine = create_engine('sqlite:///catalogwithusers.db',
                       connect_args={'check_same_thread': False})

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# the following are the routes of the project, i.e., they define
# what happens when a specific url is requested from the server

# home page


@app.route('/')
@app.route('/home/')
def home():
    categories = session.query(Category).all()
    items = session.query(Item).all()
    return render_template('home.html', categories=categories, items=items)

# log in page


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase +
                    string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

# the next three helper functions will make it easier
# for us to retrieve information about the user that
# is logged in (or not) during a login session

# this function will create a new user in the database
# user table with information collected from their
# google log in


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

# returns a user object with attributes id, name, email and picture


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

# returns a user id if a user is logged in or None if not


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# this function is called upon clicking the login button on the login page
# upon log in it will connect to google to request an access token that is
# then stored (in the login_session object)
# if the login is successful it will redirect to the homepage


@app.route('/gconnect', methods=['POST', 'GET'])
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
    result = json.loads(h.request(url, 'GET')[1].decode('UTF-8'))
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
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
                                 'Current user is already connected.'), 200)
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

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += """ ' style = 'width: 300px; height: 300px;border-radius: 150px;
              -webkit-border-radius: 150px;-moz-border-radius: 150px;'> """
    flash("you are now logged in as %s" % login_session['username'])
    return output

# this function is called by clicking on the log out button
# it will remove all information about the current user stored in the
# login_session object


@app.route('/gdisconnect', methods=['POST', 'GET'])
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps(
                                 'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token={}'.format(
           access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
                   json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# category page
# depending on whether a user is logged in or not this will return a page
# showing all items for a specific category with or without the option
# to create a new one


@app.route('/category/<int:category_id>/')
def showCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    if 'username' not in login_session:
        return render_template('publiccategory.html',
                               category=category, items=items)
    return render_template('category.html', category=category, items=items)


@app.route('/category/<int:category_id>/JSON')
def showCategoryJSON(category_id):
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(Items=[item.serialize for item in items])

# new item page
# if no user is logged in, the client will be redirected to the login page
# else, a form is displayed to create a new item


@app.route('/category/<int:category_id>/item/new/', methods=['GET', 'POST'])
def newItem(category_id):
    if 'username' not in login_session:
        flash('You are not allowed to do that, sorry! Log in first.')
        return redirect('/login')

    if request.method == 'POST':
        newItem = Item(
            name=request.form['name'],
            description=request.form['description'],
            category_id=category_id,
            user_id=login_session['user_id']
        )
        session.add(newItem)
        session.commit()
        flash("New item added!")
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template('newitem.html', category_id=category_id)

# item page
# depending on whether the creator of the item is logged in or not this
# function will return a page with the information about the item and
# the option to modify that item (or not)


@app.route('/category/<int:category_id>/item/<int:item_id>/')
def showItem(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    creator = getUserInfo(item.user_id)
    category = session.query(Category).filter_by(id=category_id).one()
    logged_in = ('username' in login_session)
    if not logged_in or creator.id != login_session['user_id']:
        return render_template('publicitem.html', category=category,
                               item=item, loggedIn=logged_in)
    else:
        return render_template('item.html', category=category, item=item)


@app.route('/category/<int:category_id>/item/<int:item_id>/JSON')
def showItemJSON(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(Item=item.serialize)

# item page
# depending on whether the creator of the item is logged in or not this
# function will return a form to edit the item or redirect to the login
# page


@app.route('/category/<int:category_id>/item/<int:item_id>/edit/',
           methods=['GET', 'POST'])
def editItem(category_id, item_id):
    if 'username' not in login_session:
        flash('You are not allowed to do that, sorry!')
        return redirect('/login')
# check if userid is correct here
    item = session.query(Item).filter_by(id=item_id).one()
    user_id = login_session['user_id']
    if user_id == item.user_id:
        categories = session.query(Category).all()
        if request.method == 'POST':
            if request.form['name']:
                item.name = request.form['name']
            if request.form['description']:
                item.description = request.form['description']
            item.category_id = int(request.form['category'])
            session.add(item)
            session.commit()
            flash("Edited %s" % item.name)
            return redirect(url_for('showItem', category_id=category_id,
                            item_id=item_id))
        else:
            return render_template('edititem.html', item=item,
                                   categories=categories)
    else:
        flash('You are not allowed to do that, sorry!')
        redirect(url_for('showItem', category_id=category_id, item_id=item_id))

# item page
# depending on whether the creator of the item is logged in or not this
# function will return a form to delete the item or redirect to the login
# page


@app.route('/category/<int:category_id>/item/<int:item_id>/delete/',
           methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    if 'username' not in login_session:
        flash('You are not allowed to do that, sorry!')
        return redirect('/login')

# check if userid is correct here
    item = session.query(Item).filter_by(id=item_id).one()
    user_id = login_session['user_id']
    if user_id == item.user_id:
        if request.method == 'POST':
            session.delete(item)
            session.commit()
            flash("Item deleted.")
            return redirect(url_for('home'))
        else:
            return render_template('deleteitem.html', item=item)
    else:
        flash('You are not allowed to do that, sorry!')
        redirect(url_for('showItem', category_id=category_id, item_id=item_id))


if __name__ == '__main__':
    app.secret_key = '17_no_0)(31'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
