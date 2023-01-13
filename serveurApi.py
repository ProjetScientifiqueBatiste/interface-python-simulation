from flask import Flask, render_template, request
import json

app = Flask(__name__)

ip = "192.168.1.172"
port = "5000"

data = ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/postData', methods=['POST'])
def postData():
    global data
    data = request.get_json()
    # Pretty print
    print(data)
    return "ok"

@app.route('/api/getData', methods=['GET'])
def getData():
    # print(f"Envoie de : {data}")
    # Return a json object
    return data

if __name__ == '__main__':
    app.run(host=ip, port=port, debug=True)