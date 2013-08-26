#!/usr/bin/python
print "Content-Type: text/plain\n\n"

import  os
import  json
# import urllib2

import cgi
form = cgi.FieldStorage()

node_json = form["json"].value



if node_json is not None:
     node = json.loads(node_json)
     for i, plugin in enumerate(node['plugins']):
         if plugin['plugin'] == 'olsrd_nameservice.so.0.3':
            host = plugin['name']

     fp = './bigboard-nodes/'+ host +'.json'
     f = open(fp,"w")
     f.write(node_json)
     f.close()
     print "json saved"
else:
     print "did not send good json"
