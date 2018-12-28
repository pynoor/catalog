from flask import Flask
app = Flask(__name__)

if __name__ == '__main__':
    app.secret_key = '17_no_0)(31'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
