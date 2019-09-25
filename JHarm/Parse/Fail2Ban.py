import AnyToJson
import re
import os

class Fail2Ban(AnyToJson.AnyToJson):
    def __init__(self):
        super().__init__()

        self.i = 0
        self.regs = {}    
        self.prepared_regex = {}    

        self.files_readed = []

        self.source = self.conf.get("detection", "source")
        self.prepared_regex["HOST"] = self.conf.get("config", "host_regex")
        self.prepared_regex["__prefix_line"] = self.conf.get("config", "prefix_regex")

        for fl in os.listdir(self.conf.get("config", "fail2ban_dir")+"/filter.d/"):
            if fl.endswith(".conf"):
                self.readfile(fl)

        self.files_readed = map(lambda each:each.strip(".conf"), self.files_readed)

        for key, value in self.prepared_regex.items():
            if "failregex" in key:
                self.regs[key] = re.compile(value)


    def readfile(self, fl):
        with open("/etc/fail2ban/filter.d/"+fl) as f:
            lines = f.readlines()

        goto = ""

        for line in lines:
            if line.startswith("before = "):
                goto = (line.split("before = ")[1]).rstrip()

        if goto and goto not in self.files_readed:
            self.readfile(goto)    

        for line in lines:
            self.get_regex(line)

        if fl not in self.files_readed:
            self.files_readed.append(fl)


    def get_regex(self, line):
        if line.startswith("#") or line.startswith("[") or line.startswith("\n") or line.startswith("ignoreregex"):
            return None

        line = line.rstrip()    
        match = re.findall("%\(([^\)]*)\)s", line)

        for name in match:     
            if "_" in name or "?P<"+name+">":
                line = re.sub("%\("+name+"\)s", self.prepared_regex[name], line)
                continue
            line = re.sub("%\("+name+"\)s", "(?P<"+name+">"+self.prepared_regex[name]+")", line)

        line = re.sub("<HOST>", "(?P<HOST>"+self.prepared_regex["HOST"]+")", line) # replace special fail2ban variable
        line = re.sub("\?P\(", "(", line) # fix broken regex

        data = line.split("=", 1)

        if len(data) == 2:
            if "__prefix_line" != data[0].rstrip():
                self.prepared_regex[data[0].rstrip()] = data[1].lstrip()
                self.rkey = data[0].rstrip()
        else:
            self.prepared_regex[self.rkey+str(self.i)] = data[0].lstrip()
            self.i += 1

