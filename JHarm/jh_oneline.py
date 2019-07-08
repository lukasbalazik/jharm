#! /usr/bin/env python3

import AnyToJson
import Run.SyslogRun
import Parse.RegexParse
import Send.ZeroMQSend

class default_oneline(Run.SyslogRun.SyslogRun,Parse.RegexParse.RegexParse,Send.ZeroMQSend.ZeroMQSend,AnyToJson.AnyToJson):

    def __init__(self):
        super().__init__()

    def parse(self, line):
        ret = True
        event = {}
        event["log"] = line
                
        event = self.regex_parse(event, line)       

        if all(x in event.keys() for x in self.keys):
            if "id" in event.keys():
				ret = self.check_exclude(event["id"])
				ret = self.check_include(event["id"])

            if ret:
                return [event]

        return []


if __name__ == '__main__':
    main = default_oneline()
    main.run()
