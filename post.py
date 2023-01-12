import requests

data = {"test": "test"}

ip = "192.168.109.180"
port = "5000"

# Send data to the server
r = requests.post(f"http://{ip}:{port}/api/postData", json=data)
print(f"Résultat requete : {r.text}")