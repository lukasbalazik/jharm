#! /usr/bin/env python3

import AnyToJson
import Run.SyslogRun
import Parse.RegexParse
import Send.SocketSend

class default_multiline(Run.SyslogRun.SyslogRun,Parse.RegexParse.RegexParse,Send.SocketSend.SocketSend,AnyToJson.AnyToJson):
    def __init__(self):
        super().__init__()
        self.event = {}


    def parse(self, line):
        ret = True
        ID_found = self.regs['multiline_id'].match(line)
        if ID_found == None:
            return []

        ID = ID_found.group("multiline_id")

        if not ID in self.event.keys():
            self.event[ID] = {}
            self.event[ID]["log"] = ""

        self.event[ID] = self.regex_parse(self.event[ID], line)

        if all(x in self.event[ID].keys() for x in self.keys):
            if "id" in event[ID].keys():
                ret = self.check_exclude(event[ID]["id"])
                ret = self.check_include(event[ID]["id"])

            if ret:
                return [self.event.pop(ID)]

        return []


if __name__ == '__main__':
    main = default_multiline()
    main.run()
