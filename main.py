from sourceserver.sourceserver import SourceServer
import json
from time import sleep

s0 = SourceServer("65.21.189.168:27015")

if s0.isClosed is True:
    print("Server is offline")
    quit
else:
    print("Server is online")
    pass


def get_rules():
    rules = s0.rules
    info = s0.info

    if s0.isClosed is True:
        quit
    else:
        pass

    return rules, info

def save_rules():
    rules, info = get_rules()
    with open('rules.json', 'w') as f:
        json.dump(rules, f, indent=4)
    with open('info.json', 'w') as f:
        json.dump(info, f, indent=4)