# Project: Item Catalog

## The task:

"You will develop an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items."

(copied from the course website)

This application is hence supposed to differentiate between sessions where a user is logged in or not, which user is logged in (the creator of a specific item or not) and render the corresponding webpage with the corresponding functionalities.

## The Set-Up/Requirements:

For this project, we will need:

- Python3
... because we will be coding in Python3 :)
https://docs.python.org/3/

    See how to install Python3 here:
    https://docs.python-guide.org/starting/install3/osx/

- Flask
This is a really cool and simple framework for developing
web applications.
Infos about Flask and how to install it can be found via:
http://flask.pocoo.org/

    Tip: Use pip3 instead of pip!

- Flask Bootstrap
Flask-Bootstrap gives us a really easy way to access the
bootstrap library. Here is the documentation for it:
https://pythonhosted.org/Flask-Bootstrap/

- SQLAlchemy
This is the module we will be using to interact with our database and for it's ORM (Object-Relational-Mapping).
More about SQLAlchemy here:
https://docs.sqlalchemy.org/en/latest/intro.html

- OAuth2Client
This will come in handy for our user login. It is a client library for OAuth2. Check it out via:
https://oauth2client.readthedocs.io/en/latest/

    Tip: You might need to use --user at the end of your installation command.

- Httplib2
This is a HTTP Client library for Python. For me it was installed along the OAuth2 Client but in case it's not for you, visit:
https://github.com/httplib2/httplib2

- Requests
Another HTTP library for Python - safe for human consumption, as specified on the website
http://docs.python-requests.org/en/master/

<b>Ready? Let's go !</b>

## Running the code:

In a few steps your application will be up and running, bear with me:

1) Download this code and cd into the directory you downloaded it into.

2) Install all the necessary modules to run the project. Check the Set-Up section of this README, if you haven't yet.

2) Set up your database by passing the following commands to your command line:

    $ python3 database_setup.py

    $ python3 dbscript.py

This will create a database called 'catalogwithusers.db' with tables 'user', 'category' and 'item'. The second command will create a few categories for you.

    Attention: Do not edit or delete these categories manually if you already have items of that category.


3) Now run the application by passing

    $ python3 project.py

    to your command line

4) Visit http://localhost:8000/ in your browser :)

5) Log in with a gmail account (This will create a first user in your database)

6) Now we are ready to add some items to the database. Type

    $ python3 additems.py

    in your command line and refresh the homepage.

7) Now play around with the webpage as you wish!


Let me know if anything didn't work for you!

Cheers :)