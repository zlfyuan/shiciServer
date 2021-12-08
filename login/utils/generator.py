import json
import random
import os
from shiciServer import settings

class Generator:
    def randomName(self):
        try:
            path = os.path.join(settings.BASE_DIR, "static/food.json")
            with open(path) as f:
                noun = json.loads(f.read())
                name = noun[random.randrange(len(noun) - 1)][0]
                print(name)
            return name
        except IOError:
            print(IOError.errno)
