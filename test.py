import json
import requests

address = "http://192.168.109.180:5000/api/getData"

def getData():
    data = requests.get(address)
    data = json.loads(data.text)
    print(data)

if __name__ == "__main__":
    getData()