#!/usr/bin/python
import  os
import  json
import urllib2

ip_mac_map = {}
links = {}
nodes = {}

# this function takes a url of the json file, and returns a decoded json obj
def decode_json(url):
    try: 
        ret = json.loads(urllib2.urlopen(url).read())
        return ret
    except (ValueError, KeyError, TypeError):
        return "JSON format error"

# this function takes decoded json from decode_json() and parses out the node
# data. additionally, this function will build an IP MAC address table.

def parse_node(decoded_json):
        # grab some stuff that we know about the node.
        ip4addr = decoded_json['interfaces'][0]['ipv4Address']
        deviceMac = decoded_json['interfaces'][0]['macAddress']
        deviceName = decoded_json['interfaces'][0]['name']
        host = decoded_json['config']['olsrdBuildHost']
        # set the gateway value
        gateway = True
        if decoded_json['config']['hasIpv4Gateway'] == False and decoded_json['config']['hasIpv6Gateway'] == False:
            gateway = False       

        # pass some data to sets outside the function
        ip_mac_map[ip4addr] = deviceMac
        node_links = decoded_json['links']
        links[deviceMac] = node_links

        # return the ffhmap formatted data
        return {'id' : deviceMac, 'name' : host, 'flags' : {'gateway' : gateway }}

# this loop will pull the node info, and build a set with all of relevant info;
# since ffhmap wants MAC addresses, and OLSR info deals in IP addresses, we 
# will have to map those pieces of data, and build link information only after
# we have gone through all the nodes, and recorded their mac addresses.
i = 0
for ip in open('monitored-nodes', 'r').readlines():
    url = 'http://'+ip+':9090/all'
    nodes[i] = parse_node(decode_json(url))
    i+1

# with the the complete set of IP to MAC mapping we can now figure out the

out_links = {}
i = 0
for linkID in links:
    destIP = links[linkID][0]['localIP']
    destMac = ip_mac_map[destIP]
    linksID = linkID+'-'+destMac
    local_quality = links[linkID][0]['linkQuality']
    neighbor_quality = links[linkID][0]['neighborLinkQuality']
    target = destMac

    quality = str(local_quality) +', '+ str(neighbor_quality)
    out_links[i] = {'id' : linksID, 'source' : linkID, 'quality' : quality, 'target': target}
    i+1


# print nodes
#print out_links
json_out = {'nodes':nodes, 'links':out_links}
with open('nodes.json', 'w') as outfile:
    json.dump(json_out, outfile)
