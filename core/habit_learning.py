import json

FILE = "habits.json"


def learn(command):

    try:
        with open(FILE, "r") as f:
            data = json.load(f)
    except:
        data = {}

    data[command] = data.get(command, 0) + 1

    with open(FILE, "w") as f:
        json.dump(data, f)