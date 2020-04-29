#! /usr/bin/env python3

import AnyToJson
import Run.SyslogRun
import Parse.JsonLoad
import Send.ElasticSend


class waf_jsonload(Run.SyslogRun.SyslogRun,Parse.JsonLoad.JsonLoad,Send.ElasticSend.ElasticSend,AnyToJson.AnyToJson):

    def __init__(self):
        super().__init__()

    def parse(self, line):
        ret = True
        event = self.load_json(line)       
        if not event:
            return []

        try:
            event["extra.waf_log"] = event.pop("log")
        except:
            pass
        event["extra.additional"] = line
            
        event["source.ip"] = event.pop("ip")
        event["destination.fqdn"] = event.pop("host")
        event["destination.url"] = event["destination.fqdn"]+event.pop("url")
        event["classification.taxonomy"] = event.pop("vsf_rule_name")
        event["extra.rule.id"] = event.pop("vsf_rule_id")

        if all(x in event.keys() for x in self.keys):

            if "id" in event.keys():
                ret = self.check_exclude(event["id"])
                ret = self.check_include(event["id"])

            if ret:
                return [event]

        return []


if __name__ == '__main__':
    main = waf_jsonload()
    main.run()
