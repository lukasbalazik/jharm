import AnyToJson
import re

class RegexParse(AnyToJson.AnyToJson):
    def __init__(self):
        super().__init__()

        self.keys = self.conf.get('detection', 'keys').split(',')

        base = ''
        if self.conf.has_option('detection', 'base'):
            base = self.conf.get('detection', 'base')

        self.regs = {}

        for k,v in self.conf.items('regex'):
            self.regs[k] = re.compile(base + v)

    def regex_parse(self, event, line):
        event["log"] += line
        
        if "source" not in event:
            event["source"] = self.conf.get("detection", "source")

        for key in self.regs.keys():
            match = self.regs[key].match(line)        
            if not match:
                continue

            for k, v in match.groupdict().items():
                if k not in event:
                    event[k] = v

        return event

