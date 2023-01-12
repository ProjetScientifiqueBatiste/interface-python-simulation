import os
import json

ip = "192.168.109.139"
port = "9090"
adress = f"http://{ip}:{port}/UrgenceManager/Capteur/GetCapteursData"

# get the data from the server and store it
os.system(f"curl {adress} > ./data/data.json")

# Read the data from the file
with open("./data/data.json", "r") as f:
    data = json.load(f)

    for capteur in data:
        id = capteur["numCapteur"]
        intensity = capteur["intCapteur"]
        state = 1 if capteur["etat"] == "ALLUME" else 0

        print(f"Capteur {id} : Valeur --> {intensity}, Etat --> {state}")