#IMPORTS
from flask import Flask, request,render_template;import requests,ai as a
#SETUP
query = ""
app = Flask(__name__)
#FLASK
@app.route("/")
def index():
    return "Online"
@app.route('/query/', methods=['GET'])
def query():
    global query
    query = request.args.get('query')
    print(f"Received search query: {query}")
    return render_template('result.html', result=a.run(query))
@app.route("/database/", methods=['POST'])
def database():
    global query
    data = request.get_json()
    data["query"] = query
    print(data)
    requests.post("https://hexdb.isaacrichardson.repl.co/add",json=data)
    return "Data received"
app.run("0.0.0.0")
