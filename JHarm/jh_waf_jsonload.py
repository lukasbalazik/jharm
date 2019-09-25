#! /usr/bin/env python3

import AnyToJson
import Run.SyslogRun
import Parse.JsonLoad
import Send.ZeroMQSend


class waf_jsonload(Run.SyslogRun.SyslogRun,Parse.JsonLoad.JsonLoad,Send.ZeroMQSend.ZeroMQSend,AnyToJson.AnyToJson):

    def __init__(self):
        super().__init__()

    def parse(self, line):
        ret = True
        event = self.load_json(line)       
        if not event:
            return []

        try:
            event["waf_log"] = event.pop("log")
        except:
            pass
        event["log"] = line

        if all(x in event.keys() for x in self.keys):
            event["src_ip"] = event.pop("ip")
            event["signature"] = event.pop("vsf_rule_name")
            if "id" in event.keys():
                ret = self.check_exclude(event["id"])
                ret = self.check_include(event["id"])

            if ret:
                return [event]

        return []


if __name__ == '__main__':
    main = waf_jsonload()
    main.run()
