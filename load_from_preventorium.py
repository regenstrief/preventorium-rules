#!/usr/bin/env python

# Pull rules from Preventorium and update local files

import requests
import re

url = "https://virtualpreventorium.com/cds_preventorium/pkgAdmin/rules"

resp = requests.get(url=url)
data = resp.json()

mapping = {}
with open("mappings.txt") as mappings_file:
	for line in mappings_file:
		# Parse any line in form "a=b", ignoring blank lines & comments
		if not re.match("^\s*(#.*)?$", line) and re.match("^[^=]+=.+$", line):
			name, filename = line.partition("=")[::2]
			mapping[name.strip()] = filename.strip()

for rule_name in mapping.keys():
	filename = mapping[rule_name]
	rule = filter(lambda x: x['name']==rule_name, data)[0]['rule']
	with open(filename, "w") as file:
		file.write(rule)