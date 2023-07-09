from flask import Flask, url_for
from scripts.generate import generate_data
from pathlib import Path
BASE_FOLDER = Path(__file__).parent.resolve()

app = Flask(__name__)
try:
    generate_data()
except Exception as e:
    print(e)
    exit()

@app.route("/data")
def data():
    return open(BASE_FOLDER / "dist/data.json","r").read()

if __name__ == '__main__':
    app.run()