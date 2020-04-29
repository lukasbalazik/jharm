import AnyToJson
import re
import json

class JsonLoad(AnyToJson.AnyToJson):
    def __init__(self):
        super().__init__()

        self.keys = self.conf.get('detection', 'keys').split(',')

        self.regs = {}

        for k,v in self.conf.items('regex'):
            self.regs[k] = re.compile(v)


    def load_json(self, line):
        event = {}

        match = self.regs["json"].match(line)        
        if not match:
            return None

        event = json.loads(match.group(1))

        match = self.regs["context"].match(line)        
        if not match:
            return None
        event["extra.context"] = match.group(1)

        if "classification.identifier" not in event:
            event["classification.identifier"] = self.conf.get("detection", "source")

        return event

