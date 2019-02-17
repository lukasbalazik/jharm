#! /usr/bin/env python3

import AnyToJson
import Run.SyslogRun
import Parse.RegexParse
import Send.ZeroMQSend

class waf_varnish(Run.SyslogRun.SyslogRun,Parse.RegexParse.RegexParse,Send.ZeroMQSend.ZeroMQSend,AnyToJson.AnyToJson):
    def __init__(self):
        super().__init__()
        self.clean_up()

    def clean_up(self):
        self.event = {}
        self.event['log'] = ""
    
    def parse(self, line):
        self.event['log'] += line

        for key in self.regs.keys():
            match = self.regs[key].match(line)        
            if match:
                if key == "start":
                    self.clean_up()
                    return []
                self.event[key] = match.group(key)

        if all(x in self.event.keys() for x in self.keys):
            return [self.event]

        return []


if __name__ == '__main__':
    main = waf_varnish()
    main.run()
