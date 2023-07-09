from flask import Flask, url_for
from scripts.generate import generate_data
app = Flask(__name__)
try:
    generate_data()
except Exception as e:
    print(e)
    exit()

@app.route("/data")
def data():
    return open("dist/data.json","r").read()

if __name__ == '__main__':
    app.run()