from flask import Flask
from db_settings import config


app = Flask(__name__)

@app.route()
def index():
    pass


if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True, port=5050)
