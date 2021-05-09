from flask import Flask
from routes.search import search_blueprint
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(search_blueprint)
CORS(app)
if __name__ == "__main__":
    app.run("0.0.0.0",port=8005,debug=True,threaded=True)