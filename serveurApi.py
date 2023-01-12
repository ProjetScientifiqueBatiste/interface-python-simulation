from flask import Flask, render_template, request

app = Flask(__name__)

ip = "172.20.10.3"
port = "5000"

data = ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/postData', methods=['POST'])
def postData():
    global data
    data = request.get_json()
    print(f"Reçu : {data}")
    return "ok"

@app.route('/api/getData', methods=['GET'])
def getData():
    print(f"Envoie de : {data}")
    # Return a json object
    return data

if __name__ == '__main__':
    app.run(host=ip, port=port, debug=True)