#! /usr/bin/env python3

import AnyToJson
import Run.SyslogRun
import Parse.Fail2Ban
import Send.ElasticSend

class fail2ban(Run.SyslogRun.SyslogRun,Parse.Fail2Ban.Fail2Ban,Send.ElasticSend.ElasticSend,AnyToJson.AnyToJson):
    def __init__(self):
        super().__init__()


    def parse(self, line):
        ret = True
        event = {}

        for key, value in self.regs.items():
            match = value.match(line)
            if match:
                event["classification.identifier"] = self.source
                event["source.ip"] = match.group("HOST")
                event["destination.ip"] = match.group("FROM")
                event["classification.taxonomy"] = match.group("PROG")
                event["extra.additional"] = line

        if event.keys():
            print(event)
            if "id" in event.keys():
                ret = self.check_exclude(event["id"])
                ret = self.check_include(event["id"])

            if ret:
                print("SEEEENDING")
                return [event]

        return []


if __name__ == '__main__':
    main = fail2ban()
    main.run()
