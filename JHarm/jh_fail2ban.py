#! /usr/bin/env python3

import AnyToJson
import Run.SyslogRun
import Parse.Fail2Ban
import Send.ZeroMQSend

class fail2ban(Run.SyslogRun.SyslogRun,Parse.Fail2Ban.Fail2Ban,Send.ZeroMQSend.ZeroMQSend,AnyToJson.AnyToJson):
    def __init__(self):
        super().__init__()


    def parse(self, line):
        ret = True
        event = {}

        for key, value in self.regs.items():
            match = value.match(line)
            if match:
                event["log"] = line
                event["source"] = self.source
                event["src_ip"] = match.group("HOST")
                event["dst_ip"] = match.group("FROM")
                event["signature"] = match.group("PROG")

        if event.keys():
            if "id" in event.keys():
                ret = self.check_exclude(event["id"])
                ret = self.check_include(event["id"])

            if ret:
                return [event]

        return []


if __name__ == '__main__':
    main = fail2ban()
    main.run()
